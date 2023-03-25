import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

from git import Repo


def browse_directory():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    return directory


def ask_output_location():
    def on_button_click(button_id):
        nonlocal selected_option
        selected_option = button_id
        dialog.destroy()

    dialog = tk.Toplevel()
    dialog.title("Output Location")
    dialog.geometry("350x150")

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

    if selected_option is None:
        raise ValueError("Invalid option selected.")

    if selected_option == 2:
        output_dir = browse_directory()
    elif selected_option == 1:
        output_dir = os.path.join(os.path.abspath("."), "data")
        os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = None

    return output_dir


def clone_repo(repo_url, local_path):
    repo = Repo.clone_from(repo_url, local_path)
    return repo


def wrap_mermaid_code(mermaid_code):
    return f"```mermaid\n{mermaid_code}```\n"
