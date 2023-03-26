import argparse
import logging
import os
import shutil

from src.code_analyzer.code_analysis import CodeAnalyzer
from src.file_operations.file_operations import FileOperations


def main():
    """Entry point for the Mermaid diagram generation tool.

    Parses command-line arguments to determine whether to clone a GitLab repository or analyze a local codebase.
    Prompts the user to select an output location for the generated diagrams.
    Creates a CodeAnalyzer object and calls its analyze method to generate the Mermaid diagrams.
    Cleans up the cloned repository (if created) after analysis is complete.
    """
    parser = argparse.ArgumentParser(
        description="Generate Mermaid class diagrams from a Python code base"
    )
    parser.add_argument("--url", help="GitLab repository URL", type=str)
    parser.add_argument(
        "--local", help="Local repository path", type=str, nargs="?", const="BROWSE"
    )
    args = parser.parse_args()

    if args.url and args.local:
        raise ValueError(
            "Please provide either a GitLab repository URL (--url) or a local repository path (--local), but not both."
        )

    if not args.url and not args.local:
        raise ValueError(
            "Please provide either a GitLab repository URL (--url) or a local repository path (--local)."
        )

    if args.url:
        local_path = os.path.join(os.path.abspath("."), "temp_repo")
        FileOperations.clone_repo(args.url, local_path)
    else:
        if args.local == "BROWSE":
            local_path = FileOperations.browse_directory()
        else:
            local_path = args.local

    output_dir = FileOperations.ask_output_location()

    analyzer = CodeAnalyzer(local_path, output_dir)
    analyzer.analyze()

    if args.url:
        # Cleanup cloned repository if created
        shutil.rmtree(local_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
