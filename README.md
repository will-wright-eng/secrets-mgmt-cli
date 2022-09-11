# secrets-mgmt-cli

[![PyPI](https://img.shields.io/pypi/v/secrets-mgmt-cli.svg)](https://pypi.org/project/secrets-mgmt-cli/)
[![Changelog](https://img.shields.io/github/v/release/william-cass-wright/secrets-mgmt-cli?include_prereleases&label=changelog)](https://github.com/william-cass-wright/secrets-mgmt-cli/releases)
[![Tests](https://github.com/william-cass-wright/secrets-mgmt-cli/workflows/Test/badge.svg)](https://github.com/william-cass-wright/secrets-mgmt-cli/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/william-cass-wright/secrets-mgmt-cli/blob/master/LICENSE)

## Summary

- A simple CLI for managing secrets in AWS Secrets Manager
- [PyPI project][2]
- Based on the following projects: 
	- cookiecutter template [simonw/click-app][3]
	- AWS code sample [secretsmanager_basics.py][1]

[1]: https://docs.aws.amazon.com/code-samples/latest/catalog/python-secretsmanager-secretsmanager_basics.py.html
[2]: https://pypi.org/project/secrets-mgmt-cli/
[3]: https://github.com/simonw/click-app

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

## new release
- change version in `setup.py`
- use `lint` and `test` labels in PR to pre-run components of publish workflow
