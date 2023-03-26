```mermaid
classDiagram
class MermaidParser {
    +__init__()
    +parse_file(file_path: str)
    +parse_classes(content: str)
    +extract_base_class(node: ast.ClassDef)
    +process_class_methods(child: ast.FunctionDef)
    +process_class_attributes(child)
    +get_diagram()
}
```
