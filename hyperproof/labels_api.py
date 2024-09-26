# labels_api.py
# 
# This module provides functionality for interacting with the Labels API of Hyperproof.
# Author: Virgil Vaduva
# Timestamp: 2024-09-25
# License: This project is licensed under the GNU General Public License (GPL).
#
# Description:
# The LabelsAPI class is responsible for handling interactions with the Labels API,
# allowing for operations related to labels such as retrieving, adding, and updating labels.

from .utils import logger
from .users_api import UsersAPI

class LabelsAPI:
    """
    This class handles interactions with the Labels API of Hyperproof.
    """
    BASE_URL = "https://api.hyperproof.app/v1/labels"

    def __init__(self, api_client):
        # Use the shared API client
        self.client = api_client
        self.users_api = UsersAPI(api_client)

    def get_labels(self, can_link=None, status=None, raw=False):
        """
        Retrieve all labels in the organization with optional filters.

        :param can_link: Filter by link permission (optional).
        :param status: Filter by label status (optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format.
        """
        params = {
            'canLink': can_link,
            'status': status
        }
        return self.client.get(self.BASE_URL, "/", params=params, raw=raw)

    def get_label_by_id(self, label_id, raw=False):
        """
        Retrieve a specific label by its unique ID.

        :param label_id: The ID of the label to retrieve.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: JSON response of the label.
        """
        return self.client.get(self.BASE_URL, f"/{label_id}", raw=raw)

    def get_label_summaries(self, can_link=None, status=None, raw=False):
        """
        Retrieve label summaries for the organization with optional filters.

        :param can_link: Filter by link permission (optional).
        :param status: Filter label summaries by their status (optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format.
        """
        params = {
            'canLink': can_link,
            'status': status
        }
        return self.client.get(self.BASE_URL, "/summaries", params=params, raw=raw)

    def add_label(self, name, description, raw=False):
        """
        Add a new label to the organization.

        :param name: Name of the label.
        :param description: A brief description of the label.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data of the newly added label.
        """
        data = {
            "name": name,
            "description": description
        }
        return self.client.post(self.BASE_URL, "/", data, raw=raw)

    def update_label(self, label_id, **kwargs):
        """
        Update an existing label with new values.

        :param label_id: The unique ID of the label to update.
        :param kwargs: Key-value pairs of the fields to update.
        :return: JSON response of the updated label.
        """
        return self.client.patch(self.BASE_URL, f"/{label_id}", kwargs)

    def add_label_proof(self, label_id, file_path, raw=False):
        """
        Add a proof item to a label.

        :param label_id: The unique ID of the label.
        :param file_path: Path to the file to upload as proof.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data of the newly uploaded proof.
        """
        with open(file_path, 'rb') as file:
            files = {'file': file}
            return self.client.post(self.BASE_URL, f"/{label_id}/proof", files=files, raw=raw)


    def get_labels_by_user(self, userid=None, givenName=None, surname=None, raw=False):
        """
        Retrieve labels associated with a user based on userid, givenName, or surname.

        :param userid: The unique identifier of the user (optional).
        :param givenName: The given name of the user (optional).
        :param surname: The surname of the user (optional).
        :param raw: If True, return raw response; otherwise return parsed JSON.
        :return: List of labels associated with the specified user(s).
        """
        org_users = self.users_api.get_organization_users(raw=False)

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
            return [] if not raw else self.client.get(self.BASE_URL, "/", raw=True)

        all_labels = self.get_labels(raw=False)

        user_labels = []
        for label in all_labels:
            created_by = label.get('createdBy')
            for user in filtered_users:
                if created_by == user.get('id') or created_by == user.get('userId'):
                    user_labels.append(label)
                    break

        if raw:
            return self.client.get(self.BASE_URL, "/", raw=True)
        else:
            return user_labels
