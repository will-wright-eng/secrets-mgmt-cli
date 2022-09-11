"""
TODO
- test boto3 control flows with stubber
- https://botocore.amazonaws.com/v1/documentation/api/latest/reference/stubber.html
"""

import json
import datetime
from pathlib import Path

import botocore.session
from dateutil.tz import tzlocal
from botocore.stub import Stubber
from click.testing import CliRunner
from secrets_mgmt_cli.aws import aws
from secrets_mgmt_cli.cli import cli

smgmt_ls_resp = {
    "SecretList": [
        {
            "ARN": "arn:aws:secretsmanager:us-west-1:582406646515:secret:test/test_secret-q6V0kt",
            "Name": "test/test_secret",
            "Description": "test secret",
            "LastChangedDate": datetime.datetime(2022, 6, 13, 23, 4, 0, 566000, tzinfo=tzlocal()),
            "LastAccessedDate": datetime.datetime(2022, 6, 13, 17, 0, tzinfo=tzlocal()),
            "Tags": [{"Key": "test", "Value": "test"}],
            "SecretVersionsToStages": {"31dcba26-fd45-4791-8062-d04ef4aa7c93": ["AWSCURRENT"]},
            "CreatedDate": datetime.datetime(2022, 6, 13, 23, 4, 0, 413000, tzinfo=tzlocal()),
        }
    ],
    "ResponseMetadata": {
        "RequestId": "811ae1d5-6237-4aa3-bd62-66ac8d9047d3",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "811ae1d5-6237-4aa3-bd62-66ac8d9047d3",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "1353",
            "date": "Sat, 18 Jun 2022 22:35:28 GMT",
        },
        "RetryAttempts": 0,
    },
}


def test_stubber():
    stubber = Stubber(aws.client)
    response = smgmt_ls_resp
    stubber.add_response("list_secrets", response)
    stubber.activate()

    service_response = aws.get_secrets_list()
    assert service_response == response


# def test_stubber_with_cli():
#     stubber = Stubber(aws.client)
#     response = smgmt_ls_resp
#     stubber.add_response('list_secrets', response)
#     stubber.activate()

#     # service_response = aws.get_secrets_list()
#     # assert service_response == response
#     runner = CliRunner()
#     service_response = runner.invoke(cli, ["ls"])
#     # assert result.exit_code == 0
#     # assert result.output.startswith("cli, version ")
#     print(response,service_response)
#     assert service_response == response
