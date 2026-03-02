"""Module cloud.py"""
import logging

import dask
import numpy as np

import src.elements.partitions as pr
import src.elements.s3_parameters as s3p
import src.s3.directives


class Delete:
    """
    Preparing particular cloud spots
    """

    def __init__(self, s3_parameters: s3p.S3Parameters):
        """

        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        """

        self.__s3_parameters = s3_parameters
        self.__directive = src.s3.directives.Directives()

    def __delete(self, section: str, partition: pr.Partitions) -> int:
        """

        :param section: fundamentals or resamples; the granularity of the former is 0.25 hours, whilst
                        that of the latter is 1 hour.
        :param partition: Refer to src/elements/partitions.py
        :return:
        """

        state = self.__directive.delete(
            path=f's3://{self.__s3_parameters.internal}/data/{section}/{partition.catchment_id}/{partition.ts_id}/')

        return state

    def exc(self, partitions: list[pr.Partitions]):
        """

        :param partitions: Refer to src/elements/partitions.py
        :return:
        """

        computations = []
        for partition in partitions:
            computations.append(
                np.array([self.__delete(section='fundamentals', partition=partition),
                          self.__delete(section='resamples', partition=partition)])
            )
        calculations = dask.compute(computations, scheduler='threads')[0]

        states = np.concat(calculations)

        logging.info(states)
        logging.info(sum(states))
