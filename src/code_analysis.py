import os

from .file_operations import wrap_mermaid_code
from .mermaid_parser import MermaidParser


def analyze_code_base(local_path, output_dir=None):
    for root, _, files in os.walk(local_path):
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

                    wrapped_mermaid_diagram = wrap_mermaid_code(mermaid_diagram)

                    if output_dir:
                        output_file_path = os.path.join(
                            output_dir, os.path.splitext(file)[0] + ".md"
                        )
                    else:
                        output_file_path = os.path.splitext(file_path)[0] + ".md"

                    with open(output_file_path, "w") as f:
                        f.write(wrapped_mermaid_diagram)

                    print(f"Mermaid diagram for {file} saved at {output_file_path}")
                except UnicodeDecodeError as e:
                    print(f"Error processing {abs_file_path}: {e}")
