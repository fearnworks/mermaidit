import ast
import textwrap

import pytest

import src.mermaid_parser as MermaidParser


def test_mermaid_sequence_parser():
    test_results = []

    code = """
class A:
    def method_a(self):
        B().method_b()
class B:
    def method_b(self):
        pass
A().method_a()
"""
    tree = ast.parse(code)
    parser = MermaidParser.MermaidSequenceParser()
    mermaid_code = parser.parse(tree)
    expected_output = ["A ->> method_a: method_a()", "B ->> method_b: method_b()"]
    test_results.append(mermaid_code.split("\n") == expected_output)

    code = """
class X:
    def __init__(self, name):
        self.name = name
    def greet(self):
        print(f"Hello, {self.name}!")
x = X("John")
x.greet()
"""
    tree = ast.parse(code)
    parser = MermaidParser.MermaidSequenceParser()
    mermaid_code = parser.parse(tree)
    expected_output = ["X ->> __init__: __init__()", "X ->> greet: greet()"]
    test_results.append(mermaid_code.split("\n") == expected_output)

    return test_results
