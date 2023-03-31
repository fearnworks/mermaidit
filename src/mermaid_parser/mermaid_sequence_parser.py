import ast
import logging
from collections import deque
from typing import Callable, Dict, List, Tuple

from src.mermaid_parser.mermaid_parser import MermaidParser


class MermaidSequenceParser(ast.NodeVisitor):
    """Mermaid Sequence Diagram Parser.

    This class is responsible for parsing Python code and generating Mermaid
    sequence diagrams.

    Attributes:
        _output_lines (List[str]): List of lines to be included in the sequence diagram.
        _object_instances (Dict): Dictionary to track object instances.
        _caller_stack (List[str]): Stack to track current caller in nested calls.
        _context_stack (List[str]): Stack to track current context (e.g., route or function).
        virtual_participant (str): Virtual participant representing an external actor.
    """

    def __init__(self):
        self._output_lines = []
        self._object_instances = {}
        self._caller_stack = []
        self._context_stack = []
        self.virtual_participant = "User"

    def parse(self, node: ast.AST) -> str:
        """Parse the abstract syntax tree and generate the Mermaid sequence diagram code.

        Args:
            node (ast.AST): The root node of the abstract syntax tree.

        Returns:
            str: The Mermaid code representing the sequence diagram.
        """
        self.visit(node)
        indented_output_lines = ["    " + line for line in self._output_lines]
        return "sequenceDiagram\n" + "\n".join(indented_output_lines)

    def _get_caller(self):
        """Get the current caller from the caller stack.

        Returns:
            str: The current caller, if available; otherwise, None.
        """
        return self._caller_stack[-1] if self._caller_stack else None

    def _get_context(self):
        """Get the current context from the context stack.

        Returns:
            str: The current context, if available; otherwise, None.
        """
        return self._context_stack[-1] if self._context_stack else None

    def visit_Call(self, node: ast.Call):
        """Visit Call nodes in the abstract syntax tree.

        Args:
            node (ast.Call): The Call node to visit.
        """
        caller = self._get_caller() or self._get_context() or self.virtual_participant
        callee = None
        instance_name = None  # Initialize instance_name to None

        # Handle object creation and constructor calls
        if isinstance(node.func, ast.Name) and node.func.id in self._object_instances:
            instance_name = node.func.id
            callee = "__init__"
        elif isinstance(node.func, ast.Attribute):
            # Handle method calls on object instances
            if (
                isinstance(node.func.value, ast.Name)
                and node.func.value.id in self._object_instances
            ):
                instance_name = self._object_instances[node.func.value.id]
                callee = node.func.attr

        if instance_name and callee:
            if caller:
                self._output_lines.append(f"{caller} ->> {instance_name}: {callee}()")
            else:
                self._output_lines.append(f"{instance_name}: {callee}()")

        self._caller_stack.append(instance_name)
        self.generic_visit(node)
        self._caller_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visit FunctionDef nodes in the abstract syntax tree.

        Args:
            node (ast.FunctionDef): The FunctionDef node to visit.
        """
        func_name = node.name
        # Include the current function as a participant in the diagram
        self._output_lines.append(f"participant {func_name}")
        self._context_stack.append(func_name)
        self.generic_visit(node)
        self._context_stack.pop()

    def visit_Assign(self, node: ast.Assign):
        """Visit Assign nodes in the abstract syntax tree.

        Args:
            node (ast.Assign): The Assign node to visit.
        """
        # Capture object instance creation
        for target in node.targets:
            if isinstance(target, ast.Name) and isinstance(node.value, ast.Call):
                if hasattr(node.value.func, "id"):
                    self._object_instances[target.id] = node.value.func.id
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visit FunctionDef nodes in the abstract syntax tree.

        Args:
            node (ast.ClassDef): The ClassDef node to visit.
        """
        func_name = node.name
        self._context_stack.append(func_name)
        self.generic_visit(node)
        self._context_stack.pop()

    def visit_ClassDef(self, node: ast.ClassDef):
        """Visit ClassDef nodes in the abstract syntax tree.

        Args:
            node (ast.ClassDef): The ClassDef node to visit.
        """
        self._context_stack.append(node.name)
        self.generic_visit(node)
        self._context_stack.pop()

    def generic_visit(self, node: ast.AST):
        """Generic visitor for all other nodes in the abstract syntax tree.

        Args:
            node (ast.AST): The AST node to visit.
        """
        super().generic_visit(node)
