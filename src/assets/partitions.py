"""Module partitions.py"""
import datetime
import typing

import pandas as pd


class Partitions:
    """
    Partitions for parallel computation.
    """

    def __init__(self, data: pd.DataFrame, attributes: dict):
        """

        :param data:
        :param attributes:
        """

        self.__data = data
        self.__attributes = attributes

    @staticmethod
    def __boundaries() -> typing.Tuple[datetime.datetime, datetime.datetime]:
        """
        The boundaries of the dates; datetime format

        :return:
        """

        # Ending
        _end = datetime.datetime.now().year
        ending = datetime.datetime.strptime(f'{_end}-01-01', '%Y-%m-%d')

        # Starting
        _start: int = _end - 1
        starting = datetime.datetime.strptime(f'{_start}-01-01', '%Y-%m-%d')

        return starting, ending

    def __dates(self, starting: datetime.datetime, ending: datetime.datetime) -> pd.DataFrame:
        """

        :param starting:
        :param ending:
        :return:
        """

        frame = pd.date_range(
            start=starting, end=ending, freq=self.__attributes.get('frequency')
        ).to_frame(index=False, name='datestr')

        return frame['datestr'].apply(lambda x: x.strftime('%Y-%m-%d')).to_frame()

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        # Reacquisition with respect to all gauges, and the system's data time span
        if self.__attributes.get('restart'):
            return self.__data

        # Standard ...
        codes: list = self.__attributes.get('excerpt')
        if len(codes) == 0:
            data = self.__data
        else:
            catchments = self.__data.loc[self.__data['ts_id'].isin(codes), 'catchment_id'].unique()
            data = self.__data.copy().loc[self.__data['catchment_id'].isin(catchments), :]
            data = data if data.shape[0] > 0 else self.__data

        # Daily standard behaviour
        starting, ending = self.__boundaries()
        dates = self.__dates(starting=starting, ending=ending)
        frame = dates.merge(data, how='left', on='datestr')

        return frame
