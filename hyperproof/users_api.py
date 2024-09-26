# users_api.py
# 
# This module provides functionality for interacting with the Users API of Hyperproof.
# Author: Virgil Vaduva
# Timestamp: 2024-09-25
# License: This project is licensed under the GNU General Public License (GPL).
#
# Description:
# The UsersAPI class is responsible for handling interactions with the Users API,
# allowing for retrieving information about the currently authenticated user and organization users.

from .utils import logger

class UsersAPI:
    """
    This class handles interactions with the Users API of Hyperproof.
    It allows retrieving information about the currently authenticated user and organization users.
    """
    BASE_URL = "https://api.hyperproof.app/v1/users"

    def __init__(self, api_client):
        # Use the shared API client
        self.client = api_client

    def get_current_user(self, expand=None, raw=False):
        """
        Retrieves the stored user information for the currently authenticated user.

        :param expand: Comma-separated list of fields to expand. Supported values: 'identityProviders', 'organizations' (optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        params = {
            'expand': expand
        }
        return self.client.get(self.BASE_URL, "/me", params=params, raw=raw)

    def get_organization_users(self, expand=None, include_deactivated=False, raw=False):
        """
        Retrieves the users in an organization.

        :param expand: Comma-separated list of fields to expand. Supported values: 'identityProviders', 'organizationRoleId' (optional).
        :param include_deactivated: Whether or not to include deactivated users in the response (default is False).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        params = {
            'expand': expand,
            'includeDeactivated': include_deactivated
        }
        return self.client.get(self.BASE_URL, "/", params=params, raw=raw)
