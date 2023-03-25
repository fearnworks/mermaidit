import json
import os

import pytest
from pytest import MonkeyPatch as monkeypatch

from src.file_operations.dialog_manager import DialogManager as UI
from src.file_operations.file_operations import FileOperations


def test_wrap_mermaid_code():
    mermaid_code = "graph TD;\nA-->B;"
    wrapped_code = FileOperations.wrap_mermaid_code(mermaid_code)
    expected_output = "```mermaid\ngraph TD;\nA-->B;```\n"
    assert wrapped_code == expected_output


def test_save_and_load_settings(tmpdir, monkeypatch):
    settings_file = tmpdir.join("settings.txt")
    monkeypatch.setattr(
        "src.file_operations.file_operations.SETTINGS_FILE", str(settings_file)
    )

    selected_option = 1
    output_dir = os.path.abspath(".")
    FileOperations.save_settings(selected_option, output_dir)

    settings = FileOperations.load_settings()
    assert settings is not None
    assert settings["selected_option"] == selected_option
    assert settings["output_dir"] == output_dir


def test_load_settings_file_not_exist(tmpdir, monkeypatch):
    settings_file = tmpdir.join("nonexistent_settings.txt")
    monkeypatch.setattr(
        "src.file_operations.file_operations.SETTINGS_FILE", str(settings_file)
    )

    settings = FileOperations.load_settings()
    assert settings is None


def test_ask_use_previous_src_dir_yes(monkeypatch):
    monkeypatch.setattr(
        FileOperations, "load_settings", lambda: {"output_dir": "/dummy/path"}
    )
    monkeypatch.setattr(UI, "ask_yes_no", lambda title, message: True)

    use_prev, src_dir = FileOperations.ask_use_previous_src_dir()
    assert use_prev is True
    assert src_dir == "/dummy/path"


def test_ask_use_previous_src_dir_no(monkeypatch):
    monkeypatch.setattr(
        FileOperations, "load_settings", lambda: {"output_dir": "/dummy/path"}
    )
    monkeypatch.setattr(UI, "ask_yes_no", lambda title, message: False)

    use_prev, src_dir = FileOperations.ask_use_previous_src_dir()
    assert use_prev is False
    assert src_dir == "/dummy/path"


def test_ask_use_previous_src_dir_no_settings(monkeypatch):
    monkeypatch.setattr(FileOperations, "load_settings", lambda: None)

    use_prev, src_dir = FileOperations.ask_use_previous_src_dir()
    assert use_prev is False
    assert src_dir is None
