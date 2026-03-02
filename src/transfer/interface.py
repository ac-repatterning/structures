"""Module interface.py"""
import json
import logging
import os

import pandas as pd

import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.ingress
import src.s3.unload
import src.transfer.cloud
import src.transfer.dictionary


class Interface:
    """
    Class Interface
    """

    def __init__(self, service: sr.Service,  s3_parameters: s3p, attributes: dict):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.
        :param attributes:
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters
        self.__attributes: dict = attributes

        buffer = src.s3.unload.Unload(s3_client=self.__service.s3_client).exc(
            bucket_name=self.__s3_parameters.configurations, key_name='data/metadata.json')
        self.__metadata = json.loads(buffer)

    def __set_metadata(self, frame: pd.DataFrame) -> pd.DataFrame:
        """

        :param frame:
        :return:
        """

        # Assign metadata dict strings via section values
        frame['metadata'] = frame['section'].map(lambda x: self.__metadata[str(x)])

        return frame


    def exc(self):
        """

        :return:
        """

        # Re-ascertaining bucket existence, and executing steps vis-à-vis restart execution instance
        src.transfer.cloud.Cloud(
            service=self.__service, s3_parameters=self.__s3_parameters).exc(restart=self.__attributes.get('restart'))

        # The strings for transferring data to Amazon S3 (Simple Storage Service)
        strings: pd.DataFrame = src.transfer.dictionary.Dictionary().exc(
            path=os.path.join(os.getcwd(), 'warehouse'), extension='*', prefix='')

        # Transfer
        if strings.empty:
            logging.info('Empty')
        else:
            strings = self.__set_metadata(frame=strings.copy())
            logging.info(strings)
            messages = src.s3.ingress.Ingress(
                service=self.__service, bucket_name=self.__s3_parameters.internal).exc(
                strings=strings, tags={'project': 'hydrography'})
            logging.info(messages)
