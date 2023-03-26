import json
import os

from git import Repo

from src.file_operations.dialog_manager import DialogManager as UI

DEFAULT_DATA_DIR = os.path.join(os.path.abspath("."), "data")
os.makedirs(DEFAULT_DATA_DIR, exist_ok=True)
SETTINGS_FILE = os.path.join(DEFAULT_DATA_DIR, "settings.txt")


class FileOperations:
    @staticmethod
    def browse_directory() -> str:
        """Prompts the user to browse and select a directory.

        Returns:
            str: The path to the selected directory.
        """
        directory = UI.ask_directory()
        return directory

    @staticmethod
    def ask_output_location() -> str:
        """Prompts the user to choose an output location and saves the settings.

        Raises:
            ValueError: If the selected option is invalid.

        Returns:
            str: The path to the output directory.
        """
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
    def clone_repo(repo_url: str, local_path: str) -> Repo:
        """Clones a Git repository to a local path.

        Args:
            repo_url (str): The URL of the Git repository.
            local_path (str): The local path where the repository should be cloned.

        Returns:
            git.Repo: The cloned Git repository.
        """
        repo = Repo.clone_from(repo_url, local_path)
        return repo

    @staticmethod
    def wrap_mermaid_code(mermaid_code: str) -> str:
        """Wraps Mermaid code in Markdown code block syntax.

        Args:
            mermaid_code (str): The Mermaid code.

        Returns:
            str: The Mermaid code wrapped in a Markdown code block.
        """
        return f"```mermaid\n{mermaid_code}```\n"

    @staticmethod
    def save_settings(selected_option, output_dir):
        """Saves the settings to a file.

        Args:
            selected_option (int): The selected output location option.
            output_dir (str): The path to the output directory.
        """
        settings = {"selected_option": selected_option, "output_dir": output_dir}

        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=2)

    @staticmethod
    def load_settings() -> dict:
        """Loads the settings from a file.

        Returns:
            dict: The loaded settings, or None if the settings file does not exist.
        """
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                settings = json.load(f)
            return settings
        return None

    @staticmethod
    def get_src_directory() -> str:
        """Prompts the user to choose between using a previous source directory or browsing a new one.

        Returns:
            str: The path to the selected source directory.
        """
        use_prev_src_dir, prev_src_dir = FileOperations.ask_use_previous_src_dir()
        if use_prev_src_dir:
            return prev_src_dir
        else:
            return FileOperations.browse_directory()

    @staticmethod
    def ask_use_previous_src_dir() -> tuple:
        """Asks the user if they want to use a previously selected source directory.

        Returns:
            tuple: A tuple containing a boolean indicating whether to use the previous directory, and the path to the previous directory or None.
        """
        settings = FileOperations.load_settings()
        if settings:
            message = f"Do you want to use the previously selected source directory:\n\n{settings['output_dir']}\n\nor browse a new one?"
            answer = UI.ask_yes_no("Use previous source directory?", message)
            return answer, settings["output_dir"]
        return False, None
