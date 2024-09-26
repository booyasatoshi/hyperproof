# programs_api.py
# 
# This module provides functionality for interacting with the Programs API of Hyperproof.
# Author: Virgil Vaduva
# Timestamp: 2024-09-25
# License: This project is licensed under the GNU General Public License (GPL).
#
# Description:
# The ProgramsAPI class is responsible for handling interactions with the Programs API,
# allowing for operations such as retrieving, adding, and updating programs within an organization.

from .utils import logger

class ProgramsAPI:
    """
    This class handles interactions with the Programs API of Hyperproof.
    It allows retrieving, adding, and updating programs within an organization.
    """
    BASE_URL = "https://api.hyperproof.app/v1/programs"

    def __init__(self, api_client):
        # Use the shared API client
        self.client = api_client

    def get_programs(self, status=None, raw=False):
        """
        Retrieves all programs for the organization with an optional status filter.

        :param status: Filter by program status (e.g., 'operating', 'defining').
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        params = {
            'status': status
        }
        return self.client.get(self.BASE_URL, "/", params=params, raw=raw)

    def add_program(self, name, description, section_root_id, primary_contact_id, work_status="defining",
                    source_template_id=None, selected_baselines=None, jumpstart_program_ids=None,
                    clone_program_name=None, framework_license_notice=None, raw=False):
        """
        Adds a new program to the organization.

        :param name: The name of the program.
        :param description: A brief description of the program.
        :param section_root_id: The section root ID associated with the program.
        :param primary_contact_id: The ID of the primary contact for the program.
        :param work_status: The current work status (default is 'defining').
        :param source_template_id: The template ID used for creating the program (optional).
        :param selected_baselines: Baselines selected for the program (optional).
        :param jumpstart_program_ids: Jumpstart program IDs (optional).
        :param clone_program_name: Name of the program to be cloned (optional).
        :param framework_license_notice: Framework license notice (optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        data = {
            "name": name,
            "description": description,
            "sectionRootId": section_root_id,
            "primaryContactId": primary_contact_id,
            "workStatus": work_status,
            "sourceTemplateId": source_template_id,
            "selectedBaselines": selected_baselines or [],
            "jumpstartProgramIds": jumpstart_program_ids or [],
            "cloneProgramName": clone_program_name,
            "frameworkLicenseNotice": framework_license_notice
        }
        return self.client.post(self.BASE_URL, "/", data=data, raw=raw)

    def get_program_by_id(self, program_id, raw=False):
        """
        Retrieves a specific program by its unique ID.

        :param program_id: The unique ID of the program.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        return self.client.get(self.BASE_URL, f"/{program_id}", raw=raw)

    def update_program(self, program_id, name=None, description=None, work_status=None,
                       override_health=None, override_health_health=None, override_health_by=None,
                       override_health_reason=None, selected_baselines=None, baseline_enabled=None,
                       framework_version_mapping_id=None, removed_requirement_ids=None,
                       updated_requirement_ids=None, clone_program_name=None, is_update_complete=None, raw=False):
        """
        Updates an existing program by its unique ID.

        :param program_id: The unique ID of the program.
        :param name: The new name of the program (optional).
        :param description: The new description of the program (optional).
        :param work_status: Updated work status (e.g., 'defining', 'operating', optional).
        :param override_health: Whether to override health (optional).
        :param override_health_health: Health status to override (e.g., 'critical', 'healthy', optional).
        :param override_health_by: ID of the person overriding health (optional).
        :param override_health_reason: Reason for health override (optional).
        :param selected_baselines: Updated baselines (optional).
        :param baseline_enabled: Whether baseline is enabled (optional).
        :param framework_version_mapping_id: Framework version mapping ID (optional).
        :param removed_requirement_ids: List of removed requirement IDs (optional).
        :param updated_requirement_ids: List of updated requirement IDs (optional).
        :param clone_program_name: Name of the program to be cloned (optional).
        :param is_update_complete: Whether the update is complete (optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        data = {
            "name": name,
            "description": description,
            "workStatus": work_status,
            "overrideHealth": override_health,
            "overrideHealthHealth": override_health_health,
            "overrideHealthBy": override_health_by,
            "overrideHealthReason": override_health_reason,
            "selectedBaselines": selected_baselines or [],
            "baselineEnabled": baseline_enabled,
            "frameworkVersionMappingId": framework_version_mapping_id,
            "removedRequirementIds": removed_requirement_ids or [],
            "updatedRequirementIds": updated_requirement_ids or [],
            "cloneProgramName": clone_program_name,
            "isUpdateComplete": is_update_complete
        }
        return self.client.patch(self.BASE_URL, f"/{program_id}", data=data, raw=raw)
