#!/usr/bin/env python3
"""
Mock Ansys AEDT MCP Server Demo

Simulates the ansys-aedt-mcp MCP server to demonstrate the workflow
without requiring an actual Ansys AEDT installation. Shows the tool
interface, request/response patterns, and simulation data flow.
"""

import json
import math
import random
import sys
from dataclasses import dataclass, field, asdict
from typing import Any

# ── Mock PyAEDT layer ──────────────────────────────────────────────

@dataclass
class MockDesign:
    name: str
    design_type: str
    variables: dict = field(default_factory=dict)
    objects: list = field(default_factory=list)
    boundaries: list = field(default_factory=list)
    excitations: list = field(default_factory=list)
    setups: list = field(default_factory=list)
    solved: bool = False


@dataclass
class MockProject:
    name: str
    designs: dict = field(default_factory=dict)
    active_design: str = ""


class MockAEDTSession:
    """Simulates an AEDT desktop session with PyAEDT-style API."""

    def __init__(self):
        self.projects: dict[str, MockProject] = {}
        self.active_project: str = ""

    def create_project(self, name: str) -> dict:
        proj = MockProject(name=name)
        self.projects[name] = proj
        self.active_project = name
        return {"status": "ok", "project": name, "path": f"C:/Users/sim/{name}.aedt"}

    def create_design(self, project: str, design_name: str, design_type: str) -> dict:
        if project not in self.projects:
            return {"status": "error", "message": f"Project '{project}' not found"}
        design = MockDesign(name=design_name, design_type=design_type)
        self.projects[project].designs[design_name] = design
        self.projects[project].active_design = design_name
        return {
            "status": "ok",
            "project": project,
            "design": design_name,
            "type": design_type,
        }

    def create_box(self, project: str, design: str, position: list,
                   dimensions: list, name: str, material: str) -> dict:
        d = self._get_design(project, design)
        if not d:
            return {"status": "error", "message": "Design not found"}
        obj = {
            "name": name, "type": "Box",
            "position": position, "dimensions": dimensions,
            "material": material,
        }
        d.objects.append(obj)
        return {"status": "ok", "object": name, "material": material}

    def create_cylinder(self, project: str, design: str, center: list,
                        radius: float, height: float, axis: str,
                        name: str, material: str) -> dict:
        d = self._get_design(project, design)
        if not d:
            return {"status": "error", "message": "Design not found"}
        obj = {
            "name": name, "type": "Cylinder",
            "center": center, "radius": radius,
            "height": height, "axis": axis, "material": material,
        }
        d.objects.append(obj)
        return {"status": "ok", "object": name, "material": material}

    def assign_excitation(self, project: str, design: str,
                          port_name: str, face_id: int, exc_type: str) -> dict:
        d = self._get_design(project, design)
        if not d:
            return {"status": "error", "message": "Design not found"}
        exc = {"name": port_name, "face_id": face_id, "type": exc_type}
        d.excitations.append(exc)
        return {"status": "ok", "excitation": port_name, "type": exc_type}

    def create_setup(self, project: str, design: str, setup_name: str,
                     frequency: str, max_passes: int) -> dict:
        d = self._get_design(project, design)
        if not d:
            return {"status": "error", "message": "Design not found"}
        setup = {
            "name": setup_name, "frequency": frequency,
            "max_passes": max_passes, "converged": False,
        }
        d.setups.append(setup)
        return {"status": "ok", "setup": setup_name, "frequency": frequency}

    def create_frequency_sweep(self, project: str, design: str,
                               setup_name: str, start: str, stop: str,
                               step: str, sweep_type: str) -> dict:
        return {
            "status": "ok",
            "setup": setup_name,
            "sweep": f"{start} - {stop} step {step}",
            "type": sweep_type,
        }

    def analyze(self, project: str, design: str, setup_name: str) -> dict:
        d = self._get_design(project, design)
        if not d:
            return {"status": "error", "message": "Design not found"}
        d.solved = True
        for s in d.setups:
            if s["name"] == setup_name:
                s["converged"] = True
        return {
            "status": "ok",
            "setup": setup_name,
            "converged": True,
            "passes": 8,
            "delta_s": 0.0018,
            "mesh_elements": 48523,
        }

    def get_s_parameters(self, project: str, design: str,
                         setup_name: str, parameter: str,
                         freq_start: float, freq_stop: float,
                         num_points: int) -> dict:
        """Generate realistic-looking S-parameter data for a patch antenna."""
        freqs = [freq_start + i * (freq_stop - freq_start) / (num_points - 1)
                 for i in range(num_points)]
        center = 2.4  # GHz resonance
        bw = 0.08     # bandwidth
        values = []
        for f in freqs:
            # Lorentzian dip at resonance
            base = -2.0
            dip = -25.0 * (bw ** 2) / ((f - center) ** 2 + bw ** 2)
            noise = random.uniform(-0.3, 0.3)
            values.append(round(base + dip + noise, 2))
        return {
            "status": "ok",
            "parameter": parameter,
            "frequencies_ghz": [round(f, 4) for f in freqs],
            "values_db": values,
            "min_value_db": round(min(values), 2),
            "min_freq_ghz": round(freqs[values.index(min(values))], 4),
        }

    def _get_design(self, project: str, design: str):
        proj = self.projects.get(project)
        if not proj:
            return None
        return proj.designs.get(design)


# ── MCP Tool Registry ──────────────────────────────────────────────

TOOLS = [
    {
        "name": "aedt_create_project",
        "description": "Create a new Ansys AEDT project",
        "inputSchema": {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
    },
    {
        "name": "aedt_create_design",
        "description": "Create a new design (HFSS, Maxwell, Q3D, Icepak) in a project",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project": {"type": "string"},
                "design_name": {"type": "string"},
                "design_type": {"type": "string", "enum": ["HFSS", "Maxwell3D", "Q3DExtractor", "Icepak"]},
            },
            "required": ["project", "design_name", "design_type"],
        },
    },
    {
        "name": "aedt_create_box",
        "description": "Create a 3D box in the design",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project": {"type": "string"},
                "design": {"type": "string"},
                "position": {"type": "array", "items": {"type": "number"}},
                "dimensions": {"type": "array", "items": {"type": "number"}},
                "name": {"type": "string"},
                "material": {"type": "string"},
            },
            "required": ["project", "design", "position", "dimensions", "name", "material"],
        },
    },
    {
        "name": "aedt_create_cylinder",
        "description": "Create a 3D cylinder in the design",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project": {"type": "string"},
                "design": {"type": "string"},
                "center": {"type": "array", "items": {"type": "number"}},
                "radius": {"type": "number"},
                "height": {"type": "number"},
                "axis": {"type": "string"},
                "name": {"type": "string"},
                "material": {"type": "string"},
            },
            "required": ["project", "design", "center", "radius", "height", "axis", "name", "material"],
        },
    },
    {
        "name": "aedt_assign_excitation",
        "description": "Assign a port excitation to a face",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project": {"type": "string"},
                "design": {"type": "string"},
                "port_name": {"type": "string"},
                "face_id": {"type": "integer"},
                "exc_type": {"type": "string", "enum": ["WavePort", "LumpedPort"]},
            },
            "required": ["project", "design", "port_name", "face_id", "exc_type"],
        },
    },
    {
        "name": "aedt_create_setup",
        "description": "Create an analysis setup with solution frequency and convergence criteria",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project": {"type": "string"},
                "design": {"type": "string"},
                "setup_name": {"type": "string"},
                "frequency": {"type": "string"},
                "max_passes": {"type": "integer"},
            },
            "required": ["project", "design", "setup_name", "frequency", "max_passes"],
        },
    },
    {
        "name": "aedt_create_frequency_sweep",
        "description": "Add a frequency sweep to an existing setup",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project": {"type": "string"},
                "design": {"type": "string"},
                "setup_name": {"type": "string"},
                "start": {"type": "string"},
                "stop": {"type": "string"},
                "step": {"type": "string"},
                "sweep_type": {"type": "string", "enum": ["Discrete", "Interpolating", "Fast"]},
            },
            "required": ["project", "design", "setup_name", "start", "stop", "step", "sweep_type"],
        },
    },
    {
        "name": "aedt_analyze",
        "description": "Run the simulation for a given setup",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project": {"type": "string"},
                "design": {"type": "string"},
                "setup_name": {"type": "string"},
            },
            "required": ["project", "design", "setup_name"],
        },
    },
    {
        "name": "aedt_get_s_parameters",
        "description": "Extract S-parameter results from a solved design",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project": {"type": "string"},
                "design": {"type": "string"},
                "setup_name": {"type": "string"},
                "parameter": {"type": "string"},
                "freq_start": {"type": "number"},
                "freq_stop": {"type": "number"},
                "num_points": {"type": "integer"},
            },
            "required": ["project", "design", "setup_name", "parameter"],
        },
    },
]


# ── MCP Protocol Simulation ───────────────────────────────────────

class MockMCPServer:
    """Simulates the MCP JSON-RPC request/response cycle."""

    def __init__(self):
        self.session = MockAEDTSession()

    def handle_request(self, method: str, params: dict) -> dict:
        if method == "initialize":
            return {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "ansys-aedt-mcp", "version": "0.1.0"},
            }
        elif method == "tools/list":
            return {"tools": TOOLS}
        elif method == "tools/call":
            return self._call_tool(params["name"], params.get("arguments", {}))
        return {"error": {"code": -32601, "message": f"Unknown method: {method}"}}

    def _call_tool(self, name: str, args: dict) -> dict:
        dispatch = {
            "aedt_create_project": lambda a: self.session.create_project(a["name"]),
            "aedt_create_design": lambda a: self.session.create_design(
                a["project"], a["design_name"], a["design_type"]),
            "aedt_create_box": lambda a: self.session.create_box(
                a["project"], a["design"], a["position"], a["dimensions"],
                a["name"], a["material"]),
            "aedt_create_cylinder": lambda a: self.session.create_cylinder(
                a["project"], a["design"], a["center"], a["radius"],
                a["height"], a["axis"], a["name"], a["material"]),
            "aedt_assign_excitation": lambda a: self.session.assign_excitation(
                a["project"], a["design"], a["port_name"], a["face_id"], a["exc_type"]),
            "aedt_create_setup": lambda a: self.session.create_setup(
                a["project"], a["design"], a["setup_name"], a["frequency"], a["max_passes"]),
            "aedt_create_frequency_sweep": lambda a: self.session.create_frequency_sweep(
                a["project"], a["design"], a["setup_name"],
                a["start"], a["stop"], a["step"], a["sweep_type"]),
            "aedt_analyze": lambda a: self.session.analyze(
                a["project"], a["design"], a["setup_name"]),
            "aedt_get_s_parameters": lambda a: self.session.get_s_parameters(
                a["project"], a["design"], a["setup_name"], a["parameter"],
                a.get("freq_start", 1.0), a.get("freq_stop", 4.0),
                a.get("num_points", 31)),
        }
        handler = dispatch.get(name)
        if not handler:
            return {"content": [{"type": "text", "text": f"Unknown tool: {name}"}]}
        result = handler(args)
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}


def format_jsonrpc(method: str, params: dict, id: int) -> dict:
    return {"jsonrpc": "2.0", "id": id, "method": method, "params": params}
