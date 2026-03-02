"""Module specific.py"""
import argparse

class Specific:
    """
    Specific
    """

    def __init__(self):
        pass

    @staticmethod
    def codes(value: str = '') -> list:
        """

        :param value:
        :return:
        """

        if len(value) == 0:
            return []

        # Split and strip
        elements = [e.strip() for e in value.split(',')]

        try:
            _codes = [int(element) for element in elements]
        except argparse.ArgumentTypeError as err:
            raise err from err

        return _codes
