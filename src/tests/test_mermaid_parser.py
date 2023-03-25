import pytest

from ..mermaid_parser import MermaidParser


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
        "    def method1(self, arg1, arg2):\n"
        "        pass\n\n"
        "    def method2(self) -> str:\n"
        "        pass\n"
    )
    parser = MermaidParser()
    parser.parse_classes(content)
    diagram = parser.get_diagram()
    assert "class MyClass" in diagram
    assert "+method1(self, arg1, arg2)" in diagram
    assert "+method2(self) : str" in diagram


def test_full_class():
    content = (
        "class DerivedClass(BaseClass):\n"
        "    prop1 = 1\n\n"
        "    def method1(self, arg1, arg2):\n"
        "        pass\n\n"
        "    def method2(self) -> str:\n"
        "        pass\n"
    )
    parser = MermaidParser()
    parser.parse_classes(content)
    diagram = parser.get_diagram()
    assert "class DerivedClass" in diagram
    assert "BaseClass <|-- DerivedClass" in diagram
    assert "+prop1" in diagram
    assert "+method1(self, arg1, arg2)" in diagram
    assert "+method2(self) : str" in diagram


def test_class_with_properties():
    content = "class MyClass:\n" "    prop1 = 1\n" "    prop2 = 'string'\n"
    parser = MermaidParser()
    parser.parse_classes(content)
    diagram = parser.get_diagram()
    assert "class MyClass" in diagram
    assert "+prop1" in diagram
    assert "+prop2" in diagram
