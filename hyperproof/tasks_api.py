# tasks_api.py
# 
# This module provides functionality for interacting with the Tasks API of Hyperproof.
# Author: Virgil Vaduva
# Timestamp: 2024-09-25
# License: This project is licensed under the GNU General Public License (GPL).
#
# Description:
# The TasksAPI class is responsible for handling interactions with the Tasks API,
# allowing for operations such as creating, retrieving, updating tasks, and handling task-related proofs.

from .users_api import UsersAPI
from .utils import logger
from .task_statuses_api import TaskStatusesAPI

class TasksAPI:
    """
    This class handles interactions with the Tasks API of Hyperproof.
    It allows for creating, retrieving, updating tasks, and handling task-related proofs.
    """
    BASE_URL = "https://api.hyperproof.app/v1/tasks"
    
    def __init__(self, api_client):
        # Use the shared API client
        self.client = api_client
        self.users_api = UsersAPI(api_client)
        self.task_statuses_api = TaskStatusesAPI(api_client)
     
    def add_task(self, title, target_object, description, assignee_id, priority, due_date, has_integration=False, raw=False):
        """
        Adds a new task to an organization.

        :param title: Title of the task.
        :param target_object: Target object (includes objectId and objectType).
        :param description: Description of the task.
        :param assignee_id: ID of the assignee.
        :param priority: Priority of the task ('highest', 'high', 'medium', 'low', 'lowest').
        :param due_date: Due date of the task (ISO 8601 format).
        :param has_integration: Boolean indicating if the task has an integration (default is False).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        data = {
            "title": title,
            "targetObject": target_object,
            "description": description,
            "assigneeId": assignee_id,
            "priority": priority,
            "dueDate": due_date,
            "hasIntegration": has_integration
        }
        return self.client.post(self.BASE_URL, "/", data=data, raw=raw)

    def get_task_by_id(self, task_id, raw=False):
        """
        Retrieves a task in an organization by ID.

        :param task_id: The unique ID of the task to retrieve.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        logger.debug(f"Getting task by ID: {task_id}")
        response = self.client.get(self.BASE_URL, f"/{task_id}", raw=raw)
        logger.debug(f"Get task response: {response}")
        return response

    def update_task(self, task_id, title=None, description=None, assignee_id=None, target_id=None, target_type=None,
                    task_status_id=None, priority=None, sort_order=None, due_date=None, raw=False):
        """
        Updates an existing task with new values.

        :param task_id: The unique ID of the task to update.
        :param title: New title for the task (optional).
        :param description: New description of the task (optional).
        :param assignee_id: New assignee ID (optional).
        :param target_id: New target object ID (optional).
        :param target_type: New target object type (optional).
        :param task_status_id: New task status ID (optional).
        :param priority: New priority of the task ('highest', 'high', 'medium', 'low', 'lowest', optional).
        :param sort_order: New sort order (optional).
        :param due_date: New due date (ISO 8601 format, optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        data = {
            "title": title,
            "description": description,
            "assigneeId": assignee_id,
            "targetId": target_id,
            "targetType": target_type,
            "taskStatusId": task_status_id,
            "priority": priority,
            "sortOrder": sort_order,
            "dueDate": due_date
        }
        return self.client.patch(self.BASE_URL, f"/{task_id}", data=data, raw=raw)

    def add_task_proof(self, task_id, file_path, proof_owned_by=None, proof_source=None, proof_source_id=None,
                       proof_source_file_id=None, proof_source_modified_on=None, proof_live_sync_enabled=False, raw=False):
        """
        Adds a proof item to a task.

        :param task_id: The unique ID of the task.
        :param file_path: Path to the proof file to upload.
        :param proof_owned_by: ID of the proof owner (optional).
        :param proof_source: Source of the proof (optional).
        :param proof_source_id: ID of the proof source (optional).
        :param proof_source_file_id: Source file ID of the proof (optional).
        :param proof_source_modified_on: Date and time the proof was modified (ISO 8601 format, optional).
        :param proof_live_sync_enabled: Whether live sync is enabled for the proof (optional, default is False).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        with open(file_path, 'rb') as file:
            files = {'proof': file}
            data = {
                "hp-proof-owned-by": proof_owned_by,
                "hp-proof-source": proof_source,
                "hp-proof-source-id": proof_source_id,
                "hp-proof-source-file-id": proof_source_file_id,
                "hp-proof-source-modified-on": proof_source_modified_on,
                "hp-proof-live-sync-enabled": proof_live_sync_enabled
            }
            return self.client.post(self.BASE_URL, f"/{task_id}/proof", files=files, data=data, raw=raw)

    def get_task_proof_metadata(self, task_id, raw=False):
        """
        Retrieves the proof metadata associated with a task.

        :param task_id: The unique ID of the task.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        return self.client.get(self.BASE_URL, f"/{task_id}/proof", raw=raw)

    def filter_tasks(self, target_object_type=None, target_object_ids=None, task_ids=None, assignee_ids=None, assignee_id=None, modified_after=None, raw=False):
        """
        Gets the set of tasks matching the supplied filter.

        :param target_object_type: Type of the target object (optional).
        :param target_object_ids: List of target object IDs to filter by (optional).
        :param task_ids: List of task IDs to filter by (optional).
        :param assignee_ids: List of assignee IDs to filter by (optional).
        :param assignee_id: Single assignee ID to filter by (optional).
        :param modified_after: Return tasks modified after this date (ISO 8601 format, optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        data = {}

        # Ensure target_object_type is added if provided
        if target_object_type:
            data["targetObjectType"] = target_object_type

        # Convert single values to lists for target_object_ids and task_ids
        if target_object_ids:
            data["targetObjectIds"] = target_object_ids if isinstance(target_object_ids, list) else [target_object_ids]
        
        if task_ids:
            data["taskIds"] = task_ids if isinstance(task_ids, list) else [task_ids]

        # Conflate assignee_ids and assignee_id into one list
        if assignee_ids and not isinstance(assignee_ids, list):
            assignee_ids = [assignee_ids]
        
        if assignee_id:
            if not assignee_ids:
                assignee_ids = [assignee_id]
            else:
                assignee_ids.append(assignee_id)

        if assignee_ids:
            data["assigneeIds"] = assignee_ids

        # Add modifiedAfter if provided
        if modified_after:
            data["modifiedAfter"] = modified_after

        logger.debug(f"Filter data: {data}")
        
        # Send the PUT request with the constructed filter data
        response = self.client.put(self.BASE_URL, "/filter", data=data, raw=raw)
        logger.debug(f"Filter tasks response: {response}")
        
        return response


    def get_task_comments(self, task_id, raw=False):
        """
        Retrieves the comments in a task's activity feed.

        :param task_id: The unique ID of the task.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        return self.client.get(self.BASE_URL, f"/{task_id}/comments", raw=raw)

    def add_task_comment(self, task_id, comment_text_formatted, is_internal_comment=False, object_type="task", object_id=None, raw=False):
        """
        Adds a comment to a task's activity feed.

        :param task_id: The unique ID of the task.
        :param comment_text_formatted: Formatted comment text.
        :param is_internal_comment: Whether it's an internal comment (default is False).
        :param object_type: Type of the object associated with the comment (default is 'task').
        :param object_id: The object ID associated with the comment (optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        data = {
            "commentTextFormatted": comment_text_formatted,
            "isInternalComment": is_internal_comment,
            "objectType": object_type,
            "objectId": object_id
        }
        return self.client.post(self.BASE_URL, f"/{task_id}/comments", data=data, raw=raw)

    def update_task_comment(self, task_id, comment_id, comment_text_formatted=None, is_internal_comment=None, object_type="task", object_id=None, raw=False):
        """
        Updates an existing comment in a task's activity feed.

        :param task_id: The unique ID of the task.
        :param comment_id: The unique ID of the comment.
        :param comment_text_formatted: Updated formatted comment text (optional).
        :param is_internal_comment: Updated internal comment flag (optional).
        :param object_type: Type of the object associated with the comment (default is 'task').
        :param object_id: The object ID associated with the comment (optional).
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        data = {
            "commentTextFormatted": comment_text_formatted,
            "isInternalComment": is_internal_comment,
            "objectType": object_type,
            "objectId": object_id
        }
        return self.client.patch(self.BASE_URL, f"/{task_id}/comments/{comment_id}", data=data, raw=raw)

    def delete_task_comment(self, task_id, comment_id, raw=False):
        """
        Deletes an existing comment in a task's activity feed.

        :param task_id: The unique ID of the task.
        :param comment_id: The unique ID of the comment.
        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        return self.client.delete(self.BASE_URL, f"/{task_id}/comments/{comment_id}", raw=raw)
    
    def get_tasks_by_user(self, user_id=None, first_name=None, surname=None):
        logger.debug(f"Getting tasks by user. User ID: {user_id}, First Name: {first_name}, Surname: {surname}")
        users = self.users_api.get_organization_users()
        logger.debug(f"Retrieved {len(users)} users")

        filtered_users = []
        for user in users:
            if user_id and user.get('userId') == user_id:
                filtered_users.append(user)
            elif first_name and surname:
                if user.get('givenName') == first_name and user.get('surname') == surname:
                    filtered_users.append(user)
            elif first_name and user.get('givenName') == first_name:
                filtered_users.append(user)
            elif surname and user.get('surname') == surname:
                filtered_users.append(user)

        logger.debug(f"Filtered {len(filtered_users)} users")

        if not filtered_users:
            logger.warning("No users found matching the given criteria")
            return {"error": "No users found matching the given criteria"}

        all_tasks = []
        for user in filtered_users:
            logger.debug(f"Getting tasks for user: {user.get('id')}")
            tasks = self.filter_tasks(assignee_ids=[user['id']], target_object_type="domain")
            logger.debug(f"Retrieved {len(tasks) if tasks else 0} tasks for user {user.get('id')}")
            if tasks:
                all_tasks.extend(tasks)

        if not all_tasks:
            logger.warning("No tasks found for the specified user(s)")
            return {"error": "No tasks found for the specified user(s)"}

        logger.debug(f"Returning {len(all_tasks)} tasks in total")
        return all_tasks

    def get_all_tasks(self, raw=False):
        """
        Retrieves all tasks by iterating through all users in the organization,
        and gathering each user's tasks using filter_tasks.

        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: All tasks combined from various calls.
        """
        all_tasks = []

        # Step 1: Retrieve all users in the organization
        users = self.users_api.get_organization_users()
        if not users:
            logger.warning("No users found.")
            return {"error": "No users found."}

        # Step 2: Iterate through each user and retrieve their tasks
        for user in users:
            user_id = user.get('id')
            if not user_id:
                continue

            # Use the user ID as a list in the filter
            tasks_for_user = self.filter_tasks(
                assignee_ids=[user_id],  # Always pass user_id as a list
                raw=raw
            )
            
            logger.debug(f"Retrieved {len(tasks_for_user) if tasks_for_user else 0} tasks for user {user_id}")
            
            if tasks_for_user:
                all_tasks.extend(tasks_for_user)

        # Step 3: Check if any tasks were found
        if not all_tasks:
            logger.warning("No tasks found.")
            return {"error": "No tasks found."}

        logger.debug(f"Total tasks retrieved: {len(all_tasks)}")
        return all_tasks


        
    def get_all_tasks_by_status(self, raw=False):
        all_tasks = []

        task_statuses = self.task_statuses_api.get_task_statuses()
        if not task_statuses:
            logger.warning("No task statuses found.")
            return {"error": "No task statuses found."}

        # Loop through each status to filter tasks by status
        for status in task_statuses:
            status_id = status.get('id')  # or use the name field if that's easier
            tasks_for_status = self.filter_tasks(task_status_id=status_id, raw=raw)
            logger.debug(f"Retrieved {len(tasks_for_status) if tasks_for_status else 0} tasks for status {status['name']}")
            
            if tasks_for_status:
                all_tasks.extend(tasks_for_status)

        if not all_tasks:
            logger.warning("No tasks found.")
            return {"error": "No tasks found."}

        return all_tasks

