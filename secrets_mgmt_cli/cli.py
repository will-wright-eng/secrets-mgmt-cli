import os
import json
import datetime

import click

from .aws import aws
from .config import ConfigHandler, config_handler


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime.datetime):
            return str(z)
        else:
            return super().default(z)


def echo_dict(input_dict: dict):
    for key, val in input_dict.items():
        click.echo(f"{key[:18]+'..' if len(key)>17 else key}{(20-int(len(key)))*'.'}{val}")


@click.group()
@click.version_option()
def cli():
    "A simple CLI for managing secrets in AWS Secrets Manager"
    pass


@cli.command()
@click.option("--config", is_flag=True)
def ls(config):
    "list secrets in AWS Secrets Manager"
    if config:
        config_handler.list_config_dirs()
    else:
        resp = aws.get_secrets_list()
        for secret in resp.get("SecretList"):
            click.echo(f"\n-- {secret.get('Name')} --")
            echo_dict(secret)


@cli.command()
@click.option("--config", is_flag=True)
@click.option("-s", "--secret-string", "secret_string", help="serialized json", required=True)
@click.option("-n", "--secret-name", "secret_name", required=True)
def create(secret_string, secret_name):
    "create new secret"
    if config:
        config_handler.write_config_file_from_dict(config_dict=json.loads(secret_string))
    else:
        aws.create(name=secret_name, secret_value=secret_string)


@cli.command()
@click.option("-n", "--secret-name", "secret_name", required=True)
def read(secret_name):
    "read contents of secret, metadata and secret_string"
    resp = aws.describe(name=secret_name)
    echo_dict(resp)
    value = click.prompt("display secret string? [Y/n]", type=str)
    if value.lower() == "y":
        click.echo(aws.get_value())


@cli.command()
@click.option("-s", "--secret-string", "secret_string", help="serialized json", required=True)
@click.option("-n", "--secret-name", "secret_name", required=True)
def update(secret_string, secret_name):  # , description):
    "change or add the contents of an existing secert"
    resp = aws.put_value(secret_value=secret_string, name=secret_name)
    click.echo(resp)


@cli.command()
@click.option("-n", "--secret-name", "secret_name", required=True)
def delete(secret_name):
    "remove or archive a secret from AWS Secret Manager"
    resp = aws.delete(name=secret_name, without_recovery=False)
    click.echo(resp)


@cli.command()
@click.option("-k", "--key-word", "key_word", required=True)
def search(key_word):
    "list secrets in AWS Secrets Manager with regex match"
    resp = aws.get_secrets_list()
    for secret in resp.get("SecretList"):
        if key_word in secret.get("Name"):
            click.echo(f"\n-- {secret.get('Name')} --")
            echo_dict(secret)


@cli.command()
@click.option("-n", "--secret-name", "secret_name", required=False, default=None)
@click.option("-p", "--project-name", "project_name", required=True)
def transfer(secret_name, project_name):
    config = ConfigHandler(project_name)
    if secret_name is None:
        secrets_prefix = "projects/dev"
        secret_name = os.path.join(secrets_prefix, project_name)
    secret = aws.get_secret(secret_name=secret_name)
    config.write_config_file_from_dict(config_dict=secret)
    return config.print_configs()


cli.add_command(ls)
cli.add_command(create)
cli.add_command(read)
cli.add_command(update)
cli.add_command(delete)
cli.add_command(search)
cli.add_command(transfer)
