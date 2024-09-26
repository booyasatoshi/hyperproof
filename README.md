# Hyperproof API Wrapper Documentation

This repository provides a Python wrapper for interacting with Hyperproof’s Governance, Risk, and Compliance (GRC) platform. It includes complete support for all [Hyperproof APIs](https://developer.hyperproof.app/apis) and all the methods contained therein, allowing developers to manage a Hyperproof instance and in addition, I extended the standard APIs with new [Features](#features) including new methods.  

This project came about mostly from my own needs attempting to build various custom integrations with the Hyperproof platform. There is a  lack of tools and support for Hyperproof custom development (outside of the SDK provided to build custom cloud-based integrations) and I personally have not seen any updates to the API codebase in the recent past. With that said, the tool is a great choice for GRC operations and I am hoping this Python wrapper will encourage Hyperproof to both update features in their APIs and help folks out there build the tools they need to integrate with Hyperproof.

The goal here is to expose the [Hyperproof APIs](https://developer.hyperproof.app/apis) to Python developers in an elegant way; you can see this in the example below using a newly implemented method:

```python
# This call will return a JSON object containing all proofs 
# matching labels containing the word Malware in the name

import hyperproof

proof = hyperproof.get_proof_by_label(label_name="Malware")
print(proof)
```
Or you can import just the method you need to use

```python
from hyperproof import get_proof_by_label 

proof = get_proof_by_label(label_name="Malware")
print(proof)
```

## Table of Contents

- [Features](#features)
  - [Brand new methods](#brand-new-methods)
  - [Using lazy instances](#using-lazy-instances)
  - [Comprehensive API support](#comprehensive-api-support)
  - [Error handling](#error-handling)
  - [Authentication](#authenticaton)
- [Known issues](#known-issues)
  - [Slow responses to API calls](#slow-responses-to-api-calls)
  - [Class instantiation improvements](#class-instantiation-improvements)
  - [Exception catching and logging](#exception-catching-and-logging)
- [Installation options](#installation-options)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
  - [General Usage](#general-usage)
  - [Fetching Controls](#fetching-controls)
  - [Adding Proof to a Task](#adding-proof-to-a-task)
  - [Managing Risks](#managing-risks)
  - [Using extended methods](#using-extended-methods)
- [Available APIs](#available-apis)
  - [Controls API](#controls-api)
  - [Proof API](#proof-api)
  - [Labels API](#labels-api)
  - [Programs API](#programs-api)
  - [Risks API](#risks-api)
  - [Tasks API](#tasks-api)
  - [Users API](#users-api)
  - [Task Statuses API](#task-statuses-api)
  - [Roles API](#roles-api)
  - [Custom Apps API](#custom-apps-api)
- [License](#license)

## Features
### Brand new API methods
Unfortunately, due to the lack of some features in the standard Hyperproof APIs, I had to extend the API wrapper and implement new methods to allow developers to correlate data from multiple API calls using just one method call. Using these methods will increase your API usage rate so be careful not to abuse them. The methods below are all new:

  - `get_controls_by_user` - Retrieve controls associated with a user based on userid, givenName, or surname.
  - `get_labels_by_user` - Retrieve labels associated with a user based on userid, givenName, or surname.
  - `get_proof_by_user` - Retrieve proofs associated with a user based on userid, givenName, surname, object_type, and object_id.
  - `get_proof_by_label` - Retrieve proofs associated with a specific label by label name (partial, case-insensitive match).
  - `get_risks_by_user` - Retrieve risks associated with a user based on userid, givenName, or surname. 
  - `get_tasks_by_user` - Retrieve tasks associated with a  user based on userid, givenName, or surname.
  - `get_all_tasks` - Retrieves all the tasks in the database.
  - `get_all_tasks_by_status` - Retrieve all tasks by status.

### Using lazy instances
Using a LazyAuth class to avoid repeated API calls to Hyperproof endpoints so that the lazy instances pass the shared APIClient to each API class. This will minimize the number of calls made to Hyperproof.

### Comprehensive API support
This wrapper covers all existing methods mapped 1:1 plus the new methods listed above.

### Error handling
The wrapper includes some logging and graceful error handling for failed API requests but it can use some improvements to catching exceptions, particularly related to using `requests`

### Authentication 
Handles OAuth 2.0 authentication with Hyperproof using client credentials.

## Known issues

### Slow responses to API calls
Unfortunately this is largely a problem on Hyperproof's end. I presume there is throttling in place and making multiple calls to multiple end points to retrieve large amounts of data and correlate data points will be slow. Reach out to your rep and talk to them about this issue.

### Class instantiation improvements
The constructor in ./hyperproof could likely be improved and instantiating classes particularly during OAuth authentication and passing the shared APIClient could be more efficient.

### Exception catching and logging
Logging is not fully implemented and improvements could be made to catch more exceptions.

## Installation options


1. **Using pip**

  The project is in PyPi so unless you want the repo, just run

  `pip install hyperproof`

2. **Clone the repository**:

  ```bash
  git clone https://github.com/booyasatoshi/hyperproof.git
  ```
  
  The wrapper only requires `requests` and `python-dotenv` so just run:

  ```bash
  pip install -r requirements.txt
  ```

## Configuration

This wrapper requires an access token to interact with the Hyperproof APIs. The `APIClient` class in the `utils.py` file handles authentication using OAuth 2.0. The access token is automatically fetched upon initialization.

The current implementation uses `dotenv` to load the credentials created in the Hyperproof web interface under Settings, API Clients; they are loaded from `.env` so please ensure a `.env` file exists in the root of your project and the entries are defined as below:

```python
CLIENT_ID="client_id"
CLIENT_SECRET="client_secret"
```
In a production environment use a more secure way to store credentials.

These credentials are passed to each API class when instantiated.

# General Usage

## Using the module

Using `pip install hyperproof` is the fastest way to install this module.  

Usage is pretty straight forward.  All the [Hyperproof APIs](https://developer.hyperproof.app/apis) and all methods and parameters therein are fully supported. You can import the module using `import hyperproof` (and then use methods via `hyperproof.method_name`) or `from hyperproof import method_name` (and then just call the method directly by name).

All methods are documented in detail below; and I recommend examining the examples included in the repo. 

I would appreciate contributions to this project so feel free to fork, improve, submit prs and help the community out.

### Fetching Controls

```python
import hyperproof

# Fetch all controls in the organization
controls = hyperproof.get_controls()
print(controls)
```

```python
# Fetch a specific control by control_id
control_id = "your-control-id"
control = controls_api.get_control_by_id(control_id="control-id")
print(control)
```

### Adding Proof to a Task

```python
from hyperproof import add_task_proof

# Add proof to a task
task_id = "your-task-id"
file_path = "/path/to/proof/file.pdf"
add_proof_request = add_task_proof(task_id, file_path)
print(add_proof_request)
```

### Managing Risks

```python
import hyperproof

# Add a new risk
risk = hyperproof.add_risk(
    risk_register_id="your-register-id",
    risk_identifier="RISK-001",
    name="Data Breach Risk",
    description="Potential for a data breach to occur",
    category="Security",
    response="mitigate",
    likelihood_level=5,
    likelihood_rationale="High likelihood based on past incidents",
    impact_level=4,
    impact_rationale="Severe impact on data and reputation",
    tolerance_level=3,
    owner_id="owner-id"
)
print(risk)
```

### Using extended methods

As I mentioned above, there are new methods implemented in this wrapper which are not natively available in the Hyperproof APIs. Until Hyperproof decides to improve their APIs, this is what is available:

  - `get_controls_by_user` - Retrieve controls associated with a user based on userid, givenName, or surname.
  - `get_labels_by_user` - Retrieve labels associated with a user based on userid, givenName, or surname.
  - `get_proof_by_user` - Retrieve proofs associated with a user based on userid, givenName, surname, object_type, and object_id.
  - `get_proof_by_label` - Retrieve proofs associated with a specific label by label name (partial, case-insensitive match).
  - `get_risks_by_user` - Retrieve risks associated with a user based on userid, givenName, or surname. 
  - `get_tasks_by_user` - Retrieve tasks associated with a  user based on userid, givenName, or surname.
  - `get_all_tasks` - Retrieves all the tasks in the database (this is an expensive call as we have to iterate through users and tasks to match the results)
  - `get_all_tasks_by_status` - Retrieve all tasks by status.

The methods use multiple API calls to retrieve data from multiple end points to correlate results and return the desired output back to the user. If you can identify more overlapping data points and fields to create new methods, feel free to let me know and I would be happy to add them.

# Available APIs

## Controls API

### Constructor

```python
def __init__(self, api_client)
```

- **Description**: Initializes the `ControlsAPI` class with the provided API client.
- **Parameters**:
  - `api_client`: An instance of the API client used to make requests.

## Methods

### `get_controls`

```python
def get_controls(can_link=None, expand_scopes=None, expand_teams=None, status=None, raw=False)
```

- **Description**: Retrieves all controls for the organization with optional filters.
- **Parameters**:
  - `can_link`: Filter by link permission (optional).
  - `expand_scopes`: Expand scopes in the response (optional).
  - `expand_teams`: Expand teams in the response (optional).
  - `status`: Filter by control status (optional).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON (default is `False`).
- **Returns**: Response data in JSON or raw text.

### `get_control_by_id`

```python
def get_control_by_id(control_id, raw=False)
```

- **Description**: Retrieves a specific control by its unique ID.
- **Parameters**:
  - `control_id`: The unique ID of the control to retrieve.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON (default is `False`).
- **Returns**: JSON response of the control or raw text.

### `add_control`

```python
def add_control(control_identifier, name, description, domain_name, owner, implementation="inProgress")
```

- **Description**: Adds a new control to the organization.
- **Parameters**:
  - `control_identifier`: The identifier for the control.
  - `name`: Name of the control.
  - `description`: Description of the control.
  - `domain_name`: Domain under which the control falls.
  - `owner`: Owner of the control.
  - `implementation`: Implementation status (default is `"inProgress"`).
- **Returns**: JSON response of the newly added control.

### `get_control_summaries`

```python
def get_control_summaries(can_link=None, status=None, raw=False)
```

- **Description**: Retrieves summaries of controls in the organization with optional filters.
- **Parameters**:
  - `can_link`: Filter by link permission (optional).
  - `status`: Filter by control status (optional).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON (default is `False`).
- **Returns**: JSON response of control summaries or raw text.

### `update_control`

```python
def update_control(control_id, **kwargs)
```

- **Description**: Updates an existing control with new values.
- **Parameters**:
  - `control_id`: The unique ID of the control to update.
  - `kwargs`: Key-value pairs of fields to update (e.g., name, description, status).
- **Returns**: JSON response of the updated control.

### `add_control_proof`

## Proof API

## Overview
This module provides a Python wrapper for interacting with the Proof API of Hyperproof. It allows developers to retrieve, manage, and upload proof data within their organization. The class uses an API client to handle communication with the Hyperproof platform.

### Constructor

```python
def __init__(self, api_client)
```

- **Description**: Initializes the `ProofAPI` class with the provided API client.
- **Parameters**:
  - `api_client`: An instance of the API client used to make requests.

## Methods

### `get_proof_metadata_collection`

```python
def get_proof_metadata_collection(limit=500, sort_by="uploadedOn", sort_direction="desc", object_type=None, object_id=None, raw=False)
```

- **Description**: Retrieves all proof metadata for the organization, control, label, or task with optional filters.
- **Parameters**:
  - `limit`: Maximum number of results to retrieve (default: 500).
  - `sort_by`: Field to sort results by (default: "uploadedOn").
  - `sort_direction`: Sort direction ("asc" or "desc", default: "desc").
  - `object_type`: Filter by object type (optional).
  - `object_id`: Filter by object ID (optional).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: List of proof metadata or raw response.

### `get_proof_metadata`

```python
def get_proof_metadata(proof_id, raw=False)
```

- **Description**: Retrieves specific proof metadata by proof ID.
- **Parameters**:
  - `proof_id`: The unique ID of the proof to retrieve.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Proof metadata or raw response.

### `add_proof`

```python
def add_proof(file_path, object_id=None, object_type=None, raw=False)
```

- **Description**: Uploads a new proof file to the organization.
- **Parameters**:
  - `file_path`: Path to the proof file to upload.
  - `object_id`: The object ID the proof is related to (optional).
  - `object_type`: The object type (optional).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data of the newly added proof.

### `add_proof_version`

```python
def add_proof_version(proof_id, file_path, raw=False)
```

- **Description**: Adds a new version of an existing proof by proof ID.
- **Parameters**:
  - `proof_id`: The ID of the proof to update.
  - `file_path`: Path to the new version of the proof file.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data of the updated proof version.

### `get_proof_contents`

```python
def get_proof_contents(proof_id, version=None, raw=False)
```

- **Description**: Retrieves the contents of a proof as a file.
- **Parameters**:
  - `proof_id`: The ID of the proof to retrieve.
  - `version`: The version of the proof to retrieve (optional).
  - `raw`: If `True`, return raw response text.
- **Returns**: The contents of the proof file or raw response.

### `get_proof_by_user`

```python
def get_proof_by_user(userid=None, givenName=None, surname=None, object_type=None, object_id=None, raw=False)
```

- **Description**: Retrieves proofs associated with a user based on their user ID, given name, surname, or object type.
- **Parameters**:
  - `userid`: The unique identifier of the user (optional).
  - `givenName`: The given name of the user (optional).
  - `surname`: The surname of the user (optional).
  - `object_type`: The object type (optional).
  - `object_id`: The object ID (optional).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: List of proofs associated with the specified user(s).

### `get_proof_by_label`

```python
def get_proof_by_label(label_name, limit=500, sort_by="uploadedOn", sort_direction="desc", raw=False)
```

- **Description**: Retrieves proofs associated with a specific label by label name (partial, case-insensitive match).
- **Parameters**:
  - `label_name`: The name of the label to search for.
  - `limit`: Maximum number of results to retrieve (default: 500).
  - `sort_by`: Field to sort results by (default: "uploadedOn").
  - `sort_direction`: Sort direction ("asc" or "desc", default: "desc").
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: List of proofs associated with the specified label.

## Dependencies
- `users_api.UsersAPI`: The `ProofAPI` interacts with the `UsersAPI` to fetch organizational users when needed.
- `labels_api.LabelsAPI`: The `ProofAPI` interacts with the `LabelsAPI` to fetch label data when needed.
- `api_client`: The class uses a shared API client to interact with Hyperproof's backend services.

```python
def add_control_proof(control_id, file_path, raw=False)
```

- **Description**: Adds a proof item (e.g., file) to a control.
- **Parameters**:
  - `control_id`: The unique ID of the control to which proof is added.
  - `file_path`: Path to the file that will be uploaded as proof.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON (default is `False`).
- **Returns**: Response data of the newly uploaded proof in JSON or raw format.

### `get_controls_by_user`

```python
def get_controls_by_user(userid=None, givenName=None, surname=None, raw=False)
```

- **Description**: Retrieves controls associated with a specific user based on their user ID, given name, or surname.
- **Parameters**:
  - `userid`: The unique identifier of the user (optional).
  - `givenName`: The given name of the user (optional).
  - `surname`: The surname of the user (optional).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON (default is `False`).
- **Returns**: List of controls associated with the specified user(s).

## Dependencies
- `users_api.UsersAPI`: The `ControlsAPI` interacts with the `UsersAPI` to fetch organizational users when needed (e.g., for filtering controls by user).
- `api_client`: The class uses a shared API client to interact with Hyperproof's backend services.


# Custom Apps API

## Overview
This module provides a Python wrapper for interacting with the Custom Apps API of Hyperproof. It allows developers to retrieve, add, update, delete custom apps, and retrieve events/statistics for custom apps. The class uses an API client to handle communication with the Hyperproof platform.

### Author: Virgil Vaduva
### License: GNU General Public License (GPL)
### Version: 1.0.0

## Class: `CustomAppsAPI`

### Constructor

```python
def __init__(self, api_client)
```

- **Description**: Initializes the `CustomAppsAPI` class with the provided API client.
- **Parameters**:
  - `api_client`: An instance of the API client used to make requests.

## Methods

### `get_custom_apps`

```python
def get_custom_apps(raw=False)
```

- **Description**: Retrieves the custom apps installed in an organization.
- **Parameters**:
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `add_custom_app`

```python
def add_custom_app(app_type, is_custom, org_id, package_name, package_version, deployment_status="pending", raw=False)
```

- **Description**: Adds a new custom app to the organization.
- **Parameters**:
  - `app_type`: Type of the app (e.g., 'hypersync').
  - `is_custom`: Boolean indicating if the app is custom.
  - `org_id`: ID of the organization where the app is installed.
  - `package_name`: Name of the app package.
  - `package_version`: Version of the app package.
  - `deployment_status`: Deployment status (default is `"pending"`).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `get_custom_app_by_id`

```python
def get_custom_app_by_id(app_id, raw=False)
```

- **Description**: Retrieves a specific custom app by its unique ID.
- **Parameters**:
  - `app_id`: The unique ID of the custom app to retrieve.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `update_custom_app`

```python
def update_custom_app(app_id, app_type=None, is_custom=None, package_name=None, package_version=None, deployment_status=None, raw=False)
```

- **Description**: Updates a custom app that is installed in an organization.
- **Parameters**:
  - `app_id`: The unique ID of the custom app to update.
  - `app_type`: Updated app type (optional).
  - `is_custom`: Updated boolean indicating if the app is custom (optional).
  - `package_name`: Updated package name (optional).
  - `package_version`: Updated package version (optional).
  - `deployment_status`: Updated deployment status (optional).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `delete_custom_app`

```python
def delete_custom_app(app_id, raw=False)
```

- **Description**: Deletes a custom app that is installed in an organization.
- **Parameters**:
  - `app_id`: The unique ID of the custom app to delete.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `get_custom_app_events`

```python
def get_custom_app_events(app_id, raw=False)
```

- **Description**: Retrieves log events generated by a custom app.
- **Parameters**:
  - `app_id`: The unique ID of the custom app.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `get_custom_app_stats`

```python
def get_custom_app_stats(app_id, raw=False)
```

- **Description**: Retrieves statistics for a custom app installed in the organization.
- **Parameters**:
  - `app_id`: The unique ID of the custom app.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

## Dependencies
- `api_client`: The class uses a shared API client to interact with Hyperproof's backend services.

## Labels API

## Overview
This module provides a Python wrapper for interacting with the Labels API of Hyperproof. It allows developers to retrieve, add, update labels, and manage label-related proofs within their organization. The class uses an API client to handle communication with the Hyperproof platform.

### Constructor

```python
def __init__(self, api_client)
```

- **Description**: Initializes the `LabelsAPI` class with the provided API client.
- **Parameters**:
  - `api_client`: An instance of the API client used to make requests.

## Methods

### `get_labels`

```python
def get_labels(can_link=None, status=None, raw=False)
```

- **Description**: Retrieves all labels in the organization with optional filters.
- **Parameters**:
  - `can_link`: Filter by link permission (optional).
  - `status`: Filter by label status (optional).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw format.

### `get_label_by_id`

```python
def get_label_by_id(label_id, raw=False)
```

- **Description**: Retrieves a specific label by its unique ID.
- **Parameters**:
  - `label_id`: The unique ID of the label to retrieve.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: JSON response or raw format of the label.

### `get_label_summaries`

```python
def get_label_summaries(can_link=None, status=None, raw=False)
```

- **Description**: Retrieves summaries of labels in the organization with optional filters.
- **Parameters**:
  - `can_link`: Filter by link permission (optional).
  - `status`: Filter label summaries by their status (optional).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: JSON response or raw text of label summaries.

### `add_label`

```python
def add_label(name, description, raw=False)
```

- **Description**: Adds a new label to the organization.
- **Parameters**:
  - `name`: The name of the label.
  - `description`: A brief description of the label.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: JSON response or raw text of the newly added label.

### `update_label`

```python
def update_label(label_id, **kwargs)
```

- **Description**: Updates an existing label with new values.
- **Parameters**:
  - `label_id`: The unique ID of the label to update.
  - `kwargs`: Key-value pairs of fields to update.
- **Returns**: JSON response of the updated label.

### `add_label_proof`

```python
def add_label_proof(label_id, file_path, raw=False)
```

- **Description**: Adds a proof item (file) to a label.
- **Parameters**:
  - `label_id`: The unique ID of the label.
  - `file_path`: Path to the file to upload as proof.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data of the newly uploaded proof in JSON or raw format.

### `get_labels_by_user`

```python
def get_labels_by_user(userid=None, givenName=None, surname=None, raw=False)
```

- **Description**: Retrieves labels associated with a user based on their user ID, given name, or surname.
- **Parameters**:
  - `userid`: The unique identifier of the user (optional).
  - `givenName`: The given name of the user (optional).
  - `surname`: The surname of the user (optional).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: List of labels associated with the specified user(s).

## Dependencies
- `users_api.UsersAPI`: The `LabelsAPI` interacts with the `UsersAPI` to fetch organizational users when needed.
- `api_client`: The class uses a shared API client to interact with Hyperproof's backend services.

## Programs API

## Overview
This module provides a Python wrapper for interacting with the Programs API of Hyperproof. It allows developers to retrieve, add, and update programs within their organization. The class uses an API client to handle communication with the Hyperproof platform.

### Constructor: ProgramsAPI

```python
def __init__(self, api_client)
```

- **Description**: Initializes the `ProgramsAPI` class with the provided API client.
- **Parameters**:
  - `api_client`: An instance of the API client used to make requests.

## Methods

### `get_programs`

```python
def get_programs(status=None, raw=False)
```

- **Description**: Retrieves all programs for the organization with an optional status filter.
- **Parameters**:
  - `status`: Filter by program status (optional, e.g., 'operating', 'defining').
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `add_program`

```python
def add_program(name, description, section_root_id, primary_contact_id, work_status="defining", 
                source_template_id=None, selected_baselines=None, jumpstart_program_ids=None, 
                clone_program_name=None, framework_license_notice=None, raw=False)
```

- **Description**: Adds a new program to the organization.
- **Parameters**:
  - `name`: The name of the program.
  - `description`: A brief description of the program.
  - `section_root_id`: The section root ID associated with the program.
  - `primary_contact_id`: The ID of the primary contact for the program.
  - `work_status`: The current work status (default is `'defining'`).
  - `source_template_id`: The template ID used for creating the program (optional).
  - `selected_baselines`: Baselines selected for the program (optional).
  - `jumpstart_program_ids`: Jumpstart program IDs (optional).
  - `clone_program_name`: Name of the program to be cloned (optional).
  - `framework_license_notice`: Framework license notice (optional).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `get_program_by_id`

```python
def get_program_by_id(program_id, raw=False)
```

- **Description**: Retrieves a specific program by its unique ID.
- **Parameters**:
  - `program_id`: The unique ID of the program.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `update_program`

```python
def update_program(program_id, name=None, description=None, work_status=None, 
                   override_health=None, override_health_health=None, override_health_by=None, 
                   override_health_reason=None, selected_baselines=None, baseline_enabled=None, 
                   framework_version_mapping_id=None, removed_requirement_ids=None, 
                   updated_requirement_ids=None, clone_program_name=None, 
                   is_update_complete=None, raw=False)
```

- **Description**: Updates an existing program by its unique ID.
- **Parameters**:
  - `program_id`: The unique ID of the program to update.
  - `name`: The new name of the program (optional).
  - `description`: The new description of the program (optional).
  - `work_status`: Updated work status (optional, e.g., 'defining', 'operating').
  - `override_health`: Whether to override health (optional).
  - `override_health_health`: Health status to override (optional).
  - `override_health_by`: ID of the person overriding health (optional).
  - `override_health_reason`: Reason for health override (optional).
  - `selected_baselines`: Updated baselines (optional).
  - `baseline_enabled`: Whether baseline is enabled (optional).
  - `framework_version_mapping_id`: Framework version mapping ID (optional).
  - `removed_requirement_ids`: List of removed requirement IDs (optional).
  - `updated_requirement_ids`: List of updated requirement IDs (optional).
  - `clone_program_name`: Name of the program to be cloned (optional).
  - `is_update_complete`: Whether the update is complete (optional).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

## Dependencies
- `api_client`: The class uses a shared API client to interact with Hyperproof's backend services.


## Risks API

## Overview
This module provides a Python wrapper for interacting with the Risks API of Hyperproof. It allows developers to retrieve, add, filter, and update risks within their organization. The class uses an API client to handle communication with the Hyperproof platform.

### Constructor

```python
def __init__(self, api_client)
```

- **Description**: Initializes the `RisksAPI` class with the provided API client.
- **Parameters**:
  - `api_client`: An instance of the API client used to make requests.

## Methods

### `get_risks`

```python
def get_risks(risk_register_id=None, status=None, raw=False)
```

- **Description**: Retrieves all risks for the organization with optional filters by risk register or status.
- **Parameters**:
  - `risk_register_id`: The unique ID of the risk register (optional).
  - `status`: Filter by the status of the risks (optional, e.g., 'active', 'archived').
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `add_risk`

```python
def add_risk(risk_register_id, risk_identifier, name, description, category, response, 
             likelihood_level, likelihood_rationale, impact_level, impact_rationale, 
             tolerance_level, owner_id, custom_fields=None, raw=False)
```

- **Description**: Adds a new risk to the organization, with optional custom fields.
- **Parameters**:
  - `risk_register_id`: The unique ID of the risk register.
  - `risk_identifier`: The identifier for the risk.
  - `name`: Name of the risk.
  - `description`: Description of the risk.
  - `category`: Category of the risk.
  - `response`: Risk response strategy (e.g., 'mitigate', 'accept').
  - `likelihood_level`: Likelihood level (e.g., 1-5).
  - `likelihood_rationale`: Explanation for the likelihood level.
  - `impact_level`: Impact level (e.g., 1-5).
  - `impact_rationale`: Explanation for the impact level.
  - `tolerance_level`: Tolerance level for the risk.
  - `owner_id`: The owner ID for the risk.
  - `custom_fields`: Optional custom fields associated with the risk.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `get_risk_by_id`

```python
def get_risk_by_id(risk_id, raw=False)
```

- **Description**: Retrieves a specific risk by its unique ID.
- **Parameters**:
  - `risk_id`: The unique ID of the risk.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `update_risk`

```python
def update_risk(risk_id, name=None, description=None, category=None, response=None, 
                likelihood_level=None, likelihood_rationale=None, impact_level=None, 
                impact_rationale=None, tolerance_level=None, status=None, owner_id=None, 
                custom_fields=None, clear_category=False, clear_likelihood_level=False, 
                clear_impact_level=False, clear_tolerance_level=False, raw=False)
```

- **Description**: Updates an existing risk with new values, with support for clearing certain fields.
- **Parameters**:
  - `risk_id`: The unique ID of the risk.
  - `name`: Updated name of the risk (optional).
  - `description`: Updated description of the risk (optional).
  - `category`: Updated category of the risk (optional).
  - `response`: Updated risk response strategy (optional).
  - `likelihood_level`: Updated likelihood level (optional).
  - `likelihood_rationale`: Updated explanation for likelihood level (optional).
  - `impact_level`: Updated impact level (optional).
  - `impact_rationale`: Updated explanation for impact level (optional).
  - `tolerance_level`: Updated tolerance level (optional).
  - `status`: Updated status of the risk (optional, e.g., 'active', 'archived').
  - `owner_id`: Updated owner ID for the risk (optional).
  - `custom_fields`: Optional custom fields associated with the risk.
  - `clear_category`: If `True`, clears the category field.
  - `clear_likelihood_level`: If `True`, clears the likelihood level field.
  - `clear_impact_level`: If `True`, clears the impact level field.
  - `clear_tolerance_level`: If `True`, clears the tolerance level field.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `filter_risks`

```python
def filter_risks(risk_ids=None, modified_after=None, status=None, raw=False)
```

- **Description**: Filters risks based on a set of criteria like risk IDs, modification date, and status.
- **Parameters**:
  - `risk_ids`: List of risk IDs to filter by (optional).
  - `modified_after`: Only return risks modified after this date (optional).
  - `status`: Filter by risk status (optional).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `get_risks_by_user`

```python
def get_risks_by_user(userid=None, givenName=None, surname=None, raw=False)
```

- **Description**: Retrieves risks associated with a user based on their user ID, given name, or surname.
- **Parameters**:
  - `userid`: The unique identifier of the user (optional).
  - `givenName`: The given name of the user (optional).
  - `surname`: The surname of the user (optional).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: List of risks associated with the specified user(s).

## Dependencies
- `users_api.UsersAPI`: The `RisksAPI` interacts with the `UsersAPI` to fetch organizational users when needed.
- `api_client`: The class uses a shared API client to interact with Hyperproof's backend services.


## Tasks API

## Overview
This module provides a Python wrapper for interacting with the Tasks API of Hyperproof. It allows developers to create, retrieve, update tasks, and handle task-related proofs within their organization. The class uses an API client to handle communication with the Hyperproof platform.

### Constructor

```python
def __init__(self, api_client)
```

- **Description**: Initializes the `TasksAPI` class with the provided API client.
- **Parameters**:
  - `api_client`: An instance of the API client used to make requests.

## Methods

### `add_task`

```python
def add_task(title, target_object, description, assignee_id, priority, due_date, 
             has_integration=False, raw=False)
```

- **Description**: Adds a new task to the organization.
- **Parameters**:
  - `title`: Title of the task.
  - `target_object`: Target object (includes `objectId` and `objectType`).
  - `description`: Description of the task.
  - `assignee_id`: ID of the assignee.
  - `priority`: Priority of the task (`'highest'`, `'high'`, `'medium'`, `'low'`, `'lowest'`).
  - `due_date`: Due date of the task (ISO 8601 format).
  - `has_integration`: Boolean indicating if the task has an integration (default is `False`).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `get_task_by_id`

```python
def get_task_by_id(task_id, raw=False)
```

- **Description**: Retrieves a task in an organization by ID.
- **Parameters**:
  - `task_id`: The unique ID of the task.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `update_task`

```python
def update_task(task_id, title=None, description=None, assignee_id=None, target_id=None, 
                target_type=None, task_status_id=None, priority=None, sort_order=None, 
                due_date=None, raw=False)
```

- **Description**: Updates an existing task with new values.
- **Parameters**:
  - `task_id`: The unique ID of the task.
  - `title`: New title for the task (optional).
  - `description`: New description of the task (optional).
  - `assignee_id`: New assignee ID (optional).
  - `target_id`: New target object ID (optional).
  - `target_type`: New target object type (optional).
  - `task_status_id`: New task status ID (optional).
  - `priority`: New priority of the task (optional).
  - `sort_order`: New sort order (optional).
  - `due_date`: New due date (optional).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `add_task_proof`

```python
def add_task_proof(task_id, file_path, proof_owned_by=None, proof_source=None, 
                   proof_source_id=None, proof_source_file_id=None, proof_source_modified_on=None, 
                   proof_live_sync_enabled=False, raw=False)
```

- **Description**: Adds a proof item to a task.
- **Parameters**:
  - `task_id`: The unique ID of the task.
  - `file_path`: Path to the proof file to upload.
  - `proof_owned_by`: ID of the proof owner (optional).
  - `proof_source`: Source of the proof (optional).
  - `proof_source_id`: ID of the proof source (optional).
  - `proof_source_file_id`: Source file ID of the proof (optional).
  - `proof_source_modified_on`: Date and time the proof was modified (optional).
  - `proof_live_sync_enabled`: Whether live sync is enabled for the proof (optional, default is `False`).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `get_task_proof_metadata`

```python
def get_task_proof_metadata(task_id, raw=False)
```

- **Description**: Retrieves the proof metadata associated with a task.
- **Parameters**:
  - `task_id`: The unique ID of the task.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `filter_tasks`

```python
def filter_tasks(target_object_type=None, target_object_ids=None, task_ids=None, 
                 assignee_ids=None, assignee_id=None, modified_after=None, raw=False)
```

- **Description**: Filters tasks based on a set of criteria.
- **Parameters**:
  - `target_object_type`: Type of the target object (optional).
  - `target_object_ids`: List of target object IDs to filter by (optional).
  - `task_ids`: List of task IDs to filter by (optional).
  - `assignee_ids`: List of assignee IDs to filter by (optional).
  - `assignee_id`: Single assignee ID to filter by (optional).
  - `modified_after`: Return tasks modified after this date (optional).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `get_task_comments`

```python
def get_task_comments(task_id, raw=False)
```

- **Description**: Retrieves the comments in a task's activity feed.
- **Parameters**:
  - `task_id`: The unique ID of the task.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `add_task_comment`

```python
def add_task_comment(task_id, comment_text_formatted, is_internal_comment=False, 
                     object_type="task", object_id=None, raw=False)
```

- **Description**: Adds a comment to a task's activity feed.
- **Parameters**:
  - `task_id`: The unique ID of the task.
  - `comment_text_formatted`: Formatted comment text.
  - `is_internal_comment`: Whether it's an internal comment (default is `False`).
  - `object_type`: Type of the object associated with the comment (default is `'task'`).
  - `object_id`: The object ID associated with the comment (optional).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `update_task_comment`

```python
def update_task_comment(task_id, comment_id, comment_text_formatted=None, 
                        is_internal_comment=None, object_type="task", object_id=None, raw=False)
```

- **Description**: Updates an existing comment in a task's activity feed.
- **Parameters**:
  - `task_id`: The unique ID of the task.
  - `comment_id`: The unique ID of the comment.
  - `comment_text_formatted`: Updated formatted comment text (optional).
  - `is_internal_comment`: Updated internal comment flag (optional).
  - `object_type`: Type of the object associated with the comment (default is `'task'`).
  - `object_id`: The object ID associated with the comment (optional).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `delete_task_comment`

```python
def delete_task_comment(task_id, comment_id, raw=False)
```

- **Description**: Deletes an existing comment in a task's activity feed.
- **Parameters**:
  - `task_id`: The unique ID of the task.
  - `comment_id`: The unique ID of the comment.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

## Dependencies
- `users_api.UsersAPI`: The `TasksAPI` interacts with the `UsersAPI` to fetch organizational users when needed.
- `task_statuses_api.TaskStatusesAPI`: The `TasksAPI` interacts with the `TaskStatusesAPI` to fetch task statuses.
- `api_client`: The class uses a shared API client to interact with Hyperproof's backend services.

## Roles API

## Overview
This module provides a Python wrapper for interacting with the Roles API of Hyperproof. It allows developers to retrieve a list of roles within their organization. The class uses an API client to handle communication with the Hyperproof platform.

### Constructor

```python
def __init__(self, api_client)
```

- **Description**: Initializes the `RolesAPI` class with the provided API client.
- **Parameters**:
  - `api_client`: An instance of the API client used to make requests.

## Methods

### `get_roles`

```python
def get_roles(raw=False)
```

- **Description**: Retrieves a list of roles in the organization.
- **Parameters**:
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

## Dependencies
- `api_client`: The class uses a shared API client to interact with Hyperproof's backend services.

## Users API

## Overview
This module provides a Python wrapper for interacting with the Users API of Hyperproof. It allows developers to retrieve information about the currently authenticated user and organization users. The class uses an API client to handle communication with the Hyperproof platform.

### Constructor

```python
def __init__(self, api_client)
```

- **Description**: Initializes the `UsersAPI` class with the provided API client.
- **Parameters**:
  - `api_client`: An instance of the API client used to make requests.

## Methods

### `get_current_user`

```python
def get_current_user(expand=None, raw=False)
```

- **Description**: Retrieves the stored user information for the currently authenticated user.
- **Parameters**:
  - `expand`: Comma-separated list of fields to expand (optional). Supported values: `'identityProviders'`, `'organizations'`.
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

### `get_organization_users`

```python
def get_organization_users(expand=None, include_deactivated=False, raw=False)
```

- **Description**: Retrieves the users in an organization.
- **Parameters**:
  - `expand`: Comma-separated list of fields to expand (optional). Supported values: `'identityProviders'`, `'organizationRoleId'`.
  - `include_deactivated`: Whether or not to include deactivated users in the response (default is `False`).
  - `raw`: If `True`, return raw response text; otherwise return parsed JSON.
- **Returns**: Response data in JSON or raw text.

## Dependencies
- `api_client`: The class uses a shared API client to interact with Hyperproof's backend services.

# License

License - GNU General Public License (GPL)
This project is licensed under the GNU General Public License (GPL). The GPL ensures that the software remains free and open-source, allowing users to modify, distribute, and use it freely. However, any modifications or derivative works must also be licensed under the GPL and include the source code, ensuring that improvements to the software are shared with the community. This fosters collaboration and encourages transparency and innovation.
