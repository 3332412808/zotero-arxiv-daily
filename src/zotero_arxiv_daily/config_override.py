from pathlib import Path

import yaml


def apply_custom_config_override(custom_config: str | None, target_path: Path) -> tuple[bool, str]:
    if not custom_config:
        return False, "CUSTOM_CONFIG is empty. Using repository config/custom.yaml."

    normalized_custom_config = custom_config
    if "\\n" in custom_config and "\n" not in custom_config:
        normalized_custom_config = custom_config.replace("\\r\\n", "\n").replace("\\n", "\n")

    try:
        yaml.safe_load(normalized_custom_config)
    except yaml.YAMLError as exc:
        return (
            False,
            f"Ignoring CUSTOM_CONFIG because it is invalid YAML. Using repository config/custom.yaml instead.\n{exc}",
        )

    target_path.write_text(f"{normalized_custom_config.rstrip()}\n", encoding="utf-8")
    return True, ""
