"""
Module bucket.py
"""
import boto3
import botocore.exceptions

import src.elements.service as sr


class Bucket:
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/index.html
    """

    def __init__(self, service: sr.Service, location_constraint: str, bucket_name: str):
        """
        Constructor

        :param service: A suite of services for interacting with Amazon Web Services.
        :param location_constraint: The location constraint of an Amazon S3 (Simple Storage Service) bucket.
        :param bucket_name: The name of an Amazon S3 bucket in focus.
        """

        self.__s3_resource: boto3.session.Session.resource = service.s3_resource

        self.__location_constraint = location_constraint
        self.__bucket_name = bucket_name

        # A bucket instance
        self.__bucket = self.__s3_resource.Bucket(name=self.__bucket_name)

    def create(self) -> bool:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/create.html

        :return:
        """

        if self.exists():
            return True

        create_bucket_configuration = {
            'LocationConstraint': self.__location_constraint
        }
        try:
            self.__bucket.create(CreateBucketConfiguration=create_bucket_configuration)
            self.__bucket.wait_until_exists()
            return True
        except botocore.exceptions.ClientError as err:
            raise err from err

    def empty(self) -> bool:
        """
        Delete a bucket's objects

        :return:
        """

        if not self.exists():
            return True

        try:
            state = self.__bucket.objects.delete()
            return bool(state)
        except botocore.exceptions.ClientError as err:
            raise err from err

    def delete(self) -> bool:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/objects.html
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/delete.html
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/wait_until_not_exists.html

        :return:
        """

        if not self.exists():
            return True

        # Ensure the bucket is empty. Subsequently, delete the bucket.
        try:
            self.empty()
            self.__bucket.delete()
            self.__bucket.wait_until_not_exists()
            return True
        except botocore.exceptions.ClientError as err:
            raise err from err

    def exists(self) -> bool:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/head_bucket.html#S3.Client.head_bucket
        https://awscli.amazonaws.com/v2/documentation/api/2.0.34/reference/s3api/head-bucket.html

        :return:
        """

        try:
            state: dict = self.__bucket.meta.client.head_bucket(Bucket=self.__bucket.name)
            return bool(state)
        except self.__bucket.meta.client.exceptions.NoSuchBucket:
            return False
        except botocore.exceptions.ClientError:
            return False
