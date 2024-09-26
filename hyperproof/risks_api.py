# risks_api.py
# 
# This module provides functionality for interacting with the Risks API of Hyperproof.
# Author: Virgil Vaduva
# Timestamp: 2024-09-25
# License: This project is licensed under the GNU General Public License (GPL).
#
# Description:
# The RisksAPI class is responsible for handling interactions with the Risks API,
# allowing for operations such as retrieving, adding, filtering, and updating risks within an organization.

from .utils import logger
from .users_api import UsersAPI

class RisksAPI:
    """
    This class handles interactions with the Risks API of Hyperproof.
    It allows retrieving, adding, filtering, and updating risks in an organization.
    """
    BASE_URL = "https://api.hyperproof.app/v1/risks"

    def __init__(self, api_client):
        # Use the shared API client
        self.client = api_client
        self.users_api = UsersAPI(api_client)

    def get_risks(self, risk_register_id=None, status=None, raw=False):
        """
        Retrieves all risks for the organization with optional filters by risk register or status.

        :param risk_register_id: The unique ID of the risk register (optional).
        :param status: Filter by the status of the risks (optional, e.g., 'active', 'archived').
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        params = {
            'riskRegisterId': risk_register_id,
            'status': status
        }
        return self.client.get(self.BASE_URL, "/", params=params, raw=raw)

    def add_risk(self, risk_register_id, risk_identifier, name, description, category, response,
                 likelihood_level, likelihood_rationale, impact_level, impact_rationale,
                 tolerance_level, owner_id, custom_fields=None, raw=False):
        """
        Adds a new risk to an organization, with optional custom fields.

        :param risk_register_id: The unique ID of the risk register.
        :param risk_identifier: The identifier for the risk.
        :param name: Name of the risk.
        :param description: Description of the risk.
        :param category: Category of the risk.
        :param response: Risk response strategy (e.g., 'mitigate', 'accept').
        :param likelihood_level: Likelihood level (e.g., 1-5).
        :param likelihood_rationale: Explanation for the likelihood level.
        :param impact_level: Impact level (e.g., 1-5).
        :param impact_rationale: Explanation for the impact level.
        :param tolerance_level: Tolerance level for the risk.
        :param owner_id: The owner ID for the risk.
        :param custom_fields: Optional custom fields associated with the risk.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        data = {
            "riskRegisterId": risk_register_id,
            "riskIdentifier": risk_identifier,
            "name": name,
            "description": description,
            "category": category,
            "response": response,
            "likelihoodLevel": likelihood_level,
            "likelihoodRationale": likelihood_rationale,
            "impactLevel": impact_level,
            "impactRationale": impact_rationale,
            "toleranceLevel": tolerance_level,
            "ownerId": owner_id,
            "customFields": custom_fields or []
        }
        return self.client.post(self.BASE_URL, "/", data=data, raw=raw)

    def get_risk_by_id(self, risk_id, raw=False):
        """
        Retrieves a specific risk by its unique ID.

        :param risk_id: The unique ID of the risk.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        return self.client.get(self.BASE_URL, f"/{risk_id}", raw=raw)

    def update_risk(self, risk_id, name=None, description=None, category=None, response=None,
                    likelihood_level=None, likelihood_rationale=None, impact_level=None,
                    impact_rationale=None, tolerance_level=None, status=None, owner_id=None,
                    custom_fields=None, clear_category=False, clear_likelihood_level=False,
                    clear_impact_level=False, clear_tolerance_level=False, raw=False):
        """
        Updates an existing risk with new values, with support for clearing certain fields.

        :param risk_id: The unique ID of the risk.
        :param name: Updated name of the risk (optional).
        :param description: Updated description of the risk (optional).
        :param category: Updated category of the risk (optional).
        :param response: Updated risk response strategy (optional).
        :param likelihood_level: Updated likelihood level (optional).
        :param likelihood_rationale: Updated explanation for likelihood level (optional).
        :param impact_level: Updated impact level (optional).
        :param impact_rationale: Updated explanation for impact level (optional).
        :param tolerance_level: Updated tolerance level (optional).
        :param status: Updated status of the risk (optional, e.g., 'active', 'archived').
        :param owner_id: Updated owner ID for the risk (optional).
        :param custom_fields: Optional custom fields associated with the risk.
        :param clear_category: If True, clears the category field.
        :param clear_likelihood_level: If True, clears the likelihood level field.
        :param clear_impact_level: If True, clears the impact level field.
        :param clear_tolerance_level: If True, clears the tolerance level field.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        data = {
            "name": name,
            "description": description,
            "category": None if clear_category else category,
            "response": response,
            "likelihoodLevel": None if clear_likelihood_level else likelihood_level,
            "likelihoodRationale": likelihood_rationale,
            "impactLevel": None if clear_impact_level else impact_level,
            "impactRationale": impact_rationale,
            "toleranceLevel": None if clear_tolerance_level else tolerance_level,
            "status": status,
            "ownerId": owner_id,
            "customFields": custom_fields or []
        }
        return self.client.patch(self.BASE_URL, f"/{risk_id}", data=data, raw=raw)

    def filter_risks(self, risk_ids=None, modified_after=None, status=None, raw=False):
        """
        Filters risks based on a set of criteria like risk IDs, modification date, and status.

        :param risk_ids: List of risk IDs to filter by (optional).
        :param modified_after: Only return risks modified after this date (optional).
        :param status: Filter by risk status (optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        data = {
            "riskIds": risk_ids or [],
            "modifiedAfter": modified_after,
            "status": status
        }
        return self.client.put(self.BASE_URL, "/filter", data=data, raw=raw)

    def get_risks_by_user(self, userid=None, givenName=None, surname=None, raw=False):
        """
        Retrieve risks associated with a user based on userid, givenName, or surname.

        :param userid: The unique identifier of the user (optional).
        :param givenName: The given name of the user (optional).
        :param surname: The surname of the user (optional).
        :param raw: If True, return raw response; otherwise return parsed JSON.
        :return: List of risks associated with the specified user(s).
        """
        # Get all organization users
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

        all_risks = self.get_risks(raw=False)

        user_risks = []
        for risk in all_risks:
            owner_id = risk.get('ownerId')
            for user in filtered_users:
                if owner_id == user.get('id') or owner_id == user.get('userId'):
                    user_risks.append(risk)
                    break

        if raw:
            return self.client.get(self.BASE_URL, "/", raw=True)
        else:
            return user_risks
