"""Module resampling.py"""
import pandas as pd


class Resampling:
    """
    Resampling
    """

    def __init__(self):
        pass

    @staticmethod
    def __resample(data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data:
        :return:
        """

        dates = pd.date_range(start=data['date'].min(), end=data['date'].max(), freq='h', inclusive='both')

        data = pd.DataFrame(data={'date': dates}).merge(data, how='left', on='date')

        return data.sort_values(by=['timestamp'], ascending=True)

    def exc(self, data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        return self.__resample(data=data.copy())
