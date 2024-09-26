# Example using the add_task_comment method to add a comment to an existing task

import hyperproof

task_id = "12345"
comment_text = "This is a formatted comment for the task."
is_internal = True  # If you want to mark it as an internal comment
object_type = "task"  # The type of object the comment relates to, default is "task"
object_id = 67890  # Optional, related object ID
raw_format = False  # Whether to return raw data or not

# Add a comment to a task
response = hyperproof.add_task_comment(task_id, comment_text, is_internal_comment=is_internal, object_type=object_type, object_id=object_id, raw=raw_format)

# Print response
print(response)


# Example using the add_task_proof method to add proof to a task

# Define the details for the proof item
task_id = 12345  # The unique ID of the task
file_path = "/path/to/proof/file.pdf"  # Path to the proof file you want to upload
proof_owned_by = 67890  # ID of the proof owner (optional)
proof_source = "System A"  # Source of the proof (optional)
proof_source_id = "ABC123"  # ID of the proof source (optional)
proof_source_file_id = "File123"  # Source file ID of the proof (optional)
proof_source_modified_on = "2024-09-01T12:00:00Z"  # Date and time the proof was last modified (ISO 8601 format, optional)
proof_live_sync_enabled = True  # Whether live sync is enabled for the proof (optional, default is False)
raw_format = False  # Set to True if you want raw response instead of parsed JSON

# Add the proof to the task
response = hyperproof.add_task_proof(
    task_id=task_id,
    file_path=file_path,
    proof_owned_by=proof_owned_by,
    proof_source=proof_source,
    proof_source_id=proof_source_id,
    proof_source_file_id=proof_source_file_id,
    proof_source_modified_on=proof_source_modified_on,
    proof_live_sync_enabled=proof_live_sync_enabled,
    raw=raw_format
)

# Print the response
print(response)
