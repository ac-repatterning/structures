"""Module egress.py"""
import pathlib

import boto3
import botocore.exceptions
import dask
import pandas as pd

import src.elements.service as sr


class Egress:
    """
    For unloading files stored within an Amazon S3 (Simple Storage Service) bucket
    """

    def __init__(self, service: sr.Service, bucket_name):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param bucket_name: The name of the target bucket.
        """

        self.__s3_client: boto3.session.Session.client = service.s3_client
        self.__bucket_name = bucket_name

    @dask.delayed
    def __egress(self, key: str, filename: str) -> str:
        """

        :param key: The name of the Amazon S3 (Simple Storage Service) file to unload
        :param filename: Where the file will be saved
        :return:
        """

        try:
            self.__s3_client.download_file(Bucket=self.__bucket_name, Key=key, Filename=filename)
            return f'Successful: {pathlib.PurePath(filename).name}'
        except botocore.exceptions.ClientError as err:
            raise err from err

    def exc(self, strings: pd.DataFrame) -> list:
        """

        :param strings: A frame of strings for retrieving objects from
                        Amazon Simple Storage Service (S3).
        :return:
        """

        computations = []
        for string in strings.to_dict(orient='records'):
            message = self.__egress(key=string['key'], filename=string['filename'])
            computations.append(message)
        messages = dask.compute(computations, scheduler='threads')[0]

        return messages
