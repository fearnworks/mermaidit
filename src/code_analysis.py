import os

from file_operations import wrap_mermaid_code
from mermaid_parser import MermaidParser


def analyze_code_base(local_path, output_dir=None):
    for root, _, files in os.walk(local_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                mermaid_parser = MermaidParser()
                mermaid_parser.parse_file(file_path)
                mermaid_diagram = mermaid_parser.get_diagram()
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
