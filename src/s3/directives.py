"""Module directives.py"""
import os
import subprocess

import src.functions.directories


class Directives:
    """
    <b>Data Retrieval Directives</b><br>
    -------------------------<br>

    From Amazon S3 (Simple Storage Service) <b>to</b> local destination.
    """

    def __init__(self):
        """

        Constructor
        """

        # Directories instances
        self.__directories = src.functions.directories.Directories()

    def synchronise(self, source_bucket: str, origin: str, target: str) -> int:
        """

        :param source_bucket: An Amazon S3 (Simple Storage Service)
        :param origin: The prefix between the source bucket & one or more key names; starts and
                       ends without a stroke, i.e., /.
        :param target: A local directory
        :return:
        """

        # Create the destination directory
        self.__directories.create(path=target)

        # Destination & Source
        destination = target.replace(os.getcwd() + os.path.sep, '')
        source = f"s3://{source_bucket}/{origin}"

        # Hence
        state = subprocess.run(f"aws s3 sync {source} {destination}", shell=True, check=True)

        return state.returncode

    @staticmethod
    def delete(path: str) -> int:
        """

        :param path: s3://{bucket.name}/{prefix.string}/
        :return:
        """

        # Hence
        state = subprocess.run(f"aws s3 rm {path} --recursive", shell=True, check=True)

        return state.returncode

    def unload(self, source_bucket: str, origin: str, target: str) -> int:
        """

        :param source_bucket: An Amazon S3 (Simple Storage Service)
        :param origin: The prefix between the source bucket & one or more key names; starts and
                       ends without a stroke, i.e., /.
        :param target: A local directory
        :return:
        """

        # Create the destination directory
        self.__directories.create(path=target)

        # Hence
        destination = target.replace(os.getcwd() + os.path.sep, '')
        source = f"s3://{source_bucket}/{origin}/"
        state = subprocess.run(f"aws s3 cp {source} {destination}/ --recursive", shell=True, check=True)

        return state.returncode
