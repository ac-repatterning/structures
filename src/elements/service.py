"""
This is the data type Interface
"""

import typing

import boto3


class Service(typing.NamedTuple):
    """
    The data type class ⇾ Service

    Attributes
    ----------
    s3_resource: boto3.session.Session.resource
        The boto3.resource instance, with service & region name settings.
    s3_client: boto3.session.Session.client
        The boto3.client instance, with service & region name settings.
    secrets_manager: boto3.session.Session.client
        A boto3.client instance for secrets
    """

    s3_resource: boto3.session.Session.resource
    s3_client: boto3.session.Session.client
    secrets_manager: boto3.session.Session.client
