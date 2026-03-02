"""Module deduplicate.py"""
import logging

import pandas as pd


class Deduplicate:
    """
    Addresses duplicate readings per distinct time point.  If a time point has
    duplicate, the reading with the best quality code, i.e., lowest numeric
    value, is selected.
    """

    def __init__(self):
        """
        Constructor
        """

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                            datefmt='%Y-%m-%d %H:%M:%S')

        self.__logger = logging.getLogger(__name__)

    def __deduplicate(self, frame: pd.DataFrame) -> pd.DataFrame:
        """

        :param frame: a gauge's time series, and supplementary, data
        :return:
        """

        data = frame.sort_values(by=['timestamp', 'quality_code'], axis=0, ascending=True)
        data.drop_duplicates(subset=['timestamp'], keep='first', inplace=True)

        if data.shape[0] != frame.shape[0]:
            self.__logger.info('original, deduplicated, deduplicates: %s, %s\n%s',
                         frame.shape, data.shape, data.head())

        return data

    def exc(self, frame: pd.DataFrame) -> pd.DataFrame:
        """

        :param frame: a gauge's time series, and supplementary, data
        :return:
        """

        return self.__deduplicate(frame=frame)
