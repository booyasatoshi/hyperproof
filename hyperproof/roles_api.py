# roles_api.py
# 
# This module provides functionality for interacting with the Roles API of Hyperproof.
# Author: Virgil Vaduva
# Timestamp: 2024-09-25
# License: This project is licensed under the GNU General Public License (GPL).
#
# Description:
# The RolesAPI class is responsible for handling interactions with the Roles API,
# allowing for operations such as retrieving a list of roles in the organization.

from .utils import logger

class RolesAPI:
    """
    This class handles interactions with the Roles API of Hyperproof.
    It allows retrieving a list of roles in the organization.
    """
    BASE_URL = "https://api.hyperproof.app/v1/roles"

    def __init__(self, api_client):
        # Use the shared API client
        self.client = api_client

    def get_roles(self, raw=False):
        """
        Retrieves a list of roles in the organization.

        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        return self.client.get(self.BASE_URL, "/", raw=raw)
