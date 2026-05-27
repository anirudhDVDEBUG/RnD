"""Phase 4: Code Generation — produce code stubs from plan + spec."""

from dataclasses import dataclass
from typing import List
from .spec import Spec
from .planner import Plan, Task


@dataclass
class GeneratedFile:
    path: str
    content: str
    task_id: int
    requirements: List[str]


def generate_model_code(spec: Spec, task: Task) -> GeneratedFile:
    """Generate a Python dataclass model from spec data models."""
    model_name = task.component.replace("_model", "")
    model = next((m for m in spec.data_models if m.name.lower() == model_name), None)
    if not model:
        return GeneratedFile(
            path=f"{model_name}.py",
            content=f"# Stub for {model_name}\n",
            task_id=task.id,
            requirements=task.requirements,
        )

    lines = [
        f'"""Auto-generated model: {model.name}"""',
        "from dataclasses import dataclass, field",
        "from typing import Optional",
        "",
        "",
        f"@dataclass",
        f"class {model.name}:",
    ]
    for fname, ftype in model.fields.items():
        py_type = {"string": "str", "integer": "int", "boolean": "bool", "float": "float"}.get(ftype, "str")
        lines.append(f"    {fname}: {py_type} = None")

    lines.append("")
    lines.append(f"    def validate(self) -> list:")
    lines.append(f'        errors = []')
    for fname, ftype in model.fields.items():
        lines.append(f'        if self.{fname} is None:')
        lines.append(f'            errors.append("{fname} is required")')
    lines.append(f"        return errors")

    return GeneratedFile(
        path=f"{model_name}.py",
        content="\n".join(lines),
        task_id=task.id,
        requirements=task.requirements,
    )


def generate_service_code(spec: Spec, task: Task) -> GeneratedFile:
    """Generate service stubs from API endpoints."""
    lines = [
        f'"""Auto-generated service for {spec.name}"""',
        "",
    ]
    for ep in spec.api_endpoints:
        func_name = ep.path.strip("/").replace("/", "_").replace("{", "").replace("}", "")
        lines.append(f"def handle_{ep.method.lower()}_{func_name}(request):")
        lines.append(f'    """Handler for {ep.method} {ep.path}: {ep.description}"""')
        lines.append(f"    # TODO: implement against spec requirements")
        lines.append(f"    raise NotImplementedError")
        lines.append("")

    return GeneratedFile(
        path="service.py",
        content="\n".join(lines),
        task_id=task.id,
        requirements=task.requirements,
    )


def generate_test_code(spec: Spec, task: Task) -> GeneratedFile:
    """Generate BDD-style test stubs for all requirements."""
    lines = [
        f'"""Auto-generated tests for {spec.name}"""',
        "",
    ]
    for req in spec.requirements:
        func_name = req.id.lower().replace("-", "_")
        lines.append(f"def test_{func_name}():")
        lines.append(f'    """{req.id}: {req.text}"""')
        lines.append(f"    # Given: preconditions")
        lines.append(f"    # When: action")
        lines.append(f"    # Then: verify {req.text}")
        lines.append(f"    assert True  # placeholder")
        lines.append("")

    return GeneratedFile(
        path="tests.py",
        content="\n".join(lines),
        task_id=task.id,
        requirements=task.requirements,
    )


def generate_code(spec: Spec, plan: Plan) -> List[GeneratedFile]:
    """Run code generation for all tasks in the plan."""
    files = []
    for task in plan.tasks:
        if "model" in task.component:
            files.append(generate_model_code(spec, task))
        elif task.component == "service":
            files.append(generate_service_code(spec, task))
        elif task.component == "tests":
            files.append(generate_test_code(spec, task))
        elif task.component == "validator":
            files.append(GeneratedFile(
                path="validator.py",
                content=f'"""Auto-generated validator"""\n\ndef validate(data, constraints):\n    errors = []\n    for c in constraints:\n        pass  # TODO: implement constraint checks\n    return errors\n',
                task_id=task.id,
                requirements=task.requirements,
            ))
        task.mark_done()
    return files
