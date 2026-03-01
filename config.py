"""
Module config
"""
import os


class Config:
    """
    Class Config

    For project settings
    """

    def __init__(self):
        """
        Constructor
        """

        self.warehouse: str = os.path.join(os.getcwd(), 'warehouse')
        self.fundamentals_ = os.path.join(self.warehouse, 'data', 'fundamentals')
        self.resamples_ = os.path.join(self.warehouse, 'data', 'resamples')

        # Keys
        self.s3_parameters_key = 's3_parameters.yaml'
        self.attributes_key = 'data/structures/attributes.json'
