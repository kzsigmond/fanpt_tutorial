import os 
import numpy as np 

# script to generate fanpt calculation directory structrure
# it copies the input templates and replaces ORDER and STEPS tags

# define parameters
orders = [1, 2, 3, 4]
steps = [10, 100, 1000]
wfn_dir = 'CISD/efree_fanpt'
input_template_path = 'input_templates/input_template_cisd.txt'
submit_path = 'input_templates/job_cisd.txt'

submit_calcs = False

### generate directories and inputs

current_directory = os.getcwd()

with open(input_template_path, 'r') as input_template:
    input_contents = input_template.read()


with open(submit_path, 'r') as submit:
    submit_contents = submit.read()

for ord in orders:
    ord_dir = os.path.join(current_directory, wfn_dir, f"order_{ord}")
    os.makedirs(ord_dir, exist_ok=False)
    for step in steps:
        step_dir = os.path.join(ord_dir, f'steps_{step}')
        os.makedirs(step_dir, exist_ok=True)

        # generate submission template
        submit_replaced = submit_contents.replace("ORDER", str(ord))
        submit_replaced = submit_replaced.replace("STEPS", str(step))
        submit_file_path = os.path.join(step_dir, "job.txt")
        with open(submit_file_path, 'w') as file:
            file.write(submit_replaced)

        # generate input template
        input_replaced = input_contents.replace("ORDER", str(ord))
        input_replaced = input_replaced.replace("STEPS", str(step))
        input_file_path = os.path.join(step_dir, "input_template.txt")
        with open(input_file_path, 'w') as file:
            file.write(input_replaced)
        
        # copy submit jobs file 
        command = f"cp input_templates/submit_jobs.py {step_dir}"
        os.system(command)
        if submit_calcs:
            # submit job
            os.chdir(step_dir)
            print("submitting jobs in directory:", step_dir)
            os.system("python submit_jobs.py")
            os.chdir(current_directory)