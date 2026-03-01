"""Module interface.py"""
import logging
import os

import pandas as pd
import dask

import config
import src.algorithms.deduplicate
import src.algorithms.inspect
import src.algorithms.resampling
import src.elements.partitions as pr
import src.elements.text_attributes as txa
import src.functions.directories
import src.functions.streams


class Interface:
    """
    Interface
    """

    def __init__(self):
        """
        Constructor
        """

        self.__directories = src.functions.directories.Directories()
        self.__streams = src.functions.streams.Streams()

        # Configurations
        self.__configurations = config.Config()

    @dask.delayed
    def __get_data(self, uri: str) -> pd.DataFrame:
        """

        :param uri:
        :return:
        """

        text = txa.TextAttributes(uri=uri, header=0)

        return self.__streams.read(text=text)

    @dask.delayed
    def __append_measure(self, frame: pd.DataFrame, gauge_datum: float):
        """

        :param frame:
        :param gauge_datum:
        :return:
        """


        frame['measure'] = frame['value'] + gauge_datum

        return frame

    @dask.delayed
    def __persist(self, data: pd.DataFrame, endpoint: str, partition: pr.Partitions):
        """
        To minimise storage costs, drop 'date', keep 'timestamp'.  The 'date' values are
         derivable from the 'timestamp' values.

        :param data:
        :param endpoint:
        :param partition:
        :return:
        """

        path = os.path.join(endpoint, str(partition.catchment_id), str(partition.ts_id))
        self.__directories.create(path=path)

        message = self.__streams.write(
            blob=data.drop(columns='date'), path=os.path.join(path, f'{partition.datestr}.csv'))

        return message + f', {os.path.basename(endpoint)} | {partition.ts_id}'

    def exc(self, partitions: list[pr.Partitions]):
        """

        :param partitions:
        :return:
        """

        # Delayed Tasks
        __inspect = dask.delayed(src.algorithms.inspect.Inspect().exc)
        __deduplicate = dask.delayed(src.algorithms.deduplicate.Deduplicate().exc)
        __resampling = dask.delayed(src.algorithms.resampling.Resampling().exc)

        computations = []
        for partition in partitions:

            data = self.__get_data(uri=partition.uri)
            data = __deduplicate(frame=data)
            data = self.__append_measure(frame=data.copy(), gauge_datum=partition.gauge_datum)
            fundamentals = __inspect(frame=data.copy(), partition=partition)
            resamples = __resampling(data=fundamentals)

            computations.append((
                self.__persist(data=fundamentals, endpoint=self.__configurations.fundamentals_, partition=partition),
                self.__persist(data=resamples, endpoint=self.__configurations.resamples_, partition=partition)
            ))

        calculations = dask.compute(computations, scheduler='threads')[0]
        logging.info(calculations)
