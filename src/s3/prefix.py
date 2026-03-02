"""Module prefix.py"""

import botocore.exceptions

import src.elements.service as sr
import src.s3.keys


class Prefix:
    """
    Class Prefix
    """

    def __init__(self, service: sr.Service, bucket_name: str):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param bucket_name: The name of an Amazon S3 bucket in focus.
        """

        self.__service: sr.Service = service
        self.__s3_client = self.__service.s3_client
        self.__bucket_name = bucket_name

    def delete(self, objects: list[dict]):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/delete_objects.html
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/bucket/delete_objects.html

        :param objects: The objects of Amazon S3 (Simple Storage Service) bucket.  The
                        format is [{'Key': '...', 'Key': '...', 'Key': '...', ...}]
        :return:
        """

        try:
            response = self.__s3_client.delete_objects(
                Bucket=self.__bucket_name, Delete={'Objects': objects, 'Quiet': False})
        except botocore.exceptions.ClientError as err:
            raise err from err

        return response

    def objects(self, prefix: str, delimiter: str = '') -> list[str]:
        """

        :param prefix: An Amazon S3 (Simple Storage Service) prefix.
        :param delimiter: Either '' or '/'
        :return:
        """

        instance = src.s3.keys.Keys(service=self.__service, bucket_name=self.__bucket_name)

        return instance.excerpt(prefix=prefix, delimiter=delimiter)
