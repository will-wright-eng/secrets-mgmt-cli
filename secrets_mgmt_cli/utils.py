import os
import json
import datetime as dt

from click import echo


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, dt.datetime):
            return str(z)
        else:
            return super().default(z)


class ManualEntry:
    def __init__(self, secret_string):
        self.secret_string = secret_string

    def manual_gen_json(self):
        field_key = input("field key:")
        field_val = input(f"{field_key} value:")
        self.secret_string[field_key] = field_val
        self.add_fields()
        return self.secret_string

    def add_fields(self):
        resp = input("add field [Y/n]?")
        if resp == "Y":
            return self.manual_gen_json()
        elif resp == "n":
            pass
        else:
            print("invalid response")
            self.add_fields()


def echo_dict(input_dict: dict):
    for key, val in input_dict.items():
        echo(f"{key[:18]+'..' if len(key)>17 else key}{(20-int(len(key)))*'.'}{val}")
