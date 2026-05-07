"""VRM file packager -- creates a valid glTF/VRM binary file."""

import json
import struct


def package_vrm(output_path, mesh_data, blendshapes, spring_bones, config, name):
    """
    Package mesh data into a VRM file (glTF 2.0 binary with VRM extensions).
    Returns the file size in bytes.
    """
    # Build glTF JSON structure
    gltf_json = _build_gltf_json(mesh_data, blendshapes, spring_bones, config, name)
    json_bytes = json.dumps(gltf_json, separators=(',', ':')).encode('utf-8')

    # Pad JSON to 4-byte alignment
    json_padding = (4 - (len(json_bytes) % 4)) % 4
    json_bytes += b' ' * json_padding

    # Binary buffer (mesh data)
    bin_data = mesh_data["vertices"] + mesh_data["normals"] + mesh_data["uvs"] + mesh_data["indices"]
    bin_padding = (4 - (len(bin_data) % 4)) % 4
    bin_data += b'\x00' * bin_padding

    # glTF binary header
    total_length = 12 + 8 + len(json_bytes) + 8 + len(bin_data)

    with open(output_path, 'wb') as f:
        # Header
        f.write(b'glTF')                                    # magic
        f.write(struct.pack('<I', 2))                       # version
        f.write(struct.pack('<I', total_length))            # total length

        # JSON chunk
        f.write(struct.pack('<I', len(json_bytes)))         # chunk length
        f.write(b'JSON')                                    # chunk type
        f.write(json_bytes)

        # Binary chunk
        f.write(struct.pack('<I', len(bin_data)))           # chunk length
        f.write(b'BIN\x00')                                # chunk type
        f.write(bin_data)

    return total_length


def _build_gltf_json(mesh_data, blendshapes, spring_bones, config, name):
    """Build the glTF JSON descriptor with VRM extensions."""
    vertex_count = mesh_data["vertex_count"]
    vertices_byte_length = vertex_count * 3 * 4  # 3 floats per vertex
    normals_byte_length = vertex_count * 3 * 4
    uvs_byte_length = vertex_count * 2 * 4
    indices_byte_length = len(mesh_data["indices"])

    total_buffer_length = vertices_byte_length + normals_byte_length + uvs_byte_length + indices_byte_length

    return {
        "asset": {
            "version": "2.0",
            "generator": "Seidr-Smidja v0.3.0"
        },
        "extensionsUsed": ["VRM"],
        "extensions": {
            "VRM": {
                "specVersion": "0.0",
                "meta": {
                    "title": name,
                    "author": "Seidr-Smidja Agent",
                    "version": "1.0",
                    "allowedUserName": "Everyone",
                    "violentUssageName": "Disallow",
                    "sexualUssageName": "Disallow",
                    "commercialUssageName": "Allow",
                    "licenseName": "CC_BY_4_0",
                },
                "humanoid": {
                    "humanBones": _get_humanoid_bones()
                },
                "blendShapeMaster": {
                    "blendShapeGroups": [
                        {"name": bs, "presetName": bs, "binds": []}
                        for bs in blendshapes
                    ]
                },
                "secondaryAnimation": {
                    "boneGroups": [
                        {
                            "comment": f"spring_chain_{i}",
                            "stiffiness": 0.5,
                            "gravityPower": 0.1,
                            "dragForce": 0.4,
                            "bones": [i]
                        }
                        for i in range(spring_bones)
                    ]
                },
                "materialProperties": [
                    {
                        "name": "body_material",
                        "shader": "VRM/MToon",
                        "renderQueue": 2000,
                        "keywordMap": {"_ALPHABLEND_ON": False},
                        "floatProperties": {"_ShadeShift": 0.1},
                        "vectorProperties": {
                            "_Color": config["palette"][0] if config.get("palette") else "#FFFFFF"
                        }
                    }
                ]
            }
        },
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [
            {"name": "root", "children": [1]},
            {"name": "body", "mesh": 0, "skin": 0}
        ],
        "meshes": [
            {
                "name": f"{name}_mesh",
                "primitives": [{
                    "attributes": {
                        "POSITION": 0,
                        "NORMAL": 1,
                        "TEXCOORD_0": 2
                    },
                    "indices": 3,
                    "material": 0
                }]
            }
        ],
        "materials": [
            {
                "name": "body_material",
                "pbrMetallicRoughness": {
                    "baseColorFactor": [0.9, 0.8, 0.75, 1.0],
                    "metallicFactor": 0.0,
                    "roughnessFactor": 0.8
                }
            }
        ],
        "skins": [
            {
                "joints": list(range(min(spring_bones, 10))),
                "skeleton": 0
            }
        ],
        "accessors": [
            {"bufferView": 0, "componentType": 5126, "count": vertex_count, "type": "VEC3"},
            {"bufferView": 1, "componentType": 5126, "count": vertex_count, "type": "VEC3"},
            {"bufferView": 2, "componentType": 5126, "count": vertex_count, "type": "VEC2"},
            {"bufferView": 3, "componentType": 5123, "count": vertex_count * 2, "type": "SCALAR"},
        ],
        "bufferViews": [
            {"buffer": 0, "byteOffset": 0, "byteLength": vertices_byte_length},
            {"buffer": 0, "byteOffset": vertices_byte_length, "byteLength": normals_byte_length},
            {"buffer": 0, "byteOffset": vertices_byte_length + normals_byte_length, "byteLength": uvs_byte_length},
            {"buffer": 0, "byteOffset": vertices_byte_length + normals_byte_length + uvs_byte_length, "byteLength": indices_byte_length},
        ],
        "buffers": [
            {"byteLength": total_buffer_length}
        ]
    }


def _get_humanoid_bones():
    """Return standard VRM humanoid bone mapping."""
    bones = [
        "hips", "spine", "chest", "upperChest", "neck", "head",
        "leftUpperArm", "leftLowerArm", "leftHand",
        "rightUpperArm", "rightLowerArm", "rightHand",
        "leftUpperLeg", "leftLowerLeg", "leftFoot",
        "rightUpperLeg", "rightLowerLeg", "rightFoot",
    ]
    return [{"bone": b, "node": i, "useDefaultValues": True} for i, b in enumerate(bones)]
