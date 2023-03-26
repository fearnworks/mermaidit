import ast
import logging
from collections import deque

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

    def add_participants(self):
        for participant in self.participants:
            self.sequence_diagram = (
                f"participant {participant} as {participant}\n" + self.sequence_diagram
            )

    def process_function_calls(self, main_function_node):
        for node in ast.walk(main_function_node):
            if isinstance(node, ast.Call):
                callee = None
                if isinstance(node.func, ast.Name):
                    callee = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    callee = node.func.attr
                if callee is not None:
                    self.participants.add(main_function_node.name)
                    self.participants.add(callee)
                    self.sequence_diagram += (
                        f"    {main_function_node.name} ->>+ {callee}: \n"
                    )

    def parse_file(self, file_path):
        with open(file_path, "r") as f:
            content = f.read()
            return content

    def get_sequence_diagram(self):
        return self.sequence_diagram

    def traverse_calls(self, caller, callees):
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

            self.traverse_calls(function_name, child_callees)

    def parse_main_entrypoint(self, main_file_path):
        with open(main_file_path, "r") as f:
            content = f.read()
            tree = ast.parse(content)

        main_function_node = None

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "main":
                main_function_node = node
                break

        if main_function_node:
            self.traverse_calls(None, [main_function_node])

            self.add_participants()

    def extract_calls(self, node):
        visitor = CallVisitor()
        visitor.visit(node)
        return visitor.calls

    def parse_main_function(self, file_path):
        """Parses the main function in the given Python file for function calls.

        Args:
            file_path (str): The path to the Python file to analyze.
        """
        with open(file_path, "r") as f:
            code = f.read()

        tree = ast.parse(code)
        main_function_node = None

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "main":
                main_function_node = node
                break

        if main_function_node:
            self.process_function_calls(main_function_node)

    def parse_function_calls(self, content, module_name):
        tree = ast.parse(content)

        function_calls = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                callee = None
                if isinstance(node.func, ast.Attribute):
                    callee = node.func.attr
                    if callee is not None:
                        caller_class = None
                        if isinstance(node.func.value, ast.Name):
                            caller_class = node.func.value.id
                        elif isinstance(node.func.value, ast.Attribute):
                            caller_class = node.func.value.attr
                        if caller_class is not None:
                            self.participants.add(caller_class)
                            self.participants.add(callee)
                            self.sequence_diagram += (
                                f"    {caller_class} ->>+ {callee}: \n"
                            )
                            function_calls.append((module_name, callee))
                            self.logger.debug(
                                f"Found function call: {caller_class} -> {callee}"
                            )

        return function_calls


class CallVisitor(ast.NodeVisitor):
    def __init__(self):
        self.calls = []

    def visit_Call(self, node):
        callee = self.get_callee(node.func)
        self.calls.append(callee)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        self.generic_visit(node)

    def get_callee(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self.get_callee(node.value)}.{node.attr}"
        else:
            return "<unknown>"
