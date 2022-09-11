"""
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html

# aws = AwsSecretMgmt()
# secret_name = "test/test_secret"
# secret = aws.get_secret(secret_name)

# secret_name = 'test/test_secret_2'
# secret_string = json.dumps(secret)
# aws.create_secret(secret_string,secret_name)

## write aws secrets to local
"""

from .aws import AwsSecretMgmt
from .config import ConfigHandler

aws = AwsSecretMgmt()


def write_secret_to_local_config(project_name):
    config = ConfigHandler(project_name)
    secrets_prefix = "projects/dev"
    secret = aws.get_secret(os.path.join(secrets_prefix, project_name))
    config.write_config_file_from_dict(config_dict=secret)
    return config.print_configs()


# for project_name in projects:
#     write_secret_to_local_config(project_name)


def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result


def create_res_dict_from_envrc():
    files = find_all(".envrc", "../.")
    projects = ["media_mgmt_cli", "twl_app"]
    res = {}
    for file_path, project_name in zip(files, projects):
        tmp_res = {}
        with open(file_path, "r") as file:
            tmp_lines = file.readlines()
            for pos, line in enumerate(tmp_lines):
                tmp_var = line.replace("\n", "").replace("export ", "").split("=")
                if "KEY" in tmp_var[0]:
                    pass
                else:
                    tmp_res[tmp_var[0]] = tmp_var[1]
        res[project_name] = tmp_res
    return res


def create_secret_from_dict(project_name, secrets_dict):
    secrets_prefix = "projects/dev"
    secret_name = os.path.join(secrets_prefix, project_name)
    secret_string = json.dumps(secrets_dict)
    return aws.create_secret(secret_string, secret_name)
