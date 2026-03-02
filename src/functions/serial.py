"""
Module serial.py
"""
import yaml

import src.functions.api


class Serial:
    """
    Class Serial

    Description
    -----------
    Present, this class reads-in local YAML data files; YAML is a data serialisation language.
    """

    def __init__(self):
        """
        Constructor
        """

    @staticmethod
    def api(url: str) -> dict:
        """

        :param url: The file string of a local YAML file; path + file name + extension.
        :return:
        """

        instance = src.functions.api.API()
        content = instance(url=url)

        return yaml.safe_load(content)

    @staticmethod
    def read(uri: str) -> dict:
        """

        :param uri: The file string of a local YAML file; path + file name + extension.
        :return:
        """

        with open(file=uri, mode='r', encoding='utf-8') as stream:
            try:
                return yaml.load(stream=stream, Loader=yaml.CLoader)
            except yaml.YAMLError as err:
                raise err from err
