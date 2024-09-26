# Example using the get_custom_app_events method to retrieve events from a 
# custom app being used by the hyperproof instance

import hyperproof

# Define the unique ID of the custom app
app_id = 12345  # Replace with the actual app ID

# Set to True if you want raw response, otherwise False for parsed JSON
raw_format = False  

# Retrieve the log events for the custom app
response = hyperproof.get_custom_app_events(app_id=app_id, raw=raw_format)

# Print the retrieved events
print(response)
