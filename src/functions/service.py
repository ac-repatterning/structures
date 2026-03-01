"""
Module service.py
"""

import boto3

import src.elements.service as sr


class Service:
    """
    Class Service

    Auto-login via IAM Identity Centre Single Sign On; beware of
    machine prerequisite.  Re-visit, vis-à-vis cloud runs.
      * https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html.

    A S3 resource service
      * https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.resource
    """

    def __init__(self, connector: boto3.session.Session, region_name: str):
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        :param region_name: Compute region.
        """

        # The S3 resource, S3 client, secrets, etc.
        self.__s3_resource: boto3.session.Session.resource = connector.resource(
            service_name='s3', region_name=region_name)
        self.__s3_client: boto3.session.Session.client = connector.client(
            service_name='s3', region_name=region_name)
        self.__secrets_manager = connector.client(
            service_name='secretsmanager', region_name=region_name)

    def exc(self) -> sr.Service:
        """

        :return:
            A collection of Amazon services
        """

        # Hence, the collection
        return sr.Service(s3_resource=self.__s3_resource,
                          s3_client=self.__s3_client,
                          secrets_manager=self.__secrets_manager)
