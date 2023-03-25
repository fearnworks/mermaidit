import os
import tempfile

from src.code_analyzer.code_analysis import CodeAnalyzer


def test_generate_class_diagram():
    test_dir = os.path.dirname(os.path.realpath(__file__))
    sample_code = os.path.join(test_dir, "sample_code")

    analyzer = CodeAnalyzer(local_path=sample_code)
    file_path = os.path.join(sample_code, "sample_class.py")

    with tempfile.TemporaryDirectory() as temp_output_dir:
        analyzer.output_dir = temp_output_dir
        analyzer.generate_class_diagram(file_path, "sample_class.py")
        output_file_path = os.path.join(temp_output_dir, "sample_class_class.md")

        assert os.path.isfile(output_file_path)


def test_generate_sequence_diagram():
    test_dir = os.path.dirname(os.path.realpath(__file__))
    sample_code = os.path.join(test_dir, "sample_code")

    analyzer = CodeAnalyzer(local_path=sample_code)
    main_file_path = os.path.join(sample_code, "main.py")

    with tempfile.TemporaryDirectory() as temp_output_dir:
        analyzer.output_dir = temp_output_dir
        analyzer.generate_sequence_diagram(main_file_path)
        output_file_path = os.path.join(temp_output_dir, "main_sequence.md")

        assert os.path.isfile(output_file_path)
