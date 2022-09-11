import os

from setuptools import setup

VERSION = "0.5.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="secrets-mgmt-cli",
    description="A simple CLI for managing secrets in AWS Secrets Manager",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Will Wright",
    url="https://github.com/william-cass-wright/secrets-mgmt-cli",
    project_urls={
        "Issues": "https://github.com/william-cass-wright/secrets-mgmt-cli/issues",
        "CI": "https://github.com/william-cass-wright/secrets-mgmt-cli/actions",
        "Changelog": "https://github.com/william-cass-wright/secrets-mgmt-cli/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["secrets_mgmt_cli"],
    entry_points="""
        [console_scripts]
        smgmt=secrets_mgmt_cli.cli:cli
    """,
    install_requires=["click", "boto3"],
    extras_require={"test": ["pytest"]},
    python_requires=">=3.7",
)
