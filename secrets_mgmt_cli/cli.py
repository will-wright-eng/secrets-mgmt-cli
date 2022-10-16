import os
import json
import datetime

import click

from .aws import aws
from .config import ConfigHandler, config_handler
from .utils import DateTimeEncoder, ManualEntry, echo_dict

option_secret_name = click.option("-n", "--secret-name", "secret_name", required=True)
option_config = click.option("--config", is_flag=True)


@click.group()
@click.version_option()
def cli():
    "A simple CLI for managing secrets in AWS Secrets Manager"
    pass


# TODO: add common dotfiles to look for and display
@cli.command()
@option_config
def ls(config):
    "[--config compatible] list secrets in AWS Secrets Manager"
    if config:
        config_handler.list_config_dirs()
    else:
        resp = aws.get_secrets_list()
        for secret in resp.get("SecretList"):
            click.echo(f"\n-- {secret.get('Name')} --")
            echo_dict(secret)


@cli.command()
@option_config
@click.option("-s", "--secret-string", "secret_string", help="serialized json", required=False, default=None)
@option_secret_name
def create(secret_string, secret_name, config):
    "[--config compatible] create new secret locally or in aws secrets"
    if secret_string is None:
        click.echo("no secret string provided, please enter json contents")
        entry = ManualEntry()
        secret_string = json.dumps(entry.manual_gen_json())

    if config:
        config_handler = ConfigHandler(project_name=secret_name)
        config_handler.create_config_locally(secret_dict=json.loads(secret_string))
    else:
        aws.create(name=secret_name, secret_value=secret_string)


@cli.command()
@option_config
@option_secret_name
def read(secret_name, config):
    "[--config compatible] read contents of secret, metadata and secret_string"
    if config:
        config_handler.list_config_dirs(secret_name=secret_name)
    else:
        resp = aws.describe(name=secret_name)
        echo_dict(resp)
        value = click.prompt("display secret string? [Y/n]", type=str)
        if value.lower() == "y":
            click.echo(json.dumps(aws.get_value(), indent=4, default=str))


@cli.command(help=aws.put_value.__doc__)
@option_config  # TODO: needd to implement local update method along with manual entry class (as seen in create())
@click.option("-s", "--secret-string", "secret_string", help="serialized json", required=True)
@option_secret_name
def update(secret_string, secret_name, config):
    resp = aws.put_value(secret_value=secret_string, name=secret_name)
    click.echo(resp)


@cli.command()
@option_secret_name
def delete(secret_name):
    "[aws] remove or archive a secret from AWS Secret Manager"
    resp = aws.delete(name=secret_name, without_recovery=False)
    click.echo(resp)


@cli.command()
@click.option("-k", "--key-word", "key_word", required=True)
def search(key_word):
    "[aws] list secrets in AWS Secrets Manager with regex match"
    resp = aws.get_secrets_list()
    for secret in resp.get("SecretList"):
        if key_word in secret.get("Name"):
            click.echo(f"\n-- {secret.get('Name')} --")
            echo_dict(secret)


@cli.command()
@click.option("-n", "--secret-name", "secret_name", required=False, default=None)
@click.option("-p", "--project-name", "project_name", required=True)
def transfer(secret_name: str, project_name: str):
    "[aws -> local] get secret from projects/dev/ and recreate in ~/.config/project_name/config file"
    config_handler = ConfigHandler(project_name=project_name)
    if secret_name is None:
        secrets_prefix = "projects/dev"
        secret_name = os.path.join(secrets_prefix, project_name)
    secret_dict = aws.get_secret(secret_name=secret_name)
    config_handler.create_config_locally(secret_dict)
    return config_handler.print_configs()
