import ast
import logging


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
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

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
        tree = ast.parse(content)
        self.logger.debug(f"Parsed AST tree: {tree}")

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                self.logger.debug(f"Found class: {class_name}")

                base_class = None
                if node.bases:
                    base_class = (
                        node.bases[0].id
                        if isinstance(node.bases[0], ast.Name)
                        else None
                    )
                self.class_diagram += f"class {class_name} {{\n"

                for child in ast.iter_child_nodes(node):
                    if isinstance(child, ast.FunctionDef):
                        method_name = child.name
                        self.logger.debug(f"Found method: {method_name}")

                        params = ", ".join(
                            arg.arg for arg in child.args.args if arg.arg != "self"
                        )
                        return_type = None
                        if child.returns and isinstance(child.returns, ast.Name):
                            return_type = child.returns.id
                        if return_type:
                            self.class_diagram += (
                                f"    +{method_name}({params}) : {return_type}\n"
                            )
                        else:
                            self.class_diagram += f"    +{method_name}({params})\n"

                    elif isinstance(child, ast.Assign) or isinstance(
                        child, ast.AnnAssign
                    ):
                        if isinstance(child, ast.Assign):
                            targets = child.targets
                        else:
                            targets = [child.target]

                        for target in targets:
                            if isinstance(target, ast.Name):
                                attribute_name = target.id
                                self.logger.debug(f"Found attribute: {attribute_name}")
                                self.class_diagram += f"    +{attribute_name}\n"

                self.class_diagram += "}\n"

                if base_class:
                    self.class_diagram += f"{base_class} <|-- {class_name}\n"

    def get_diagram(self):
        """
        Returns the generated class diagram.

        Returns:
            str: The generated class diagram.
        """
        self.logger.debug(f"Generated class diagram: {self.class_diagram}")
        return self.class_diagram
