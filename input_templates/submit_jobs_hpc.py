#!/usr/bin/env python
import os
import numpy as np

# Create H8 cube geometries
print("# Create BeH2 geometries...")

alphas = np.asarray([0., 1, 2, 2.5, 2.75, 3.0, 3.5, 4, 6, 20]) 
a = np.asarray([2.54, 2.08, 1.62, 1.39, 1.275, 1.16, 0.93, 0.7, 0.7, 0.7])

geoms = []
for i, alpha in enumerate(alphas):
    geom = [["Be", ["0.0", "0.0", "0.0"]], 
            ["H", ["0.0", str(-a[i]), str(alpha)]],
            ["H", ["0.0", str(a[i]), str(alpha)]]]
    geoms.append(geom)


current_directory = os.getcwd()
input_template_path = 'input_template.txt'
with open(input_template_path, 'r') as input_template:
    input_contents = input_template.read()

submit_path = 'job.txt'
with open(submit_path, 'r') as submit:
    submit_contents = submit.read()

for alpha, geom in zip(alphas, geoms):
    input_replaced = input_contents.replace("IMPORT_GEOM", str(geom))
    input_replaced = input_replaced.replace("ALPHA", str(alpha))
    submit_replaced = submit_contents.replace("ALPHA", str(alpha))

    folder_path = 'alpha-{:}'.format(alpha)
    os.makedirs(folder_path, exist_ok=True)

    for i in range(1):
        folder_path = os.path.join('alpha-{:}'.format(alpha), 'calc-{:02}'.format(i+1))
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join('alpha-{:}'.format(alpha), 'calc-{:02}'.format(i+1), 'input.py')

        # Write the text to a file
        with open(file_path, 'w') as file:
            file.write(input_replaced)

        submit_replaced = submit_replaced.replace("CALCS", '{:02}'.format(i+1))
        file_path = os.path.join('alpha-{:}'.format(alpha), 'calc-{:02}'.format(i+1), 'job.sh')
        with open(file_path, 'w') as file:
            file.write(submit_replaced)

        os.chdir(folder_path)
        os.system('sbatch job.sh')
        os.chdir(current_directory)
        print(f"Job submitted by {file_path}")