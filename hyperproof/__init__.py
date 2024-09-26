import os
from dotenv import load_dotenv, find_dotenv
from functools import wraps

# Load environment variables
load_dotenv(find_dotenv())

# Get client credentials from environment variables
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Import API client and API classes
from .utils import APIClient
from .controls_api import ControlsAPI
from .proof_api import ProofAPI
from .labels_api import LabelsAPI
from .custom_apps_api import CustomAppsAPI
from .programs_api import ProgramsAPI
from .risks_api import RisksAPI
from .roles_api import RolesAPI
from .tasks_api import TasksAPI
from .task_statuses_api import TaskStatusesAPI
from .users_api import UsersAPI

# Create a single APIClient instance
_api_client = APIClient(client_id, client_secret)

class LazyAuth:
    def __init__(self, api_class):
        self.api_class = api_class
        self.instance = None

    def __getattr__(self, name):
        if self.instance is None:
            self.instance = self.api_class  # Already initialized with _api_client
        return getattr(self.instance, name)

def lazy_method(api, method_name):
    @wraps(getattr(api.api_class, method_name))
    def wrapper(*args, **kwargs):
        return getattr(api, method_name)(*args, **kwargs)
    return wrapper

# Create lazy instances, passing the shared APIClient to each API class
_controls_api = LazyAuth(ControlsAPI(_api_client))
_proof_api = LazyAuth(ProofAPI(_api_client))
_labels_api = LazyAuth(LabelsAPI(_api_client))
_custom_apps_api = LazyAuth(CustomAppsAPI(_api_client))
_programs_api = LazyAuth(ProgramsAPI(_api_client))
_risks_api = LazyAuth(RisksAPI(_api_client))
_roles_api = LazyAuth(RolesAPI(_api_client))
_tasks_api = LazyAuth(TasksAPI(_api_client))
_task_statuses_api = LazyAuth(TaskStatusesAPI(_api_client))
_users_api = LazyAuth(UsersAPI(_api_client))

# Explicitly expose all methods
# ControlsAPI methods
get_controls = lazy_method(_controls_api, 'get_controls')
get_control_summaries = lazy_method(_controls_api, 'get_control_summaries')
get_controls_by_user = lazy_method(_controls_api, 'get_controls_by_user')
update_control = lazy_method(_controls_api, 'update_control')
add_control_proof = lazy_method(_controls_api, 'add_control_proof')
get_control_by_id = lazy_method(_controls_api, 'get_control_by_id')
add_control = lazy_method(_controls_api, 'add_control')

# ProofAPI methods
get_proof_metadata_collection = lazy_method(_proof_api, 'get_proof_metadata_collection')
get_proof_contents = lazy_method(_proof_api, 'get_proof_contents')
get_proof_metadata = lazy_method(_proof_api, 'get_proof_metadata')
get_proof_by_user = lazy_method(_proof_api, 'get_proof_by_user')
get_proof_by_label = lazy_method(_proof_api, 'get_proof_by_label')
add_proof = lazy_method(_proof_api, 'add_proof')
add_proof_version = lazy_method(_proof_api, 'add_proof_version')

# LabelsAPI methods
get_labels = lazy_method(_labels_api, 'get_labels')
get_label_summaries = lazy_method(_labels_api, 'get_label_summaries')
get_label_by_id = lazy_method(_labels_api, 'get_label_by_id')
get_labels_by_user = lazy_method(_labels_api, 'get_labels_by_user')
add_label = lazy_method(_labels_api, 'add_label')
update_label = lazy_method(_labels_api, 'update_label')

# CustomAppsAPI methods
get_custom_apps = lazy_method(_custom_apps_api, 'get_custom_apps')
add_custom_app = lazy_method(_custom_apps_api, 'add_custom_app')
get_custom_app_by_id = lazy_method(_custom_apps_api, 'get_custom_app_by_id')
update_custom_app = lazy_method(_custom_apps_api, 'update_custom_app')
delete_custom_app = lazy_method(_custom_apps_api, 'delete_custom_app')
get_custom_app_events = lazy_method(_custom_apps_api, 'get_custom_app_events')
get_custom_app_stats = lazy_method(_custom_apps_api, 'get_custom_app_stats')

# ProgramsAPI methods
get_programs = lazy_method(_programs_api, 'get_programs')
get_program_by_id = lazy_method(_programs_api, 'get_program_by_id')
add_program = lazy_method(_programs_api, 'add_program')
update_program = lazy_method(_programs_api, 'update_program')

# RisksAPI methods
get_risks = lazy_method(_risks_api, 'get_risks')
get_risk_by_id = lazy_method(_risks_api, 'get_risk_by_id')
get_risks_by_user = lazy_method(_risks_api, 'get_risks_by_user')
add_risk = lazy_method(_risks_api, 'add_risk')
update_risk = lazy_method(_risks_api, 'update_risk')
filter_risks = lazy_method(_risks_api, 'filter_risks')

# TasksAPI methods
get_all_tasks = lazy_method(_tasks_api, 'get_all_tasks')
get_all_tasks_by_status = lazy_method(_tasks_api, 'get_all_tasks_by_status')
add_task = lazy_method(_tasks_api, 'add_task')
get_task_by_id = lazy_method(_tasks_api, 'get_task_by_id')
get_tasks_by_user = lazy_method(_tasks_api, 'get_tasks_by_user')
update_task = lazy_method(_tasks_api, 'update_task')
add_task_proof = lazy_method(_tasks_api, 'add_task_proof')
filter_tasks = lazy_method(_tasks_api, 'filter_tasks')
add_task_comment = lazy_method(_tasks_api, 'add_task_comment')

# TaskStatusesAPI methods
get_task_statuses = lazy_method(_task_statuses_api, 'get_task_statuses')

# RolesAPI methods
get_roles = lazy_method(_roles_api, 'get_roles')

# UsersAPI methods
get_current_user = lazy_method(_users_api, 'get_current_user')
get_organization_users = lazy_method(_users_api, 'get_organization_users')

# List all exposed methods
__all__ = [
    'get_controls', 'get_control_summaries', 'get_controls_by_user', 
    'update_control', 'add_control_proof',
    'get_control_by_id', 'add_control', 'get_proof_metadata_collection',
    'get_proof_contents', 'get_proof_metadata', 'get_proof_by_user', 
    'add_proof', 'add_proof_version', 'get_proof_by_label',
    'get_labels', 'get_label_summaries', 'get_label_by_id', 'add_label', 'update_label', 'get_labels_by_user',
    'get_custom_apps', 'add_custom_app', 'get_custom_app_by_id', 'update_custom_app',
    'delete_custom_app', 'get_custom_app_events', 'get_custom_app_stats',
    'get_programs', 'get_program_by_id', 'add_program', 'update_program',
    'get_risks', 'get_risk_by_id', 'get_risks_by_user', 'add_risk', 'update_risk', 
    'filter_risks', 'get_all_tasks', 'get_all_tasks_by_status',
    'add_task', 'get_task_by_id', 'get_tasks_by_user', 'update_task', 'add_task_proof',
    'filter_tasks', 'add_task_comment', 'get_task_statuses', 'get_roles',
    'get_current_user', 'get_organization_users'
]




# import os
# from dotenv import load_dotenv, find_dotenv
# from functools import wraps

# # Load environment variables
# load_dotenv(find_dotenv())

# # Get client credentials from environment variables
# client_id = os.getenv("CLIENT_ID")
# client_secret = os.getenv("CLIENT_SECRET")

# class LazyAuth:
#     def __init__(self, api_class):
#         self.api_class = api_class
#         self.instance = None

#     def __getattr__(self, name):
#         if self.instance is None:
#             self.instance = self.api_class(client_id, client_secret)
#         return getattr(self.instance, name)

# def lazy_method(api, method_name):
#     @wraps(getattr(api.api_class, method_name))
#     def wrapper(*args, **kwargs):
#         return getattr(api, method_name)(*args, **kwargs)
#     return wrapper

# # Import API classes
# from .controls_api import ControlsAPI
# from .proof_api import ProofAPI
# from .labels_api import LabelsAPI
# from .custom_apps_api import CustomAppsAPI
# from .programs_api import ProgramsAPI
# from .risks_api import RisksAPI
# from .roles_api import RolesAPI
# from .tasks_api import TasksAPI
# from .task_statuses_api import TaskStatusesAPI
# from .users_api import UsersAPI

# # Create lazy instances
# _controls_api = LazyAuth(ControlsAPI)
# _proof_api = LazyAuth(ProofAPI)
# _labels_api = LazyAuth(LabelsAPI)
# _custom_apps_api = LazyAuth(CustomAppsAPI)
# _programs_api = LazyAuth(ProgramsAPI)
# _risks_api = LazyAuth(RisksAPI)
# _roles_api = LazyAuth(RolesAPI)
# _tasks_api = LazyAuth(TasksAPI)
# _task_statuses_api = LazyAuth(TaskStatusesAPI)
# _users_api = LazyAuth(UsersAPI)

# # Explicitly expose all methods
# # ControlsAPI methods
# get_controls = lazy_method(_controls_api, 'get_controls')
# get_control_summaries = lazy_method(_controls_api, 'get_control_summaries')
# get_controls_by_user = lazy_method(_controls_api, 'get_controls_by_user')
# update_control = lazy_method(_controls_api, 'update_control')
# add_control_proof = lazy_method(_controls_api, 'add_control_proof')
# get_control_by_id = lazy_method(_controls_api, 'get_control_by_id')
# add_control = lazy_method(_controls_api, 'add_control')

# # ProofAPI methods
# get_proof_metadata_collection = lazy_method(_proof_api, 'get_proof_metadata_collection')
# get_proof_contents = lazy_method(_proof_api, 'get_proof_contents')
# get_proof_metadata = lazy_method(_proof_api, 'get_proof_metadata')
# get_proof_by_user = lazy_method(_proof_api, 'get_proof_by_user')
# get_proof_by_label = lazy_method(_proof_api, 'get_proof_by_label')
# add_proof = lazy_method(_proof_api, 'add_proof')
# add_proof_version = lazy_method(_proof_api, 'add_proof_version')

# # LabelsAPI methods
# get_labels = lazy_method(_labels_api, 'get_labels')
# get_label_summaries = lazy_method(_labels_api, 'get_label_summaries')
# get_label_by_id = lazy_method(_labels_api, 'get_label_by_id')
# get_labels_by_user = lazy_method(_labels_api, 'get_labels_by_user')
# add_label = lazy_method(_labels_api, 'add_label')
# update_label = lazy_method(_labels_api, 'update_label')

# # CustomAppsAPI methods
# get_custom_apps = lazy_method(_custom_apps_api, 'get_custom_apps')
# add_custom_app = lazy_method(_custom_apps_api, 'add_custom_app')
# get_custom_app_by_id = lazy_method(_custom_apps_api, 'get_custom_app_by_id')
# update_custom_app = lazy_method(_custom_apps_api, 'update_custom_app')
# delete_custom_app = lazy_method(_custom_apps_api, 'delete_custom_app')
# get_custom_app_events = lazy_method(_custom_apps_api, 'get_custom_app_events')
# get_custom_app_stats = lazy_method(_custom_apps_api, 'get_custom_app_stats')

# # ProgramsAPI methods
# get_programs = lazy_method(_programs_api, 'get_programs')
# get_program_by_id = lazy_method(_programs_api, 'get_program_by_id')
# add_program = lazy_method(_programs_api, 'add_program')
# update_program = lazy_method(_programs_api, 'update_program')

# # RisksAPI methods
# get_risks = lazy_method(_risks_api, 'get_risks')
# get_risk_by_id = lazy_method(_risks_api, 'get_risk_by_id')
# get_risks_by_user = lazy_method(_risks_api, 'get_risks_by_user')
# add_risk = lazy_method(_risks_api, 'add_risk')
# update_risk = lazy_method(_risks_api, 'update_risk')
# filter_risks = lazy_method(_risks_api, 'filter_risks')

# # TasksAPI methods
# get_all_tasks = lazy_method(_tasks_api, 'get_all_tasks')
# get_all_tasks_by_status = lazy_method(_tasks_api, 'get_all_tasks_by_status')
# add_task = lazy_method(_tasks_api, 'add_task')
# get_task_by_id = lazy_method(_tasks_api, 'get_task_by_id')
# get_tasks_by_user = lazy_method(_tasks_api, 'get_tasks_by_user')
# update_task = lazy_method(_tasks_api, 'update_task')
# add_task_proof = lazy_method(_tasks_api, 'add_task_proof')
# filter_tasks = lazy_method(_tasks_api, 'filter_tasks')
# add_task_comment = lazy_method(_tasks_api, 'add_task_comment')

# # TaskStatusesAPI methods
# get_task_statuses = lazy_method(_task_statuses_api, 'get_task_statuses')

# # RolesAPI methods
# get_roles = lazy_method(_roles_api, 'get_roles')

# # UsersAPI methods
# get_current_user = lazy_method(_users_api, 'get_current_user')
# get_organization_users = lazy_method(_users_api, 'get_organization_users')

# # List all exposed methods
# __all__ = [
#     'get_controls', 'get_control_summaries', 'get_controls_by_user', 
#     'update_control', 'add_control_proof',
#     'get_control_by_id', 'add_control', 'get_proof_metadata_collection',
#     'get_proof_contents', 'get_proof_metadata', 'get_proof_by_user', 
#     'add_proof', 'add_proof_version', 'get_proof_by_label',
#     'get_labels', 'get_label_summaries', 'get_label_by_id', 'add_label', 'update_label', 'get_labels_by_user',
#     'get_custom_apps', 'add_custom_app', 'get_custom_app_by_id', 'update_custom_app',
#     'delete_custom_app', 'get_custom_app_events', 'get_custom_app_stats',
#     'get_programs', 'get_program_by_id', 'add_program', 'update_program',
#     'get_risks', 'get_risk_by_id', 'get_risks_by_user', 'add_risk', 'update_risk', 
#     'filter_risks', 'get_all_tasks', 'get_all_tasks_by_status',
#     'add_task', 'get_task_by_id', 'get_tasks_by_user', 'update_task', 'add_task_proof',
#     'filter_tasks', 'add_task_comment', 'get_task_statuses', 'get_roles',
#     'get_current_user', 'get_organization_users'
# ]

