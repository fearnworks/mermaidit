import re


class MermaidParser:
    """
    A parser for extracting class definitions from Python code and generating
    Mermaid diagrams from them.
    """

    def __init__(self):
        """
        Initializes the `MermaidParser` object with an empty class diagram.
        """
        self.class_diagram = "classDiagram\n"

    def parse_file(self, file_path):
        """
        Parses a Python file for class definitions and updates the class diagram
        with the parsed information.

        Args:
            file_path (str): The path to the Python file to parse.
        """
        with open(file_path, "r") as f:
            content = f.read()
            self.parse_classes(content)

    def parse_classes(self, content):
        """
        Parses a string for class definitions and updates the class diagram with
        the parsed information.

        Args:
            content (str): The content to parse for class definitions.
        """
        class_definitions = re.findall(
            r"^class\s+(\w+)(\s*\((\w+)\))?:", content, re.MULTILINE
        )

        for class_def in class_definitions:
            class_name, _, base_class = class_def
            self.class_diagram += f"class {class_name} {{\n"

            methods = re.findall(
                r"^\s+def\s+(\w+)\s*\((.*?)\)(\s*->\s*(\w+))?:", content, re.MULTILINE
            )
            for method in methods:
                method_name, params, _, return_type = method
                if return_type:
                    self.class_diagram += (
                        f"    +{method_name}({params}) : {return_type}\n"
                    )
                else:
                    self.class_diagram += f"    +{method_name}({params})\n"

            properties = re.findall(r"^\s+([a-zA-Z_]\w+)\s*=", content, re.MULTILINE)
            for prop in properties:
                self.class_diagram += f"    +{prop}\n"

            self.class_diagram += "}\n"

            if base_class:
                self.class_diagram += f"{base_class} <|-- {class_name}\n"

    def get_diagram(self):
        """
        Returns the generated class diagram.

        Returns:
            str: The generated class diagram.
        """
        return self.class_diagram
