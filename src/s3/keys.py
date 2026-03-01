"""
Module keys.py
"""
import boto3
import botocore.exceptions

import src.elements.service as sr


class Keys:
    """
    Class Keys

    Notes
    -----

    Gets lists of Amazon S3 keys.
    """

    def __init__(self, service: sr.Service, bucket_name: str):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param bucket_name: The name of an Amazon S3 bucket in focus.
        """

        self.__bucket_name = bucket_name
        self.__s3_resource: boto3.session.Session.resource = service.s3_resource
        self.__s3_client = service.s3_client
        self.__bucket = self.__s3_resource.Bucket(name=self.__bucket_name)

    def excerpt(self, prefix: str, delimiter: str = '') -> list[str]:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_objects_v2.html

        :param prefix: An Amazon S3 (Simple Storage Service) prefix.
        :param delimiter: Either '' or '/'
        :return:
            A list of Amazon S3 (Simple Storage Service) keys.
        """

        # Keys
        try:
            dictionaries = self.__s3_client.list_objects_v2(
                Bucket=self.__bucket_name, Prefix=prefix, Delimiter=delimiter, MaxKeys=100000)
        except botocore.exceptions.ClientError as err:
            raise err from err

        # Any keys?
        if dictionaries['KeyCount'] == 0:
            return []

        match delimiter:
            case '':
                return [dictionary['Key']
                        for dictionary in dictionaries['Contents']]
            case '/':
                return [dictionary['Prefix']
                    for dictionary in dictionaries['CommonPrefixes']]
            case _:
                return []

    def all(self) -> list[str]:
        """

        :return:
            A list of Amazon S3 (Simple Storage Service) keys.
        """

        try:
            state: dict = self.__bucket.meta.client.head_bucket(Bucket=self.__bucket.name)
        except self.__bucket.meta.client.exceptions.NoSuchBucket as err:
            raise err from err
        except botocore.exceptions.ClientError as err:
            raise err from err

        if state:
            items = [k.key for k in list(self.__bucket.objects.all())]
        else:
            items = []

        return items
