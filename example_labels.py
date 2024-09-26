# Example using the add_label_proof method to add proof to a label

from hyperproof import add_label_proof

# Define the proof ID and the label to be added
proof_id = "98765"
label_id = "e6c5cb85-2ba3-11ee-87b3"

# Add a label to the proof
response = add_label_proof(proof_id, label_id)

# Print the response to confirm the label was added
print(response)
