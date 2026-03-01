"""Module ingress.py"""
import urllib.parse

import botocore.exceptions
import dask
import pandas as pd

import src.elements.service as sr


class Ingress:
    """
    Class Ingress

    Description
    -----------

    Uploads files to Amazon Simple Storage Service (S3)
    """

    def __init__(self, service: sr.Service, bucket_name):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param bucket_name: The name of the target bucket.
        """

        self.__s3_client = service.s3_client
        self.__bucket_name = bucket_name

    @dask.delayed
    def __ingress(self, file: str, key: str, metadata: dict, tags: dict = None) -> str:
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/
            s3.html#boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS

        :param file: The local file string, i.e., <path> + <file name> + <extension>,
                     of the file being uploaded
        :param key: The Amazon S3 key of the file being uploaded; the key is
                    relative-to the S3 Bucket name, but excludes the S3 Bucket name.
        :param metadata: The metadata of the files being uploaded. Note, files of
                         the same content type are expected, assumed.
        :param tags: Tags
        :return:
        """

        # From dict, e.g., {'flock': 'sheep', 'shoal': 'aquatic creatures'}, to 'flock=sheep&shoal=aquatic+creatures'
        if tags:
            tagging = urllib.parse.urlencode(tags)
        else:
            tagging = ''

        try:
            self.__s3_client.upload_file(Filename=file, Bucket=self.__bucket_name, Key=key,
                                         ExtraArgs={'Metadata': metadata, 'Tagging': tagging})
            return f'Uploading {key}'
        except botocore.exceptions.ClientError as err:
            raise err from err

    def exc(self, strings: pd.DataFrame, tags: dict = None) -> list[str]:
        """

        :param strings: The strings for Amazon Simple Storage Service (S3) transfers
        :param tags: For project, etc., tagiing.
        :return:
        """

        computations = []
        for string in strings.to_dict(orient='records'):
            message = self.__ingress(file=string['file'], key=string['key'],
                                     metadata=string['metadata'], tags=tags)
            computations.append(message)
        messages = dask.compute(computations, scheduler='threads')[0]

        return messages
