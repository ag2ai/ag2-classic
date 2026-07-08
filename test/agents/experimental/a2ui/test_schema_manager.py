# Copyright (c) 2023 - 2026, AG2ai, Inc., AG2ai open-source projects maintainers and core contributors
#
# SPDX-License-Identifier: Apache-2.0

import json
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest

from autogen.agents.experimental.a2ui.schema_manager import A2UISchemaManager


def _cp1252_default_open(
    file: Any,
    mode: str = "r",
    buffering: int = -1,
    encoding: str | None = None,
    errors: str | None = None,
    newline: str | None = None,
    closefd: bool = True,
    opener: Any | None = None,
) -> Any:
    if "b" not in mode and encoding is None:
        encoding = "cp1252"
    return Path(file).open(mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline)


class TestA2UISchemaManager:
    def test_default_init(self) -> None:
        manager = A2UISchemaManager()
        assert manager.protocol_version == "v0.9"
        assert "v0_9" in manager.catalog_id
        assert manager.server_to_client_schema is not None
        assert manager.basic_catalog_schema is not None
        assert manager.common_types_schema is not None

    def test_unsupported_version_raises(self) -> None:
        with pytest.raises(ValueError, match="Unsupported A2UI protocol version"):
            A2UISchemaManager(protocol_version="v0.7")

    def test_custom_catalog_id_from_catalog(self) -> None:
        manager = A2UISchemaManager(custom_catalog={"$id": "https://mycompany.com/custom.json", "components": {}})
        assert manager.catalog_id == "https://mycompany.com/custom.json"

    def test_custom_catalog_without_id_raises(self) -> None:
        with pytest.raises(ValueError, match="Custom catalog must include"):
            A2UISchemaManager(custom_catalog={"components": {}})

    def test_server_to_client_schema_structure(self) -> None:
        manager = A2UISchemaManager()
        schema = manager.server_to_client_schema
        assert schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
        assert "oneOf" in schema
        assert "$defs" in schema
        defs = schema["$defs"]
        assert "CreateSurfaceMessage" in defs
        assert "UpdateComponentsMessage" in defs
        assert "UpdateDataModelMessage" in defs
        assert "DeleteSurfaceMessage" in defs

    def test_basic_catalog_has_components(self) -> None:
        manager = A2UISchemaManager()
        catalog = manager.basic_catalog_schema
        components = catalog.get("components", {})
        assert "Text" in components
        assert "Image" in components
        assert "Button" in components
        assert "Column" in components
        assert "Row" in components

    def test_catalog_rules_loaded(self) -> None:
        manager = A2UISchemaManager()
        rules = manager.catalog_rules
        assert "REQUIRED PROPERTIES" in rules
        assert "Text" in rules

    def test_generate_prompt_section_includes_format(self) -> None:
        manager = A2UISchemaManager()
        prompt = manager.generate_prompt_section()
        assert "A2UI Response Format" in prompt
        assert "v0.9" in prompt
        assert "---a2ui_JSON---" in prompt
        assert "createSurface" in prompt
        assert "updateComponents" in prompt

    def test_generate_prompt_section_includes_components(self) -> None:
        manager = A2UISchemaManager()
        prompt = manager.generate_prompt_section()
        assert "Available Components" in prompt
        assert "Text" in prompt

    def test_generate_prompt_section_includes_rules(self) -> None:
        manager = A2UISchemaManager()
        prompt = manager.generate_prompt_section(include_rules=True)
        assert "Component Rules" in prompt
        assert "REQUIRED PROPERTIES" in prompt

    def test_generate_prompt_section_excludes_rules(self) -> None:
        manager = A2UISchemaManager()
        prompt = manager.generate_prompt_section(include_rules=False)
        assert "Component Rules" not in prompt

    def test_generate_prompt_section_includes_schema(self) -> None:
        manager = A2UISchemaManager()
        prompt = manager.generate_prompt_section(include_schema=True)
        assert "A2UI Message Schema" in prompt
        assert '"$schema"' in prompt

    def test_generate_prompt_section_excludes_schema(self) -> None:
        manager = A2UISchemaManager()
        prompt = manager.generate_prompt_section(include_schema=False)
        assert "A2UI Message Schema" not in prompt

    def test_custom_delimiter_in_prompt(self) -> None:
        manager = A2UISchemaManager()
        prompt = manager.generate_prompt_section(response_delimiter="<<<A2UI>>>")
        assert "<<<A2UI>>>" in prompt
        assert "---a2ui_JSON---" not in prompt

    def test_custom_catalog_file_load_handles_non_utf_default_encoding(self, tmp_path: Path) -> None:
        # Regression for the UTF-8 encoding pins on the open() calls inside
        # A2UISchemaManager. This simulates platforms whose default
        # locale.getencoding() is not UTF-8, notably Windows cp1252 / cp932.
        custom_catalog = {
            "$id": "https://例.com/catalogue.json",
            "components": {
                "Bouton": {
                    "type": "object",
                    "description": "Composant interactif — étiquette: 智能按钮",
                }
            },
        }
        catalog_path = tmp_path / "catalogue.json"
        catalog_path.write_text(json.dumps(custom_catalog, ensure_ascii=False), encoding="utf-8")

        with patch("builtins.open", side_effect=_cp1252_default_open):
            manager = A2UISchemaManager(custom_catalog=str(catalog_path))

        loaded = manager.custom_catalog_schema
        assert loaded is not None
        assert loaded["$id"] == "https://例.com/catalogue.json"
        bouton = loaded["components"]["Bouton"]
        assert bouton["description"] == "Composant interactif — étiquette: 智能按钮"
        assert manager.catalog_id == "https://例.com/catalogue.json"
