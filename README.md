# Mermaid It
Mermaid It is a command-line application that parses software projects and generates Mermaid diagrams from the parsed code base. It is designed to help software developers visualize and understand complex software projects.

## Installation
To install Mermaid It, clone the repository and install the required dependencies:

```bash

git clone https://github.com/fearnworks/mermaidit.git
cd mermaidit
pip install -r requirements.txt
```

## Usage
Mermaid It can be used to generate class diagrams from a Python code base. To generate diagrams, run the following command:

```bash
python run.py --local
```
This will prompt you to select the local directory to analyze. Once selected, Mermaid It will generate a .md file for each Python file in the directory that contains class definitions. The generated files will be saved in the selected directory.

Mermaid It also supports generating diagrams from GitLab repositories. To generate diagrams from a GitLab repository, run the following command:

```bash
python run.py --url <repository_url>

```
This will clone the repository to a local directory and generate the diagrams as described above.

## Supported Diagrams
Mermaid It currently supports generating class diagrams.

## Contributing
If you would like to contribute to Mermaid It, please feel free to submit a pull request. We welcome contributions of all kinds, including bug reports, feature requests, documentation improvements, and code changes.

Before submitting a pull request, please make sure that your code is well-formatted and passes all tests.

## License
Mermaid It is released under the MIT License. See LICENSE for more information.
