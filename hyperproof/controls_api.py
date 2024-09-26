# controls_api.py
# 
# This module provides functionality for interacting with the Controls API of Hyperproof.
# Author: Virgil Vaduva
# Timestamp: 2024-09-25
# License: This project is licensed under the GNU General Public License (GPL).
#
# Description:
# The ControlsAPI class is responsible for handling interactions with the Controls API.
# It manages control-related operations such as retrieving, updating, and adding controls.

from .utils import logger
from .users_api import UsersAPI

class ControlsAPI:
    """
    This class handles interactions with the Controls API of Hyperproof.
    """
    BASE_URL = "https://api.hyperproof.app/v1/controls"

    def __init__(self, api_client):
        # Use the shared API client
        self.client = api_client
        self.users_api = UsersAPI(api_client)


    def get_controls(self, can_link=None, expand_scopes=None, expand_teams=None, status=None, raw=False):
        """
        Retrieve all controls for the organization with optional filters.

        :param can_link: Filter by link permission (optional).
        :param expand_scopes: Whether to expand scopes (optional).
        :param expand_teams: Whether to expand teams (optional).
        :param status: Filter by control status (optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format.
        """
        params = {
            'canLink': can_link,
            'expandScopes': expand_scopes,
            'expandTeams': expand_teams,
            'status': status
        }
        return self.client.get(self.BASE_URL, "/", params=params, raw=raw)

    def get_control_by_id(self, control_id, raw=False):
        """
        Retrieve a specific control by its unique ID.

        :param control_id: The ID of the control to retrieve.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: JSON response of the control.
        """
        return self.client.get(self.BASE_URL, f"/{control_id}", raw=raw)

    def add_control(self, control_identifier, name, description, domain_name, owner, implementation="inProgress"):
        """
        Add a new control to the organization.

        :param control_identifier: The identifier for the control.
        :param name: Name of the control.
        :param description: Description of the control.
        :param domain_name: Domain under which the control falls.
        :param owner: Owner of the control.
        :param implementation: Implementation status (default is inProgress).
        :return: JSON response of the newly added control.
        """
        data = {
            "controlIdentifier": control_identifier,
            "name": name,
            "description": description,
            "domainName": domain_name,
            "implementation": implementation,
            "owner": owner
        }
        return self.client.post(self.BASE_URL, "/", data)

    # New methods added below

    def get_control_summaries(self, can_link=None, status=None, raw=False):
        """
        Retrieve control summaries for the organization with optional filters.

        :param can_link: Filter by link permission (optional).
        :param status: Filter by control status (optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: JSON response of control summaries.
        """
        params = {
            'canLink': can_link,
            'status': status
        }
        return self.client.get(self.BASE_URL, "/summaries", params=params, raw=raw)

    def update_control(self, control_id, **kwargs):
        """
        Update an existing control with new values.

        :param control_id: The unique ID of the control to update.
        :param kwargs: Key-value pairs of the fields to update.
        :return: JSON response of the updated control.
        """
        return self.client.patch(self.BASE_URL, f"/{control_id}", kwargs)

    def add_control_proof(self, control_id, file_path, raw=False):
        """
        Add a proof item to a control.

        :param control_id: The unique ID of the control.
        :param file_path: Path to the file to upload as proof.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data of the newly uploaded proof.
        """
        with open(file_path, 'rb') as file:
            files = {'file': file}
            return self.client.post(self.BASE_URL, f"/{control_id}/proof", files=files, raw=raw)

    def get_controls_by_user(self, userid=None, givenName=None, surname=None, raw=False):
        """
        Retrieve controls associated with a user based on userid, givenName, or surname.

        :param userid: The unique identifier of the user (optional).
        :param givenName: The given name of the user (optional).
        :param surname: The surname of the user (optional).
        :param raw: If True, return raw response; otherwise return parsed JSON.
        :return: List of controls associated with the specified user(s).
        """
        # Get all organization users
        org_users = self.users_api.get_organization_users(raw=False)

        if raw:
            return org_users

        filtered_users = []
        for user in org_users:
            if userid and (user.get('id') == userid or user.get('userId') == userid):
                filtered_users.append(user)
            elif givenName and surname:
                if user.get('givenName') == givenName and user.get('surname') == surname:
                    filtered_users.append(user)
            elif givenName and user.get('givenName') == givenName:
                filtered_users.append(user)
            elif surname and user.get('surname') == surname:
                filtered_users.append(user)

        if not filtered_users:
            return []

        all_controls = self.get_controls(raw=False)

        user_controls = []
        for control in all_controls:
            control_owner = control.get('owner', {})
            for user in filtered_users:
                if control_owner.get('id') == user.get('id') or control_owner.get('id') == user.get('userId'):
                    user_controls.append(control)
                    break

        return user_controls