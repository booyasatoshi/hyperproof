# Example using the get_proof_by_user method to retrieve all proofs in 
# the Hyperproof organization created by username with the last name Smith

import hyperproof

proof = hyperproof.get_proof_by_user(surname="Smith")
print(proof)




# Example using the get_proof_metadata_collection method to retrieve all the 
# metadata for all the proof.  Use the next_token parameter returned by the 
# server to manage pagination if you have more than 500 proofs.

# Define parameters for retrieving proof metadata
limit = "500"  # Maximum number of results per call (default is 500)
sort_by = "uploadedOn"  # Field to sort by (default is 'uploadedOn')
sort_direction = "desc"  # Sort direction ('asc' or 'desc', default is 'desc')
object_type = "control"  # Optional: Filter by object type (e.g., 'control' or 'label')
object_id = "12345"  # Optional: Filter by object ID
raw_format = False  # Set to True if you want raw response instead of parsed JSON

# Initialize an empty list to store all proof metadata
all_proof_metadata = []
next_token = None

# Loop to handle pagination and retrieve all proof metadata
while True:
    # Fetch proof metadata with pagination support
    response = hyperproof.get_proof_metadata_collection(
        limit=limit,
        sort_by=sort_by,
        sort_direction=sort_direction,
        object_type=object_type,
        object_id=object_id,
        raw=raw_format
    )

    # Check if the response contains data and append it to the list
    if not response or 'data' not in response:
        raise ValueError("No data returned from get_proof_metadata_collection.")

    all_proof_metadata.extend(response['data'])

    # Retrieve the next token for pagination, if available
    next_token = response.get('continuationToken')

    # If no next token is present, we've retrieved all the data
    if not next_token:
        break

# Process or display the accumulated proof metadata
for proof in all_proof_metadata:
    print(proof)
