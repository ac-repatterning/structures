"""Module inspect.py"""
import datetime
import logging

import numpy as np
import pandas as pd

import src.elements.partitions as pr


class Inspect:
    """
    Ascertains date points; every 15 minutes.
    """

    def __init__(self):
        """
        Constructor
        """

        # The gauges record river water levels every 15 minutes; at the quarter points of an hour.
        self.__frequency = '0.25h'

    def __get_reference(self, _maximum: pd.Timestamp, _minimum: pd.Timestamp) -> pd.DataFrame:
        """

        :param _maximum:
        :param _minimum:
        :return:
        """

        latest = datetime.datetime.now().year
        dates = pd.date_range(
            start=_minimum, end=_maximum, freq=self.__frequency,
            inclusive='left' if _maximum.year != latest else 'both',
            name='date').to_frame()
        dates.reset_index(drop=True, inplace=True)

        return dates

    @staticmethod
    def __set_missing(data: pd.DataFrame, partition: pr.Partitions) -> pd.DataFrame:

        frame = data.copy()
        states = frame['measure'].isna()
        logging.info(frame.loc[states, :])

        frame.loc[states, 'ts_id'] = partition.ts_id
        frame.loc[states, 'timestamp'] = (frame.loc[states, 'date'].astype(np.int64)/1000000).values
        logging.info(frame.loc[states, :])

        return frame

    def exc(self, frame: pd.DataFrame, partition: pr.Partitions) -> pd.DataFrame:
        """

        :param frame:
        :param partition:
        :return:
        """

        # A pandas.Timestamp field of dates
        frame['date'] = pd.to_datetime(frame['timestamp'], unit='ms')

        # Get the reference set of dates; Sequence(minimum, maximum, every 15 minutes)
        dates: pd.DataFrame = self.__get_reference(_maximum=frame['date'].max(), _minimum=frame['date'].min())

        # Ascertaining a strictly monotonically increasing date sequence of frequency 0.25 hours
        data = frame.copy().merge(dates, how='right', on='date')
        data.sort_values(by='date', ascending=True, inplace=True)

        # Setting empty cells of known values
        data = self.__set_missing(data=data, partition=partition)

        return data
