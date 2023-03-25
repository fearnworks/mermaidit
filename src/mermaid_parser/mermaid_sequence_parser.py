import ast
import inspect
import os
import re
from collections import deque

from src.mermaid_parser.mermaid_parser import MermaidParser


class MermaidSequenceParser(MermaidParser):
    def __init__(self):
        super().__init__()
        self.sequence_diagram = "sequenceDiagram\n"
        self.participants = set()
        self.visited = set()

    def add_participants(self):
        for participant in self.participants:
            self.sequence_diagram = (
                f"participant {participant} as {participant}\n" + self.sequence_diagram
            )

    def parse_function_calls(self, content, caller):
        function_calls = re.findall(r"\b(\w+)\s*\(", content)
        return [(caller, callee) for callee in function_calls]

    def parse_file(self, file_path):
        with open(file_path, "r") as f:
            content = f.read()
            return content

    def get_sequence_diagram(self):
        return self.sequence_diagram

    def traverse_calls(self, entry_module):
        queue = deque([(None, entry_module)])

        while queue:
            caller, callee = queue.popleft()

            if callee in self.visited:
                continue

            self.visited.add(callee)

            if caller:
                self.participants.add(caller)
                self.participants.add(callee)
                self.sequence_diagram += f"    {caller} ->>+ {callee}: \n"

            try:
                callee_module = __import__(callee)
                source_file = inspect.getsourcefile(callee_module)
                content = self.parse_file(source_file)
                function_calls = self.parse_function_calls(content, callee)
                queue.extend(function_calls)
            except (ModuleNotFoundError, ImportError, TypeError):
                continue

    def parse_main_entrypoint(self, main_file_path):
        with open(main_file_path, "r") as f:
            content = f.read()
            entry_module = re.search(r"(\w+)\.main\(\)", content)

            if entry_module:
                entry_module = entry_module.group(1)
                self.traverse_calls(entry_module)

        self.add_participants()

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
            self.traverse_calls(main_function_node)
