"""Module interface.py"""
import typing

import boto3

import config
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.service
import src.preface.setup
import src.s3.configurations
import src.s3.s3_parameters


class Interface:
    """
    Interface
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()

    def __get_attributes(self, connector: boto3.session.Session) -> dict:
        """

        :param connector: <a href="https://boto3.amazonaws.com/v1/documentation/api/latest/guide/session.html#custom-session">
                          A boto3 custom session</a>
        :return:
        """

        attributes =  src.s3.configurations.Configurations(
            connector=connector).objects(key_name=self.__configurations.attributes_key)

        return attributes

    @staticmethod
    def __precedence(inactive: bool, codes: list[int], attributes: dict) -> dict:
        """

        :param inactive: Is the cloud storage area inactive?
        :param codes: A set of gauge time series codes
        :param attributes: github.com/repatterning/configurations/src/data/structures/attributes.*
        :return:
        """

        # Initial setting
        attributes['restart'] = bool(inactive)


        if codes is None:
            attributes['excerpt'] = []
        else:
            attributes['excerpt'] = codes
            attributes['restart'] = False

        return attributes

    def exc(self, codes: list[int]) -> typing.Tuple[boto3.session.Session, s3p.S3Parameters, sr.Service, dict]:
        """

        :param codes:
        :return:
        """

        connector = boto3.session.Session()
        s3_parameters: s3p.S3Parameters = src.s3.s3_parameters.S3Parameters(connector=connector).exc()
        service: sr.Service = src.functions.service.Service(
            connector=connector, region_name=s3_parameters.region_name).exc()
        attributes: dict = self.__get_attributes(connector=connector)

        # Setting up
        inactive = src.preface.setup.Setup(
            service=service, s3_parameters=s3_parameters).exc()

        # The restart & excerpt fields
        attributes = self.__precedence(inactive=inactive, codes=codes, attributes=attributes)

        return connector, s3_parameters, service, attributes
