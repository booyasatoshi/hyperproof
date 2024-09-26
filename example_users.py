# Example using the get_organization_users method to retrieve all users in 
# the Hyperproof organization, including deactivated users with the output raw

import hyperproof

users = hyperproof.get_organization_users(include_deactivated=False, raw=True)
print(users)