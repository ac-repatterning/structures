"""Module api.py"""
import sys

import requests


class API:
    """
    Class API
    """

    def __init__(self):
        pass

    def __call__(self, url: str) -> str:
        """

        :param url: An online data source URL (Uniform Resource Locator)
        :return:
        """

        try:
            response = requests.get(url=url, timeout=600)
            response.raise_for_status()
        except requests.exceptions.Timeout as err:
            raise err from err
        except Exception as err:
            raise err from err

        if response.status_code == 200:
            content = response.content.decode(encoding='utf-8')
            return content

        sys.exit(response.status_code)
