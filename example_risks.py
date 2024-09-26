# Example using the filter_risks method to retrieve a filtered list of specific risks, 
# matching a filter criteria. This will return risks modified after an ISO formatted
# date with an active status 

import hyperproof

# Define filtering criteria
risk_ids = [101, 102, 103]  # List of risk IDs to filter by
modified_after = "2023-01-01T00:00:00Z"  # ISO formatted date to filter risks modified after this date
status = "active"  # Filter by status, e.g., "active" or "closed"
raw_format = False  # Set to True if you want raw response instead of parsed JSON

# Call the method to filter risks based on the given criteria
response = hyperproof.filter_risks(risk_ids=risk_ids, modified_after=modified_after, status=status, raw=raw_format)

# Print the response
print(response)
