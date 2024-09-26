# Example using the get_task_statuses method to retrieve all the statuses defined
# in the Hyperproof organization

import hyperproof

task_statuses = hyperproof.get_task_statuses()
print(task_statuses)