# hyperproof/task_statuses_api.py
# from .utils import APIClient

class TaskStatusesAPI:
    """
    This class handles interactions with the Task Statuses API of Hyperproof.
    It allows retrieving the task status values in an organization.
    """
    BASE_URL = "https://api.hyperproof.app/v1/taskstatuses"

    def __init__(self, api_client):
        # Initialize the API client with authentication
        self.client = api_client

    def get_task_statuses(self, raw=False):
        """
        Retrieves the task statuses in an organization.

        :param raw: If True, return raw response text; otherwise return parsed JSON.
        :return: Response data in the desired format (raw or parsed JSON).
        """
        return self.client.get(self.BASE_URL, "/", raw=raw)
