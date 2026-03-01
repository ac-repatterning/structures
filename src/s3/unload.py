"""
Module unload.py
"""

import botocore.exceptions

import boto3


class Unload:
    """

    Notes<br>
    ------<br>

    Unloads a data file from Amazon S3 (Simple Storage Service).  Extracts and decodes
    the 'Body' name.  If<br>
        &nbsp; &nbsp; blob = self.__s3_client.get_object(...)<br>
    and<br>
        &nbsp; &nbsp; buffer = blob['Body'].read().decode('utf-8')<br><br>
    <b>Then</b>
    <ul>
        <li>JSON: No more steps; `buffer` is a dict.</li>
        <li>CSV: io.StringIO(buffer)</li>
    </ul>
    <br>
    """

    def __init__(self, s3_client: boto3.session.Session.client):
        """

        :param s3_client: An S3 (Simple Storage Service) client instance
        """

        self.__s3_client = s3_client

    def exc(self, bucket_name: str, key_name: str):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/get_object.html
        https://botocore.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#client-exceptions

        :param bucket_name:
        :param key_name: The S3 path of the data file, excluding the bucket name, including the file name.
        :return:
        """

        try:
            blob = self.__s3_client.get_object(Bucket=bucket_name, Key=key_name)
        except self.__s3_client.exceptions.NoSuchKey as err:
            raise err from err
        except self.__s3_client.exceptions.InvalidObjectState as err:
            raise err.response
        except botocore.exceptions.ClientError as err:
            raise err.response

        buffer = blob['Body'].read().decode('utf-8')

        return buffer
