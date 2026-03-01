"""Delete __pycache__"""
import logging
import pathlib
import shutil


class Cache:
    """
    Extraneous
    """

    def __init__(self) -> None:
        """
        Constructor
        """

        self.__patterns: list[str] = ['__pycache__', '.pytest_cache']

        # Logging
        logging.basicConfig(level=logging.WARNING,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __delete(self, pattern: str) -> None:
        """

        :return:
        """

        for path in pathlib.Path.cwd().rglob(pattern=pattern):
            if path.is_dir():
                try:
                    shutil.rmtree(path)
                except PermissionError as err:
                    raise (self.__logger.warning(err)) from err

    def exc(self):
        """

        :return: None
        """

        for pattern in self.__patterns:

            self.__delete(pattern=pattern)
