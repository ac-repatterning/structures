"""
Module secret.py
"""
import json

import boto3
import botocore.exceptions


class Secret:
    """
    <b>Description</b><br>
    ------------<br>
    This class will retrieve a requested secret.<br><br>


    <b>References</b><br>
    ------------<br>

    <a href="https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html" target="_blank">
    Secret Value Documentation</a>

    """

    def __init__(self, connector: boto3.session.Session) -> None:
        """

        :param connector: A boto3 session instance, it retrieves the developer's <default> Amazon
                          Web Services (AWS) profile details, which allows for programmatic interaction with AWS.
        """

        # self.__session = boto3.session.Session()
        self.__secrets_manager = connector.client(service_name='secretsmanager')

    def __get__value(self, secret_id: str) -> str:
        """
        The reader of a secret key's value.

        :param secret_id: The identification code of the secret

        Returns:
            _type_: str
        """

        try:
            secret_value: dict = self.__secrets_manager.get_secret_value(
                SecretId=secret_id)
        except botocore.exceptions.ClientError as err:
            raise err

        return secret_value['SecretString']

    def exc(self, secret_id: str, node: str = None) -> str:
        """
        Gets the value of a secret key.

        :param secret_id: The identification code of the secret
        :param node: A child element

        Returns:
            _type_: str
        """

        expression = self.__get__value(secret_id=secret_id)
        dictionary: dict = json.loads(expression)

        if node is None:
            return dictionary[secret_id]

        return dictionary[node]
