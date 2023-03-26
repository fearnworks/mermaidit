import ast
import logging
from collections import deque
from typing import Callable, Dict, List, Tuple

from src.mermaid_parser.mermaid_parser import MermaidParser


class MermaidSequenceParser(MermaidParser):
    logger: logging.Logger
    sequence_diagram: str
    visited: set
    participants: set

    def __init__(self):
        super().__init__()
        self.sequence_diagram = "sequenceDiagram\n"
        self.participants = set()
        self.visited = set()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG)

    def add_participants(self) -> None:
        """
        Adds the sequence diagram participants to the diagram.
        """
        for participant in self.participants:
            self.sequence_diagram = (
                f"participant {participant} as {participant}\n" + self.sequence_diagram
            )

    def process_function_calls(
        self, caller_name: str, caller_node: ast.AST, imports: Dict[str, str]
    ) -> None:
        """
        Processes the function calls in the given caller_node and updates the sequence diagram.

        Args:
            caller_name (str): The name of the caller.
            caller_node (ast.AST): The AST node of the caller.
            imports (Dict[str, str]): The imported modules in the Python file.
        """
        for node in ast.walk(caller_node):
            if isinstance(node, ast.Call):
                callee = self.get_callee(node.func, imports)
                if callee is not None:
                    self.participants.add(caller_name)
                    self.participants.add(callee)
                    self.sequence_diagram += f"    {caller_name} ->>+ {callee}: {callee}({', '.join([ast.dump(arg) for arg in node.args])})\n"

    def process_branches(
        self, caller_name: str, main_function_node: ast.AST, imports: Dict[str, str]
    ) -> None:
        """
        Processes the branches in the main function node and updates the sequence diagram.

        Args:
            caller_name (str): The name of the caller.
            main_function_node (ast.AST): The main function node of the Python file.
            imports (Dict[str, str]): The imported modules in the Python file.
        """
        for node in ast.walk(main_function_node):
            if isinstance(node, (ast.If, ast.For, ast.While)):
                self.process_function_calls(caller_name, node, imports)
                if hasattr(node, "body"):
                    for body_node in node.body:
                        self.process_branches(caller_name, body_node, imports)
                if hasattr(node, "orelse"):
                    for orelse_node in node.orelse:
                        self.process_branches(caller_name, orelse_node, imports)

    def parse_file(
        self, file_path: str, imports=None
    ) -> Tuple[ast.AST, Dict[str, str]]:
        """
        Parses a Python file and returns the AST and a dictionary of imported module names and aliases.

        Args:
            file_path (str): The path to the Python file to parse.

        Returns:
            tuple: A tuple containing the AST of the parsed file and a dictionary of imported module names and aliases.
        """
        if imports is None:
            imports = {}

        with open(file_path, "r") as f:
            content = f.read()
            tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports[alias.asname or alias.name] = alias.name
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imports[alias.asname or alias.name] = f"{node.module}.{alias.name}"

        return tree, imports

    def get_sequence_diagram(self):
        return self.sequence_diagram

    def traverse_calls(
        self, caller: str, nodes: List[ast.AST], imports: Dict[str, str]
    ):
        """
        Traverses a list of AST nodes representing function calls and adds them to the sequence diagram.

        Args:
            caller (str): The name of the calling function or class.
            nodes (List[ast.AST]): A list of AST nodes representing function calls.
            imports (Dict[str, str]): A dictionary of imported module names and aliases.
        """
        for callee in callees:
            self.logger.debug(f"Processing: {caller}, {callee}")

            if isinstance(callee, ast.FunctionDef):
                function_name = callee.name
            elif isinstance(callee, ast.Name):
                function_name = callee.id
            elif isinstance(callee, ast.Attribute):
                function_name = callee.attr
            else:
                continue

            if function_name in self.visited:
                self.logger.debug(f"Skipping {function_name} (already visited)")
                continue

            self.visited.add(function_name)

            if caller:
                self.participants.add(caller)
                self.participants.add(function_name)
                self.sequence_diagram += f"    {caller} ->>+ {function_name}: \n"

            child_callees = self.extract_calls(callee)

            for child_callee in child_callees:
                self.logger.debug(f"Child callee: {child_callee}")

            self.traverse_calls(function_name, child_callees, imports)

    def parse_main_entrypoint(self, main_file_path: str):
        """
        Parses the main entry point of a Python project.

        Args:
            main_file_path (str): The path to the main entry point file.
        """
        tree, imports = self.parse_file(main_file_path)

        main_function_node = None

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "main":
                main_function_node = node
                break

        if main_function_node:
            self.traverse_calls(None, [main_function_node], imports)

        self.add_participants()

    def extract_calls(self, node):
        visitor = CallVisitor(self.get_callee)
        visitor.visit(node)
        return visitor.calls

    def parse_main_function(self, file_path):
        """Parses the main function in the given Python file for function calls.

        Args:
            file_path (str): The path to the Python file to analyze.
        """
        tree, imports = self.parse_file(file_path)

        main_function_node = None

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "main":
                main_function_node = node
                break

        if main_function_node:
            self.process_function_calls(
                main_function_node.name, main_function_node, imports
            )
            self.process_branches(main_function_node.name, main_function_node, imports)

    def get_callee(self, node, imports):
        if isinstance(node, ast.Name):
            return imports.get(node.id, node.id)
        elif isinstance(node, ast.Attribute):
            return f"{self.get_callee(node.value, imports)}.{node.attr}"
        else:
            return "<unknown>"


class CallVisitor(ast.NodeVisitor):
    """A class for visiting function call nodes in an AST."""

    def __init__(self, get_callee_fn: Callable[[ast.AST], str]):
        """
        Initialize a new CallVisitor.

        Args:
            get_callee_fn: A function that takes an AST node as input and returns the name
                of the function being called (as a string).
        """
        self.calls: List[str] = []
        self.get_callee_fn = get_callee_fn

    def visit_Call(self, node: ast.Call):
        """
        Visit a Call node in the AST.

        This method extracts the name of the function being called and adds it to the list
        of calls.

        Args:
            node: The Call node to visit.
        """
        callee = self.get_callee_fn(node.func)
        self.calls.append(callee)
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        """
        Visit an Attribute node in the AST.

        This method visits the children of the Attribute node.

        Args:
            node: The Attribute node to visit.
        """
        self.generic_visit(node)
