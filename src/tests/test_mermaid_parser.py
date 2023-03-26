import ast

import pytest

from src.mermaid_parser.mermaid_parser import MermaidParser


def test_empty_class():
    content = "class MyClass:\n    pass\n"
    parser = MermaidParser()
    parser.parse_classes(content)
    assert "class MyClass" in parser.get_diagram()


def test_class_with_base():
    content = "class DerivedClass(BaseClass):\n    pass\n"
    parser = MermaidParser()
    parser.parse_classes(content)
    diagram = parser.get_diagram()
    assert "class DerivedClass" in diagram
    assert "BaseClass <|-- DerivedClass" in diagram


def test_class_with_methods():
    content = (
        "class MyClass:\n"
        "    def method1(arg1, arg2):\n"
        "        pass\n\n"
        "    def method2() -> str:\n"
        "        pass\n"
    )
    parser = MermaidParser()
    parser.parse_classes(content)
    diagram = parser.get_diagram()
    assert "class MyClass" in diagram
    assert "+method1(arg1, arg2)" in diagram
    assert "+method2() : str" in diagram


def test_full_class():
    content = (
        "class DerivedClass(BaseClass):\n"
        "    prop1 = 1\n\n"
        "    def method1(arg1, arg2):\n"
        "        pass\n\n"
        "    def method2() -> str:\n"
        "        pass\n"
    )
    parser = MermaidParser()
    parser.parse_classes(content)
    diagram = parser.get_diagram()
    assert "class DerivedClass" in diagram
    assert "BaseClass <|-- DerivedClass" in diagram
    assert "+prop1" in diagram
    assert "+method1(arg1, arg2)" in diagram
    assert "+method2() : str" in diagram


def test_class_with_properties():
    content = "class MyClass:\n" "    prop1 = 1\n" "    prop2 = 'string'\n"
    parser = MermaidParser()
    parser.parse_classes(content)
    diagram = parser.get_diagram()
    assert "class MyClass" in diagram
    assert "+prop1" in diagram
    assert "+prop2" in diagram


def test_extract_base_class():
    parser = MermaidParser()
    code = """
class Derived(Base):
    pass
"""
    node = ast.parse(code).body[0]
    assert parser.extract_base_class(node) == "Base"


def test_extract_base_class_no_base():
    parser = MermaidParser()
    code = """
class Simple:
    pass
"""
    node = ast.parse(code).body[0]
    assert parser.extract_base_class(node) is None


def test_process_class_methods():
    parser = MermaidParser()
    code = """
class MyClass:
    def my_method(arg1, arg2):
        pass
"""
    node = ast.parse(code).body[0].body[0]
    parser.process_class_methods(node)
    expected = "    +my_method(arg1, arg2)\n"
    assert expected in parser.class_diagram


def test_process_class_attributes():
    parser = MermaidParser()
    code = """
class MyClass:
    attr1 = 1
    attr2: int
"""
    node1 = ast.parse(code).body[0].body[0]
    node2 = ast.parse(code).body[0].body[1]
    parser.process_class_attributes(node1)
    parser.process_class_attributes(node2)
    expected1 = "    +attr1\n"
    expected2 = "    +attr2\n"
    assert expected1 in parser.class_diagram
    assert expected2 in parser.class_diagram
