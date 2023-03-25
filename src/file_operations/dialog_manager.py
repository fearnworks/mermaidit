import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class DialogManager:
    """
    DialogManager class is responsible for managing and displaying
    dialogs and messages related to file operations.
    """

    @staticmethod
    def ask_directory():
        """
        Opens a dialog for selecting a directory and returns the selected directory.

        Returns:
            str: The selected directory path.
        """
        root = tk.Tk()
        root.withdraw()
        directory = filedialog.askdirectory()
        return directory

    @staticmethod
    def ask_output_location():
        """
        Opens a dialog to ask for the output location for diagrams.

        Returns:
            int: The selected option index (0: source directory, 1: default data directory, 2: custom directory).
        """

        def on_button_click(button_id):
            nonlocal selected_option
            selected_option = button_id
            dialog.destroy()

        dialog = tk.Toplevel()
        dialog.title("Output Location")
        dialog.geometry("350x250")

        label = tk.Label(dialog, text="Where would you like to save the diagrams?")
        label.pack(pady=10)

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        options = [
            "Source directory",
            "Default data directory (./data)",
            "Custom directory",
        ]

        selected_option = None

        for idx, option in enumerate(options):
            button = ttk.Button(
                button_frame, text=option, command=lambda i=idx: on_button_click(i)
            )
            button.grid(row=0, column=idx, padx=10)

        dialog.lift()
        dialog.attributes("-topmost", True)
        dialog.grab_set()
        dialog.wait_window()

        return selected_option

    @staticmethod
    def ask_yes_no(title, message):
        """
        Displays a Yes/No messagebox with the given title and message.

        Args:
            title (str): The title of the messagebox.
            message (str): The message displayed in the messagebox.

        Returns:
            bool: True if Yes is selected, False if No is selected.
        """
        answer = messagebox.askyesno(title, message)
        return answer
