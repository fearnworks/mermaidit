import re


class MermaidParser:
    def __init__(self):
        self.class_diagram = "classDiagram\n"

    def parse_file(self, file_path):
        with open(file_path, "r") as f:
            content = f.read()
            self.parse_classes(content)

    def parse_classes(self, content):
        class_definitions = re.findall(
            r"^class\s+(\w+)(\s*\((\w+)\))?:", content, re.MULTILINE
        )

        for class_def in class_definitions:
            class_name, _, base_class = class_def
            if base_class:
                self.class_diagram += f"{base_class} <|-- {class_name}\n"

    def get_diagram(self):
        return self.class_diagram
