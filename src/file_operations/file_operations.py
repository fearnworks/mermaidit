import json
import os

from git import Repo

from src.file_operations.dialog_manager import DialogManager as UI

DEFAULT_DATA_DIR = os.path.join(os.path.abspath("."), "data")
os.makedirs(DEFAULT_DATA_DIR, exist_ok=True)
SETTINGS_FILE = os.path.join(DEFAULT_DATA_DIR, "settings.txt")


class FileOperations:
    @staticmethod
    def browse_directory():
        directory = UI.ask_directory()
        return directory

    @staticmethod
    def ask_output_location():
        selected_option = UI.ask_output_location()

        if selected_option is None:
            raise ValueError("Invalid option selected.")

        if selected_option == 2:
            output_dir = FileOperations.browse_directory()
        elif selected_option == 1:
            output_dir = os.path.join(os.path.abspath("."), "data")
            os.makedirs(output_dir, exist_ok=True)
        else:
            output_dir = None

        FileOperations.save_settings(selected_option, output_dir)
        return output_dir

    @staticmethod
    def clone_repo(repo_url, local_path):
        repo = Repo.clone_from(repo_url, local_path)
        return repo

    @staticmethod
    def wrap_mermaid_code(mermaid_code):
        return f"```mermaid\n{mermaid_code}```\n"

    @staticmethod
    def save_settings(selected_option, output_dir):
        settings = {"selected_option": selected_option, "output_dir": output_dir}

        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=2)

    @staticmethod
    def load_settings():
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                settings = json.load(f)
            return settings
        return None

    @staticmethod
    def get_src_directory():
        use_prev_src_dir, prev_src_dir = FileOperations.ask_use_previous_src_dir()
        if use_prev_src_dir:
            return prev_src_dir
        else:
            return FileOperations.browse_directory()

    @staticmethod
    def ask_use_previous_src_dir():
        settings = FileOperations.load_settings()
        if settings:
            message = f"Do you want to use the previously selected source directory:\n\n{settings['output_dir']}\n\nor browse a new one?"
            answer = UI.ask_yes_no("Use previous source directory?", message)
            return answer, settings["output_dir"]
        return False, None
