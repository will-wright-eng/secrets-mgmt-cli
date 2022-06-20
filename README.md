# secrets-mgmt-cli

[![PyPI](https://img.shields.io/pypi/v/secrets-mgmt-cli.svg)](https://pypi.org/project/secrets-mgmt-cli/)
[![Changelog](https://img.shields.io/github/v/release/william-cass-wright/secrets-mgmt-cli?include_prereleases&label=changelog)](https://github.com/william-cass-wright/secrets-mgmt-cli/releases)
[![Tests](https://github.com/william-cass-wright/secrets-mgmt-cli/workflows/Test/badge.svg)](https://github.com/william-cass-wright/secrets-mgmt-cli/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/william-cass-wright/secrets-mgmt-cli/blob/master/LICENSE)

- A simple CLI for managing secrets in AWS Secrets Manager
- [PyPI project](https://pypi.org/project/secrets-mgmt-cli/)
- Based on cookiecutter template [simonw/click-app](https://github.com/simonw/click-app)

## Installation
Install this tool using `pip`:
```bash
pip install secrets-mgmt-cli
```

## Usage
For help, run:
```bash
secrets-mgmt-cli --help
```
You can also use:
```bash
python -m secrets_mgmt_cli --help
```

## Development
To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd secrets-mgmt-cli
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
