"""
Module: streams.py
"""
import csv
import pathlib

import pandas as pd
import requests

import src.elements.text_attributes as txa


class Streams:
    """
    Class Streams

    Description
    -----------
    Reads 'csv' files, and exports data frames to 'csv' files.
    """

    def __init__(self):
        """
        Constructor
        """

    @staticmethod
    def write(blob: pd.DataFrame, path: str) -> str:
        """
        :param blob: The data being stored in a `csv` file.
        :param path: The path + file + extension string.
        :return:
        """

        name = pathlib.Path(path).stem

        if blob.empty:
            return f'{name}: empty'

        try:
            blob.to_csv(path_or_buf=path, index=False, header=True, encoding='utf-8',
                        quoting=csv.QUOTE_NONNUMERIC)
            return f'{name}: succeeded'
        except OSError as err:
            raise ValueError(err.strerror) from err

    @staticmethod
    def read(text: txa.TextAttributes) -> pd.DataFrame:
        """

        :param text: Includes uri: str, header: int = 0, usecols: list = None,
                     dtype: dict = None, date_fields: list = None,
                     date_format: dict = None.
        :return:
        """

        if text.date_fields is None:
            parse_dates = False
        else:
            parse_dates = text.date_fields

        try:
            return pd.read_csv(filepath_or_buffer=text.uri, header=text.header,
                               sep=text.sep, usecols=text.usecols, dtype=text.dtype,
                               encoding='utf-8', parse_dates=parse_dates,
                               date_format=text.date_format)
        except ImportError:
            return pd.DataFrame()

    def api(self, text: txa.TextAttributes) -> pd.DataFrame:
        """

        :param text: Includes uri: str, header: int = 0, usecols: list = None,
                     dtype: dict = None, date_fields: list = None,
                     date_format: dict = None.
        :return:
        """

        data = pd.DataFrame()

        try:
            response = requests.head(url=text.uri, timeout=300)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise ValueError(f'HTTP Error: {err}') from err

        if response.status_code == 200:
            data = self.read(text=text)

        return data
