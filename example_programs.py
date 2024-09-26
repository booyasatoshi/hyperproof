# Example using the add_program method to add a program to the
# organization

import hyperproof

# Define the details for the new program
name = "New Compliance Program"  # Name of the program
description = "A program to ensure compliance with industry standards."  # Brief description
section_root_id = "1234"  # Section root ID associated with the program
primary_contact_id = "5678"  # ID of the primary contact for the program
work_status = "defining"  # Work status of the program (default is 'defining')
source_template_id = None  # Optional: Template ID for creating the program
selected_baselines = "[101, 102]"  # Optional: Baselines selected for the program
jumpstart_program_ids = "[201, 202]"  # Optional: Jumpstart program IDs
clone_program_name = None  # Optional: Name of the program to be cloned
framework_license_notice = "MIT License"  # Optional: Framework license notice
raw_format = False  # Set to True if you want raw response instead of parsed JSON

# Add the new program
response = hyperproof.add_program(
    name=name,
    description=description,
    section_root_id=section_root_id,
    primary_contact_id=primary_contact_id,
    work_status=work_status,
    source_template_id=source_template_id,
    selected_baselines=selected_baselines,
    jumpstart_program_ids=jumpstart_program_ids,
    clone_program_name=clone_program_name,
    framework_license_notice=framework_license_notice,
    raw=raw_format
)

# Print the response
print(response)
