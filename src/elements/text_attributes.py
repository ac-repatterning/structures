"""
This is the data type TextAttributes
"""
import typing


class TextAttributes(typing.NamedTuple):
    """
    The data type class ⇾ TextAttributes

    Attributes
    ----------
        uri :
            The uniform resource identifier; path + file + extension string.
        header :
            The header row of the `csv` file
        sep :
            The separator
        usecols :
            The fields in focus
        dtype :
            Dictionary of type per field
        date_fields :
            The list of data fields, if any.
        date_format :
            The date format per date field.
    """

    uri: str
    header: int
    sep: str = ','
    usecols: list = None
    dtype: dict = None
    date_fields: list = None
    date_format: dict = None
