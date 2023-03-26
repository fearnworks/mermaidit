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

    def parse_file(self, file_path: str):
        """
        Parses a Python file for class definitions and updates the class diagram
        with the parsed information.

        Args:
            file_path (str): The path to the Python file to parse.
        """
        with open(file_path, "r") as f:
            content = f.read()
            self.parse_classes(content)

    def parse_classes(self, content: str):
        """
        Parses the content of a class file and builds a Mermaid class diagram.

        Args:
            content (str): The content of the class file to parse.
        """
        tree = ast.parse(content)
        self.logger.debug(f"Parsed AST tree: {tree}")

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                self.logger.debug(f"Found class: {class_name}")

                base_class = self.extract_base_class(node)

                self.class_diagram += f"class {class_name} {{\n"

                for child in ast.iter_child_nodes(node):
                    if isinstance(child, ast.FunctionDef):
                        self.process_class_methods(child)
                    elif isinstance(child, ast.Assign) or isinstance(
                        child, ast.AnnAssign
                    ):
                        self.process_class_attributes(child)

                self.class_diagram += "}\n"

                if base_class:
                    self.class_diagram += f"{base_class} <|-- {class_name}\n"

    def extract_base_class(self, node: ast.ClassDef):
        """Extracts the base class from an AST ClassDef node.

        Args:
            node (ast.ClassDef): The ClassDef node to extract the base class from.

        Returns:
            str or None: The base class name or None if no base class is present.
        """
        base_class = None
        if node.bases:
            base_class = (
                node.bases[0].id if isinstance(node.bases[0], ast.Name) else None
            )
        return base_class

    def process_class_methods(self, child: ast.FunctionDef):
        """Processes class methods and appends them to the class diagram.

        Args:
            child (ast.FunctionDef): The FunctionDef node representing a class method.
        """
        method_name = child.name
        self.logger.debug(f"Found method: {method_name}")

        # Extracting argument types
        params = []
        for arg in child.args.args:
            if arg.arg != "self":
                arg_type = ""
                if arg.annotation:
                    if isinstance(arg.annotation, ast.Name):
                        arg_type = f": {arg.annotation.id}"
                    elif isinstance(arg.annotation, ast.Attribute):
                        arg_type = f": {arg.annotation.value.id}.{arg.annotation.attr}"
                params.append(f"{arg.arg}{arg_type}")

        # Extracting return type
        return_type = None
        if child.returns:
            if isinstance(child.returns, ast.Name):
                return_type = child.returns.id
            elif isinstance(child.returns, ast.Attribute):
                return_type = f"{child.returns.value.id}.{child.returns.attr}"

        params_str = ", ".join(params)
        if return_type:
            self.class_diagram += f"    +{method_name}({params_str}) : {return_type}\n"
        else:
            self.class_diagram += f"    +{method_name}({params_str})\n"

    def process_class_attributes(self, child: ast.Assign or ast.AnnAssign):
        """Processes class attributes and appends them to the class diagram.

        Args:
            child (ast.Assign or ast.AnnAssign): The Assign or AnnAssign node representing a class attribute.
        """
        if isinstance(child, ast.Assign):
            targets = child.targets
        else:
            targets = [child.target]

        for target in targets:
            if isinstance(target, ast.Name):
                attribute_name = target.id
                self.logger.debug(f"Found attribute: {attribute_name}")
                self.class_diagram += f"    +{attribute_name}\n"

    def get_diagram(self):
        """
        Returns the generated class diagram.

        Returns:
            str: The generated class diagram.
        """
        self.logger.debug(f"Generated class diagram: {self.class_diagram}")
        return self.class_diagram
