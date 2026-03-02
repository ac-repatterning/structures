"""Module datum.py"""

import pandas as pd

import src.elements.s3_parameters as s3p
import src.elements.text_attributes as txa
import src.functions.streams


class Datum:
    """

    Datum
    """

    def __init__(self,  s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters:
        """

        self.__s3_parameters = s3_parameters

    def __get_datum(self) -> pd.DataFrame:
        """

        :return:
        """

        uri = f's3://{self.__s3_parameters.internal}/{self.__s3_parameters.path_internal_references}assets.csv'
        usecols = ['ts_id', 'gauge_datum']
        text = txa.TextAttributes(uri=uri, header=0, usecols=usecols)

        return src.functions.streams.Streams().read(text=text)

    def __call__(self) -> pd.DataFrame:
        """

        :return:
        """

        return self.__get_datum()
