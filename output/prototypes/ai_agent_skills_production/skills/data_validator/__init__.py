"""Data validator skill - validates structured data against schemas."""

from skills.base import BaseSkill, SkillResult
from skills.registry import registry


@registry.register
class DataValidatorSkill(BaseSkill):
    name = "data_validator"
    description = "Validate structured data against a schema definition"
    version = "1.0.0"

    def validate_input(self, input_data: dict) -> bool:
        return "data" in input_data and "schema" in input_data

    def execute(self, input_data: dict) -> SkillResult:
        data = input_data["data"]
        schema = input_data["schema"]
        errors = []

        for field_name, rules in schema.items():
            value = data.get(field_name)

            if rules.get("required") and value is None:
                errors.append(f"Missing required field: {field_name}")
                continue

            if value is None:
                continue

            expected_type = rules.get("type")
            if expected_type:
                type_map = {"str": str, "int": int, "float": float, "bool": bool, "list": list, "dict": dict}
                if expected_type in type_map and not isinstance(value, type_map[expected_type]):
                    errors.append(f"Field '{field_name}': expected {expected_type}, got {type(value).__name__}")

            if "min_length" in rules and isinstance(value, str) and len(value) < rules["min_length"]:
                errors.append(f"Field '{field_name}': length {len(value)} < min {rules['min_length']}")

            if "max_value" in rules and isinstance(value, (int, float)) and value > rules["max_value"]:
                errors.append(f"Field '{field_name}': value {value} > max {rules['max_value']}")

        return SkillResult(
            success=len(errors) == 0,
            data={"valid": len(errors) == 0, "errors": errors, "fields_checked": len(schema)},
            metadata={"error_count": len(errors)},
        )
