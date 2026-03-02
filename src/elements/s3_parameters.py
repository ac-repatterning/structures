"""
This is data type S3Parameters
"""
import typing


class S3Parameters(typing.NamedTuple):
    """
    The data type class ⇾ S3Parameters

    Attributes
    ----------
    region_name : str
      The Amazon Web Services region code.

    location_constraint : str
      The region code of the region that the data is limited to.

    internal : str
      The Amazon S3 (Simple Storage Service) bucket that hosts this project's data.

    path_internal_data : str
      A root bucket-prefix for data.

    path_internal_references : str
      A root bucket-prefix for references.

    path_internal_artefacts : str
      A root bucket-prefix for the artefacts of models.

    external: str
      An Amazon S3 (Simple Storage Service) bucket.

    configurations: str
      An Amazon S3 (Simple Storage Service) bucket.
    """

    region_name: str
    location_constraint: str
    internal: str
    path_internal_data: str
    path_internal_references: str
    path_internal_artefacts: str
    external: str
    configurations: str
