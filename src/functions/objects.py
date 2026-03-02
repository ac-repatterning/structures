"""
Module objects.py
"""
import json
import pathlib
import pandas as pd

import src.functions.api


class Objects:
    """
    Class Objects

    Description
    -----------
    This class reads & writes JSON (JavaScript Object Notation) objects.
    """

    def __init__(self):
        """
        Constructor
        """

    @staticmethod
    def write(nodes: dict, path: str) -> str:
        """

        :param nodes: A dictionary of data
        :param path: A string, which includes a file name & extension, representing a storage point.
        :return:
        """

        name = pathlib.Path(path).stem

        if not bool(nodes):
            return f'{name}: empty'

        try:
            with open(file=path, mode='w', encoding='utf-8') as disk:
                json.dump(obj=nodes, fp=disk, ensure_ascii=False, indent=4)
            return f'{name}: succeeded'
        except IOError as err:
            raise err from err

    @staticmethod
    def api(url: str) -> dict | list[dict]:
        """

        :param url: An online data source URL (Uniform Resource Locator)
        :return:
        """

        instance = src.functions.api.API()
        content = instance(url=url)

        return json.loads(content)

    @staticmethod
    def read(uri: str) -> dict | list[dict]:
        """

        :param uri: A file's URI (Uniform Resource Identifier)
        :return:
        """

        try:
            with open(file=uri, mode='r', encoding='utf-8') as disk:
                return json.load(fp=disk)
        except ImportError as err:
            raise err from err

    @staticmethod
    def frame(path: str, orient: str) -> pd.DataFrame:
        """

        :param path:
        :param orient:
        :return:
        """

        try:
            cases = pd.read_json(path_or_buf=path, orient=orient)
        except ImportError as err:
            raise err from err

        return cases
