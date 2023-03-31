import ast
import logging
import os

from src.file_operations.file_operations import FileOperations
from src.mermaid_parser.mermaid_parser import MermaidParser
from src.mermaid_parser.mermaid_sequence_parser import MermaidSequenceParser


class CodeAnalyzer:

    """A class for analyzing a codebase and generating Mermaid diagrams for class definitions and sequence diagrams.

    Attributes:
        logger (logging.Logger): The logger for the `CodeAnalyzer` class.
        local_path (str): The path to the codebase to analyze.
        output_dir (str, optional): The directory to save the generated diagrams in.
            If not specified, the diagrams will be saved in the same directory as the source files.
    """

    logger: logging.Logger
    output_dir: str
    local_path: str

    def __init__(self, local_path: str, output_dir: str = None):
        self.local_path = local_path
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def analyze(self):
        """Analyzes the codebase and generates Mermaid diagrams for class definitions and sequence diagrams.

        Walks the directory tree rooted at `local_path`, and for each Python file found,
        generates a Mermaid diagram for its class definitions and a sequence diagram,
        then saves the diagrams to corresponding Markdown files.

        Raises:
            UnicodeDecodeError: If a file in the codebase cannot be decoded as UTF-8.
        """
        for root, _, files in os.walk(self.local_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    abs_file_path = os.path.abspath(file_path)
                    print(f"Processing: {abs_file_path}")

                    self.generate_class_diagram(file_path, file)
                    self.generate_sequence_diagram(file_path)

    def generate_class_diagram(self, file_path: str, file: str):
        """Generates a Mermaid class diagram for the given file.

        Args:
            file_path (str): The path to the Python file to analyze.
            file (str): The name of the Python file.
        """
        mermaid_parser = MermaidParser()
        mermaid_parser.parse_file(file_path)
        mermaid_diagram = mermaid_parser.get_diagram()

        if "class " not in mermaid_diagram:
            print(f"No classes found in {file}, skipping.")
            return

        wrapped_mermaid_diagram = FileOperations.wrap_mermaid_code(mermaid_diagram)

        if self.output_dir:
            output_file_path = os.path.join(
                self.output_dir,
                os.path.splitext(file)[0] + "_class.md",
            )
        else:
            output_file_path = os.path.splitext(file_path)[0] + "_class.md"

        with open(output_file_path, "w") as f:
            f.write(wrapped_mermaid_diagram)

        print(f"Mermaid class diagram for {file} saved at {output_file_path}")

    def generate_sequence_diagram(self, file_path: str):
        """Generates a Mermaid sequence diagram for the given file.

        Args:
            file_path (str): The path to the Python file to analyze.
        """
        if os.path.basename(file_path) == "main.py":
            # Create an instance of the MermaidSequenceParser class
            mermaid_sequence_parser = MermaidSequenceParser()
            self.logger.debug(f"Generating sequence diagram for {file_path}")

            # Parse the code into an abstract syntax tree (AST)
            with open(file_path, "r", encoding="utf-8") as file:
                code = file.read()
                tree = ast.parse(code)

            # Use the parser to generate the mermaid sequence diagram
            mermaid_sequence_diagram = mermaid_sequence_parser.parse(tree)
            self.logger.debug(f"Sequence diagram generated for {file_path}")

            if mermaid_sequence_diagram.strip() == "":
                print(
                    f"No function calls found in {os.path.basename(file_path)}, skipping."
                )
                return

            wrapped_sequence_diagram = FileOperations.wrap_mermaid_code(
                mermaid_sequence_diagram
            )

            if self.output_dir:
                output_file_path = os.path.join(
                    self.output_dir,
                    os.path.splitext(os.path.basename(file_path))[0] + "_sequence.md",
                )
            else:
                output_file_path = os.path.splitext(file_path)[0] + "_sequence.md"

            with open(output_file_path, "w") as f:
                f.write(wrapped_sequence_diagram)

            print(
                f"Mermaid sequence diagram for {os.path.basename(file_path)} saved at {output_file_path}"
            )
