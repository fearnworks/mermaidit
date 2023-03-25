import os

from src.file_operations.file_operations import FileOperations
from src.mermaid_parser.mermaid_parser import MermaidParser


class CodeAnalyzer:
    """A class for analyzing a codebase and generating Mermaid diagrams for class definitions.

    Attributes:
        local_path (str): The path to the codebase to analyze.
        output_dir (str, optional): The directory to save the generated diagrams in.
            If not specified, the diagrams will be saved in the same directory as the source files.
    """

    def __init__(self, local_path, output_dir=None):
        self.local_path = local_path
        self.output_dir = output_dir

    def analyze(self):
        """Analyzes the codebase and generates Mermaid diagrams for class definitions.

        Walks the directory tree rooted at `local_path`, and for each Python file found,
        generates a Mermaid diagram for its class definitions and saves the diagram to
        a corresponding Markdown file.

        Raises:
            UnicodeDecodeError: If a file in the codebase cannot be decoded as UTF-8.
        """
        for root, _, files in os.walk(self.local_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    abs_file_path = os.path.abspath(file_path)
                    print(f"Processing: {abs_file_path}")

                    try:
                        mermaid_parser = MermaidParser()
                        mermaid_parser.parse_file(file_path)
                        mermaid_diagram = mermaid_parser.get_diagram()

                        # Check if the diagram contains any class definitions
                        if "class " not in mermaid_diagram:
                            print(f"No classes found in {file}, skipping.")
                            continue

                        wrapped_mermaid_diagram = FileOperations.wrap_mermaid_code(
                            mermaid_diagram
                        )

                        if self.output_dir:
                            output_file_path = os.path.join(
                                self.output_dir, os.path.splitext(file)[0] + ".md"
                            )
                        else:
                            output_file_path = os.path.splitext(file_path)[0] + ".md"

                        with open(output_file_path, "w") as f:
                            f.write(wrapped_mermaid_diagram)

                        print(f"Mermaid diagram for {file} saved at {output_file_path}")
                    except UnicodeDecodeError as e:
                        print(f"Error processing {abs_file_path}: {e}")
