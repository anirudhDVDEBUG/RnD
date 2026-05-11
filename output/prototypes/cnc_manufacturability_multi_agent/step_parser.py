"""
STEP File Parser — Stage 1 of the pipeline.

In production this uses cadquery/OpenCASCADE for exact geometry extraction.
This module provides mock feature extraction for demo purposes, plus a
real parser function if cadquery is installed.
"""

import json
from pathlib import Path


def extract_features_mock(part_name: str = "sample_bracket") -> dict:
    """Return mock extracted features for demo without cadquery."""
    MOCK_PARTS = {
        "sample_bracket": {
            "part_name": "sample_bracket.step",
            "bounding_box_mm": [120.0, 80.0, 25.0],
            "volume_mm3": 148200.0,
            "surface_area_mm2": 32400.0,
            "holes": [
                {"diameter_mm": 8.0, "depth_mm": 25.0, "count": 4, "type": "through"},
                {"diameter_mm": 5.0, "depth_mm": 12.0, "count": 2, "type": "blind"},
                {"diameter_mm": 10.0, "depth_mm": 25.0, "count": 2, "type": "through"},
            ],
            "flat_surfaces": 12,
            "chamfers": [
                {"size_mm": 1.0, "count": 8},
            ],
            "fillets": [
                {"radius_mm": 3.0, "count": 4},
            ],
            "threads": [
                {"spec": "M8x1.25", "depth_mm": 20.0, "count": 4},
                {"spec": "M10x1.5", "depth_mm": 25.0, "count": 2},
            ],
            "pockets": [
                {"length_mm": 40.0, "width_mm": 20.0, "depth_mm": 8.0, "corner_radius_mm": 3.0, "count": 1},
            ],
        },
        "simple_plate": {
            "part_name": "simple_plate.step",
            "bounding_box_mm": [200.0, 100.0, 10.0],
            "volume_mm3": 195000.0,
            "surface_area_mm2": 46200.0,
            "holes": [
                {"diameter_mm": 6.0, "depth_mm": 10.0, "count": 6, "type": "through"},
            ],
            "flat_surfaces": 8,
            "chamfers": [{"size_mm": 0.5, "count": 4}],
            "fillets": [],
            "threads": [{"spec": "M6x1.0", "depth_mm": 10.0, "count": 6}],
            "pockets": [],
        },
    }
    return MOCK_PARTS.get(part_name, MOCK_PARTS["sample_bracket"])


def try_real_parser(step_path: str) -> dict | None:
    """Attempt real STEP parsing with cadquery if available."""
    try:
        import cadquery as cq
        from OCP.BRepAdaptor import BRepAdaptor_Surface
        from OCP.GeomAbs import GeomAbs_Cylinder

        model = cq.importers.importStep(step_path)
        shape = model.val()
        bb = shape.BoundingBox()

        holes = {}
        for face in model.faces().vals():
            adaptor = BRepAdaptor_Surface(face.wrapped)
            if adaptor.GetType() == GeomAbs_Cylinder:
                radius = adaptor.Cylinder().Radius()
                diameter = round(radius * 2, 3)
                holes[diameter] = holes.get(diameter, 0) + 1

        return {
            "part_name": Path(step_path).name,
            "bounding_box_mm": [round(bb.xlen, 2), round(bb.ylen, 2), round(bb.zlen, 2)],
            "volume_mm3": round(shape.Volume(), 2),
            "surface_area_mm2": round(shape.Area(), 2),
            "holes": [
                {"diameter_mm": d, "count": c, "type": "detected"}
                for d, c in holes.items()
            ],
            "flat_surfaces": 0,  # simplified
            "chamfers": [],
            "fillets": [],
            "threads": [],
            "pockets": [],
        }
    except ImportError:
        return None
