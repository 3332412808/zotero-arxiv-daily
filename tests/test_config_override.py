from pathlib import Path

from zotero_arxiv_daily.config_override import apply_custom_config_override


def test_apply_custom_config_override_writes_valid_yaml(tmp_path: Path):
    target = tmp_path / "custom.yaml"

    applied, message = apply_custom_config_override(
        "zotero:\n  include_path: [\"foo/**\"]",
        target,
    )

    assert applied is True
    assert message == ""
    assert target.read_text(encoding="utf-8") == "zotero:\n  include_path: [\"foo/**\"]\n"


def test_apply_custom_config_override_rejects_invalid_yaml(tmp_path: Path):
    target = tmp_path / "custom.yaml"
    target.write_text("existing: true\n", encoding="utf-8")

    applied, message = apply_custom_config_override(
        "zotero:\n  include_path: include_path: [\"foo/**\"]",
        target,
    )

    assert applied is False
    assert "invalid YAML" in message
    assert target.read_text(encoding="utf-8") == "existing: true\n"


def test_apply_custom_config_override_supports_escaped_newlines(tmp_path: Path):
    target = tmp_path / "custom.yaml"

    applied, message = apply_custom_config_override(
        "zotero:\\n  include_path: [\"foo/**\"]",
        target,
    )

    assert applied is True
    assert message == ""
    assert target.read_text(encoding="utf-8") == "zotero:\n  include_path: [\"foo/**\"]\n"
