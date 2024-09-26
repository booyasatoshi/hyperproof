# utils.py
#
# This module provides utility functionality for interacting with the Hyperproof API, 
# including handling API authentication and sending HTTP requests to the Hyperproof API.
# Author: Virgil Vaduva
# Timestamp: 2024-09-25
# License: This project is licensed under the GNU General Public License (GPL).
#
# Description:
# The APIClient class handles authentication via OAuth, and it provides methods 
# for making GET, POST, PUT, and PATCH requests. The class ensures token-based 
# authorization is applied to every request. Error handling and logging are used to 
# capture and report request issues.

import requests
import logging
from requests.exceptions import HTTPError, RequestException, Timeout, ConnectionError
import json

# Set up logging
# A logger named 'Hyperproof API' is created to capture logs for this module.
logger = logging.getLogger('Hyperproof API')
logger.setLevel(logging.INFO)  # Default logging level set to INFO

# Create a console handler for the logger and set its logging level to DEBUG.
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Formatter is created to display logs in a specific format: time, logger name, 
# logging level, and the actual log message.
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Attach the formatter to the console handler.
ch.setFormatter(formatter)

# Attach the console handler to the logger.
logger.addHandler(ch)

# OAuth token endpoint for Hyperproof's authentication.
TOKEN_ENDPOINT = "https://accounts.hyperproof.app/oauth/token"

class APIClient:
    """
    The APIClient class handles authentication via OAuth2 and makes HTTP requests to the Hyperproof API.
    This class manages the access token required for authorization and includes methods to interact
    with the API (GET, POST, PUT, PATCH).
    """
    
    def __init__(self, client_id, client_secret):
        """
        Initializes the APIClient with the given client credentials and authenticates immediately.
        - client_id: The OAuth client ID for authenticating with Hyperproof.
        - client_secret: The OAuth client secret for authenticating with Hyperproof.
        
        The access_token is initially set to None. Upon initialization, the client attempts to 
        authenticate by calling the `_authenticate()` method.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None  # Access token will be set upon successful authentication.
        
        logger.debug(f"Initializing APIClient with client_id: {client_id}")
        
        try:
            self._authenticate()  # Attempt to authenticate upon initialization.
        except Exception as e:
            logger.error(f"Failed to authenticate: {e}")
            self.access_token = None  # Ensure token remains None if authentication fails.

    def _authenticate(self):
        """
        Handles OAuth authentication with Hyperproof to retrieve an access token.
        Sends a POST request to the TOKEN_ENDPOINT with the client credentials.
        If successful, the access token is stored for future requests.
        """
        logger.debug("Authenticating to get access token")
        
        # Parameters required for the OAuth2 client credentials grant type.
        params = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        logger.debug(f"Authentication params: {json.dumps(params, indent=2)}")
        
        try:
            # Sending POST request to OAuth token endpoint to obtain the access token.
            response = requests.post(TOKEN_ENDPOINT, data=params)
            
            # Log the status code and response details for debugging purposes.
            logger.debug(f"Token request status code: {response.status_code}")
            logger.debug(f"Token response headers: {json.dumps(dict(response.headers), indent=2)}")
            logger.debug(f"Token response body: {response.text}")

            if response.status_code == 200:
                # Parse and store the access token if authentication is successful.
                response_json = self._parse_json(response)
                self.access_token = response_json.get('access_token')
                logger.debug("Access token retrieved successfully")
            else:
                # Log an error if the token request fails (e.g., invalid credentials).
                logger.error(f"Failed to retrieve access token: {response.status_code} {response.text}")
                self.access_token = None
        except (HTTPError, ConnectionError, Timeout, RequestException) as err:
            # Catch common HTTP request errors and log them.
            logger.error(f"Error during authentication: {err}")
            self.access_token = None

    def _get_headers(self):
        """
        Constructs the headers required for API requests.
        If the access token is missing or expired, the client will attempt to re-authenticate.
        Returns the headers including the Authorization Bearer token.
        """
        if not self.access_token:
            logger.debug("Access token not found. Re-authenticating...")
            self._authenticate()  # Re-authenticate if no valid access token is available.
        
        # Headers for the API request, including the Authorization token and content type.
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        logger.debug(f"Request headers: {json.dumps(headers, indent=2)}")
        return headers

    def get(self, base_url, endpoint, params=None, raw=False):
        """
        Sends a GET request to the specified API endpoint.
        - base_url: The base URL for the API.
        - endpoint: The specific API endpoint to interact with.
        - params: Optional query parameters to include in the request.
        - raw: If True, returns the raw response body; otherwise, returns parsed JSON.
        """
        url = f"{base_url}{endpoint}"
        logger.debug(f"Sending GET request to: {url}")
        logger.debug(f"GET request params: {json.dumps(params, indent=2)}")
        
        try:
            # Sending the GET request with appropriate headers and parameters.
            response = requests.get(url, headers=self._get_headers(), params=params)
            
            # Log the response status and body for debugging purposes.
            logger.debug(f"GET response status code: {response.status_code}")
            logger.debug(f"GET response headers: {json.dumps(dict(response.headers), indent=2)}")
            logger.debug(f"GET response body: {response.text}")
            
            return self._handle_response(response, raw=raw)
        except Exception as e:
            # Log any exceptions that occur during the GET request.
            logger.error(f"GET request failed: {e}")
            return None

    def post(self, base_url, endpoint, data=None, files=None, raw=False):
        """
        Sends a POST request to the specified API endpoint.
        - base_url: The base URL for the API.
        - endpoint: The specific API endpoint to interact with.
        - data: Optional JSON payload to include in the request body.
        - files: Optional file payload for multipart requests.
        - raw: If True, returns the raw response body; otherwise, returns parsed JSON.
        """
        url = f"{base_url}{endpoint}"
        logger.debug(f"Sending POST request to: {url}")
        logger.debug(f"POST request data: {json.dumps(data, indent=2)}")
        logger.debug(f"POST request files: {files}")
        
        try:
            # Sending the POST request, handling both JSON and file uploads.
            if files:
                response = requests.post(url, headers=self._get_headers(), files=files)
            else:
                response = requests.post(url, headers=self._get_headers(), json=data)
            
            logger.debug(f"POST response status code: {response.status_code}")
            logger.debug(f"POST response headers: {json.dumps(dict(response.headers), indent=2)}")
            logger.debug(f"POST response body: {response.text}")
            
            return self._handle_response(response, raw=raw)
        except Exception as e:
            logger.error(f"POST request failed: {e}")
            return None

    def put(self, base_url, endpoint, data=None, raw=False):
        """
        Sends a PUT request to the specified API endpoint.
        - base_url: The base URL for the API.
        - endpoint: The specific API endpoint to interact with.
        - data: Optional JSON payload to include in the request body.
        - raw: If True, returns the raw response body; otherwise, returns parsed JSON.
        """
        url = f"{base_url}{endpoint}"
        logger.debug(f"Sending PUT request to: {url}")
        logger.debug(f"PUT request data: {json.dumps(data, indent=2)}")
        
        try:
            # Sending the PUT request with the provided data.
            response = requests.put(url, headers=self._get_headers(), json=data)
            
            logger.debug(f"PUT response status code: {response.status_code}")
            logger.debug(f"PUT response headers: {json.dumps(dict(response.headers), indent=2)}")
            logger.debug(f"PUT response body: {response.text}")
            
            return self._handle_response(response, raw=raw)
        except Exception as e:
            logger.error(f"PUT request failed: {e}")
            return None

    def patch(self, base_url, endpoint, data=None, raw=False):
        """
        Sends a PATCH request to the specified API endpoint.
        - base_url: The base URL for the API.
        - endpoint: The specific API endpoint to interact with.
        - data: Optional JSON payload to include in the request body.
        - raw: If True, returns the raw response body; otherwise, returns parsed JSON.
        """
        url = f"{base_url}{endpoint}"
        logger.debug(f"Sending PATCH request to: {url}")
        logger.debug(f"PATCH request data: {json.dumps(data, indent=2)}")
        
        try:
            # Sending the PATCH request with the provided data.
            response = requests.patch(url, headers=self._get_headers(), json=data)
            
            logger.debug(f"PATCH response status code: {response.status_code}")
            logger.debug(f"PATCH response headers: {json.dumps(dict(response.headers), indent=2)}")
            logger.debug(f"PATCH response body: {response.text}")
            
            return self._handle_response(response, raw=raw)
        except Exception as e:
            logger.error(f"PATCH request failed: {e}")
            return None

    def _handle_response(self, response, raw=False):
        """
        Handles the response from an API request, raising exceptions for HTTP errors
        and parsing the response body as JSON (unless raw=True is specified).
        - response: The HTTP response object.
        - raw: If True, returns the raw response body; otherwise, parses as JSON.
        """
        try:
            # Raise an exception if the response contains an HTTP error status code.
            response.raise_for_status()
            
            if raw:
                return response.text  # Return raw text if specified.
            
            return self._parse_json(response)  # Parse JSON by default.
        except HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err} - {response.text}")
            return None
        except ValueError as val_err:
            logger.error(f"JSON decoding error: {val_err}")
            return None
        except Exception as err:
            logger.error(f"An error occurred when handling the response: {err}")
            return None

    def _parse_json(self, response):
        """
        Safely parses the JSON content of a response, handling content-type validation
        and logging errors for unexpected or invalid content.
        - response: The HTTP response object to parse.
        Returns the parsed JSON object or an empty dictionary if parsing fails.
        """
        try:
            # Ensure the response content-type is JSON before attempting to parse.
            if 'application/json' in response.headers.get('Content-Type', ''):
                return response.json()  # Parse the response body as JSON.
            else:
                logger.error(f"Unexpected content type: {response.headers.get('Content-Type')}")
                return {}
        except ValueError as val_err:
            # Log the JSON parsing error and return an empty dictionary.
            logger.error(f"Error parsing JSON: {val_err}")
            return {}
