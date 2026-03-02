"""Module dictionary.py"""
import logging
import glob
import os

import pandas as pd


class Dictionary:
    """
    Class Dictionary
    """

    def __init__(self):
        pass

    @staticmethod
    def __local(path: str, extension: str) -> pd.DataFrame:
        """

        :param path: The path wherein the files of interest lie
        :param extension: The extension type of the files of interest
        :return:
        """

        # This will be warehouse/
        splitter = os.path.basename(path) + os.path.sep
        logging.info('SPLITTER: %s', splitter)

        # The list of files within the path directory, including its child directories.
        files: list[str] = glob.glob(pathname=os.path.join(path, '**', f'*.{extension}'), recursive=True)

        # Hence
        if len(files) == 0:
            return pd.DataFrame()

        details: list[dict] = [{'file': file,
                                'vertex': file.rsplit(splitter, maxsplit=1)[1]}
                               for file in files]

        return pd.DataFrame.from_records(details)

    @staticmethod
    def __sections(local: pd.DataFrame) -> pd.DataFrame:
        """

        :param local:
        :return:
        """

        local['section'] = local['vertex'].apply(lambda x: str(x).split(sep='/', maxsplit=3)[1])

        return local

    def exc(self, path: str, extension: str, prefix: str) -> pd.DataFrame:
        """

        :param path: The path wherein the files of interest lie
        :param extension: The extension type of the files of interest
        :param prefix: The Amazon S3 (Simple Storage Service) where the files of path are heading
        :return:
        """

        local: pd.DataFrame = self.__local(path=path, extension=extension)
        if local.empty:
            return pd.DataFrame()

        # Building the Amazon S3 strings
        local = self.__sections(local=local.copy())
        frame = local.assign(key=prefix + local["vertex"])

        return frame
