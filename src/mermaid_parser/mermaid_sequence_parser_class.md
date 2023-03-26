```mermaid
classDiagram
class MermaidSequenceParser {
    +logger
    +sequence_diagram
    +visited
    +participants
    +__init__()
    +add_participants()
    +process_function_calls(main_function_node)
    +parse_file(file_path)
    +get_sequence_diagram()
    +traverse_calls(caller, callees)
    +parse_main_entrypoint(main_file_path)
    +extract_calls(node)
    +parse_main_function(file_path)
    +parse_function_calls(content, module_name)
}
MermaidParser <|-- MermaidSequenceParser
class CallVisitor {
    +__init__()
    +visit_Call(node)
    +visit_Attribute(node)
    +get_callee(node)
}
```
