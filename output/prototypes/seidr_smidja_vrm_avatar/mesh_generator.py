"""Parametric humanoid mesh generator for VRM avatars."""

import struct
import math


# Vertex counts by density
DENSITY_MAP = {
    "low": 6400,
    "medium": 12847,
    "high": 18200,
}


def generate_humanoid_mesh(config):
    """
    Generate a parametric humanoid mesh based on configuration.
    Returns mesh data dict with vertices, faces, and UVs as binary buffers.
    """
    density = config.get("vertex_density", "medium")
    vertex_count = DENSITY_MAP.get(density, 12847)
    head_ratio = config.get("head_ratio", 1.1)
    eye_scale = config.get("eye_scale", 1.2)

    # Generate vertices for humanoid body parts
    vertices = []
    normals = []
    uvs = []

    # Body proportions (anime-style: larger head, slimmer body)
    body_parts = _generate_body_layout(vertex_count, head_ratio)

    for part_name, part_verts in body_parts.items():
        for v in part_verts:
            vertices.extend(v["pos"])
            normals.extend(v["normal"])
            uvs.extend(v["uv"])

    # Generate face indices (triangles)
    face_count = (vertex_count * 2) - 4  # approximate
    faces = _generate_faces(vertex_count, face_count)

    # Pack into binary buffers
    vertex_buffer = struct.pack(f'{len(vertices)}f', *vertices)
    normal_buffer = struct.pack(f'{len(normals)}f', *normals)
    uv_buffer = struct.pack(f'{len(uvs)}f', *uvs)
    index_buffer = struct.pack(f'{len(faces)}H', *faces)

    return {
        "vertex_count": vertex_count,
        "face_count": face_count,
        "vertices": vertex_buffer,
        "normals": normal_buffer,
        "uvs": uv_buffer,
        "indices": index_buffer,
        "body_parts": list(body_parts.keys()),
    }


def _generate_body_layout(total_verts, head_ratio):
    """Generate vertex distribution across body parts."""
    # Distribution ratios
    parts = {
        "head": 0.20,
        "torso": 0.25,
        "arms_left": 0.10,
        "arms_right": 0.10,
        "hands_left": 0.05,
        "hands_right": 0.05,
        "legs_left": 0.10,
        "legs_right": 0.10,
        "hair": 0.05,
    }

    result = {}
    for part_name, ratio in parts.items():
        count = int(total_verts * ratio)
        result[part_name] = _generate_part_vertices(part_name, count, head_ratio)

    return result


def _generate_part_vertices(part_name, count, head_ratio):
    """Generate vertices for a body part using parametric shapes."""
    vertices = []

    # Body part center positions (Y-up coordinate system)
    centers = {
        "head": (0.0, 1.5 * head_ratio, 0.0),
        "torso": (0.0, 1.0, 0.0),
        "arms_left": (-0.4, 1.1, 0.0),
        "arms_right": (0.4, 1.1, 0.0),
        "hands_left": (-0.6, 0.8, 0.0),
        "hands_right": (0.6, 0.8, 0.0),
        "legs_left": (-0.15, 0.4, 0.0),
        "legs_right": (0.15, 0.4, 0.0),
        "hair": (0.0, 1.7 * head_ratio, -0.05),
    }

    center = centers.get(part_name, (0.0, 1.0, 0.0))

    # Generate vertices in a parametric ellipsoid around center
    for i in range(count):
        t = i / max(count - 1, 1)
        phi = t * math.pi * 2
        theta = (i * 0.618033) * math.pi  # golden angle for distribution

        # Radius varies by part
        r = 0.15 if "hand" in part_name else 0.25
        if part_name == "head":
            r = 0.18 * head_ratio
        elif part_name == "hair":
            r = 0.22 * head_ratio

        x = center[0] + r * math.sin(theta) * math.cos(phi)
        y = center[1] + r * math.sin(theta) * math.sin(phi) * 0.5
        z = center[2] + r * math.cos(theta)

        # Normal (pointing outward from center)
        nx = x - center[0]
        ny = y - center[1]
        nz = z - center[2]
        length = math.sqrt(nx*nx + ny*ny + nz*nz) or 1.0
        nx, ny, nz = nx/length, ny/length, nz/length

        # UV mapping
        u = (math.atan2(nz, nx) / (2 * math.pi)) + 0.5
        v = (math.asin(max(-1, min(1, ny))) / math.pi) + 0.5

        vertices.append({
            "pos": [x, y, z],
            "normal": [nx, ny, nz],
            "uv": [u, v],
        })

    return vertices


def _generate_faces(vertex_count, face_count):
    """Generate triangle indices for the mesh."""
    faces = []
    # Simple triangle strip generation
    for i in range(min(face_count, vertex_count - 2)):
        if i % 2 == 0:
            faces.extend([i, i + 1, i + 2])
        else:
            faces.extend([i + 1, i, i + 2])
    return faces
