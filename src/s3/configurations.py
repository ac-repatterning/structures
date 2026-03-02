"""Module configurations.py"""
import json

import boto3
import yaml

import src.functions.secret
import src.s3.unload


class Configurations:
    """
    Notes<br>
    ------<br>

    This class reads-in Amazon S3 (Simple Storage Service) based configuration files.
    """

    def __init__(self, connector: boto3.session.Session):
        """

        :param connector: An instance of boto3.session.Session
        """

        # An instance for S3 interactions
        self.__s3_client: boto3.session.Session.client = connector.client(
            service_name='s3')

        # An instance for Secrets Manager interactions.
        self.__secret = src.functions.secret.Secret(connector=connector)

    def __buffer(self, key_name: str):
        """

        :param key_name: <prefix> + <file name, including extension>
        :return:
        """

        buffer = src.s3.unload.Unload(s3_client=self.__s3_client).exc(
            bucket_name=self.__secret.exc(secret_id='HydrographyProject', node='configurations'),
            key_name=key_name)

        return buffer

    def serial(self, key_name: str) -> dict:
        """

        :param key_name: <prefix> + <file name, including extension>
        :return:
            A dictionary of <a href="https://yaml.org" target="_blank">YAML</a> file contents
        """

        try:
            data: dict = yaml.load(stream=self.__buffer(key_name=key_name), Loader=yaml.CLoader)
        except yaml.YAMLError as err:
            raise err from err

        return data

    def objects(self, key_name: str):
        """

        :param key_name: <prefix> + <file name, including extension>
        :return:
            A dictionary of <a href="https://www.json.org/json-en.html" target="_blank">
            JSON (JavaScript Object Notation)</a> file contents
        """

        try:
            data = json.loads(self.__buffer(key_name=key_name))
        except json.JSONDecodeError as err:
            raise err from err

        return data
