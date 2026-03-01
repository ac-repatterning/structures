"""
Module setup.py
"""
import os

import config
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.directories
import src.s3.bucket
import src.s3.prefix


class Cloud:
    """

    Notes
    -----

    This class prepares the Amazon S3 (Simple Storage Service) and local data environments.
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters

        # Configurations
        self.__configurations = config.Config()

        # An instance for interacting with objects within an Amazon S3 prefix
        self.__pre = src.s3.prefix.Prefix(service=self.__service, bucket_name=self.__s3_parameters.internal)

        self.__prefixes = [self.__s3_parameters.path_internal_data + os.path.basename(value)
                           for value in [self.__configurations.resamples_, self.__configurations.fundamentals_] ]

    def __clear_prefix(self) -> bool:
        """

        :return:
        """

        # Get the keys therein
        states = []
        for prefix in self.__prefixes:
            keys: list[str] = self.__pre.objects(prefix=prefix)
            if len(keys) > 0:
                objects = [{'Key' : key} for key in keys]
                state = self.__pre.delete(objects=objects)
                states.append(bool(state))
            else:
                states.append(True)

        return all(states)

    def __s3(self, restart: bool) -> bool:
        """
        Prepares an Amazon S3 (Simple Storage Service) bucket.

        :param restart: Is this part of a re-compute directive?
        :return:
        """

        # An instance for interacting with Amazon S3 buckets.
        bucket = src.s3.bucket.Bucket(service=self.__service, location_constraint=self.__s3_parameters.location_constraint,
                                      bucket_name=self.__s3_parameters.internal)

        if bucket.exists():
            return self.__clear_prefix() if restart else True

        return bucket.create()

    def exc(self, restart: bool) -> bool:
        """

        :param restart: Is this part of a re-compute directive?
        :return:
        """

        return self.__s3(restart=restart)
