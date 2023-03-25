import argparse

from code_analysis import analyze_code_base
from file_operations import ask_output_location, browse_directory, clone_repo
from mermaid_parser import MermaidParser


def main():
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
        clone_repo(args.url, local_path)
    else:
        if args.local == "BROWSE":
            local_path = browse_directory()
        else:
            local_path = args.local

    output_dir = ask_output_location()
    analyze_code_base(local_path, output_dir)

    if args.url:
        # Cleanup cloned repository if created
        import shutil

        shutil.rmtree(local_path)


if __name__ == "__main__":
    main()
