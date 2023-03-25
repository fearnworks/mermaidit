import os
from unittest.mock import MagicMock, patch

import pytest

from ..file_operations import browse_directory, load_settings, save_settings

DEFAULT_DATA_DIR = os.path.join(os.path.abspath("."), "data")
SETTINGS_FILE = os.path.join(DEFAULT_DATA_DIR, "settings.txt")


def test_browse_directory(tmp_path):
    with patch(
        "src.file_operations.filedialog.askdirectory", return_value=str(tmp_path)
    ):
        result = browse_directory()
        assert result == str(tmp_path)


def test_save_and_load_settings():
    save_settings(1, "/test/output/dir")
    settings = load_settings()
    assert settings["selected_option"] == 1
    assert settings["output_dir"] == "/test/output/dir"
    os.remove(SETTINGS_FILE)  # Cleanup
