import json
import os
from unittest.mock import MagicMock, patch

import pytest

from ..file_operations import (
    ask_output_location,
    ask_use_previous_src_dir,
    browse_directory,
    get_src_directory,
    load_settings,
    save_settings,
)

DEFAULT_DATA_DIR = os.path.join(os.path.abspath("."), "data")
SETTINGS_FILE = os.path.join(DEFAULT_DATA_DIR, "settings.txt")


def test_browse_directory():
    with patch(
        "src.file_operations.filedialog.askdirectory", return_value="/some/directory"
    ):
        result = browse_directory()
        assert result == "/some/directory"


def test_save_and_load_settings():
    save_settings(1, "/test/output/dir")
    settings = load_settings()
    assert settings["selected_option"] == 1
    assert settings["output_dir"] == "/test/output/dir"
    os.remove(SETTINGS_FILE)  # Cleanup


def test_ask_use_previous_src_dir():
    save_settings(1, "/test/output/dir")

    with patch("src.file_operations.messagebox.askyesno", return_value=True):
        use_prev_src_dir, prev_src_dir = ask_use_previous_src_dir()
        assert use_prev_src_dir
        assert prev_src_dir == "/test/output/dir"

    os.remove(SETTINGS_FILE)  # Cleanup


def test_get_src_directory_use_previous():
    save_settings(1, "/test/output/dir")

    with patch("src.file_operations.messagebox.askyesno", return_value=True):
        with patch("src.file_operations.browse_directory") as mock_browse_directory:
            src_dir = get_src_directory()
            assert src_dir == "/test/output/dir"
            mock_browse_directory.assert_not_called()

    os.remove(SETTINGS_FILE)  # Cleanup


def test_get_src_directory_browse_new():
    save_settings(1, "/test/output/dir")

    with patch("src.file_operations.messagebox.askyesno", return_value=False):
        with patch(
            "src.file_operations.browse_directory", return_value="/new/directory"
        ):
            src_dir = get_src_directory()
            assert src_dir == "/new/directory"

    os.remove(SETTINGS_FILE)  # Cleanup
