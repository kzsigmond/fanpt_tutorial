# Running FANPT calculations with Fanpy

## Quick start

### Step 1: Run `generate_dirs_and_inputs.py` for the BeH2 calculations.

```bash
python generate_dirs_and_inputs.py
```

### Step 2: Generating the geometry folders

Go to a folder for a given order and steps combination. E.g. 

```bash
cd CISD/efree_fanpt/order_2/steps_10
```

and execute `submit_jobs.py`

```bash
python submit_jobs.py
```

This will create the folders and input files for the specific geometries for BeH2. Note: The print statement (`Job submitted...`) is still there, but no calculation is submitted. The default `submit_jobs.py` template only generates the geometry directories. 

### Step 3: Run a calculation

Each geometry can have multiple folders if one wants multiple repetitions of a calculation. 

Go to one of the calculation folder. E.g.

```bash
cd alpha-0.0/calc-01
```
and run 

```bash
python input.py
```

This will generate an input similar to:

```
(Mid Optimization) Norm of wavefunction: 0.999994715779685
(Mid Optimization) Electronic Energy: 0.0022219946848426263
(Mid Optimization) Cost: 1.0568399059315789e-05
(Mid Optimization) Cost from constraints: 2.7922984337276587e-11
(Mid Optimization) Norm of the Jacobian: 263.0252879286794
       1              2         5.2842e-06      1.43e-11       3.41e+03       3.09e-10    
`gtol` termination condition is satisfied.
Function evaluations 2, initial cost 5.2842e-06, final cost 5.2842e-06, first-order optimality 3.09e-10.
Total execution time: 6.330204963684082 seconds
### Final energy: 3.3486786875982277
```
`example.log` has the complete output of a calculation. Note that the wavefunction parameters are not saved with the current input template. 
## Explanation of files

### `generate_dirs_and_inputs.py`
Generates the folder structure for FanPT calculations for a given wavefunction. It copies the templates over to their respective folders. This has the option of submitting all of the calculations as well on a cluster. Set `submit_calcs` to `True` to use this. Note: for each geometry and repetition 1 calculation is submitted.

The generated directory structure is:
```bash
CISD
└── efree_fanpt
    ├── order_1
    │   ├── steps_10
    │   │   ├── alpha-0.0
    │   │   ├── alpha-1.0
    │   │   ├── ...
    │   ├── steps_100
    │   │   ├── ...
    │   ├── steps_1000
    │   │   ├── ...
    ├── order_2
    ├── ...
```


### `submit_jobs.py`
Generates the geometry directories without submitting the calculations. This is only useful for initial tests/debugging purposes. 

### `submit_jobs_hpc.py`
Uses `sbatch` to submit the job specified in the job template (e.g. `job_cisd.txt`). The difference between `submit_jobs.py` and `submit_jobs_hpc.py` is that the line:
```python
        os.system('sbatch job.sh')
```
Is commented out in `submit_jobs.py` so that it does not try to submit the jobs. 

### `input_template_cisd.txt`
A file to run calculations with. The following words get replaced with the actual value:
* `ALPHA`: geometry param (e.g. 0.0 for BeH2)
* `IMPORT_GEOM`: geometry needed to run the PySCF calculation with
* `ORDER`: FanPT order 
* `STEPS`: FanPT steps

### `job_cisd.txt`
Job submission template. The `ORDER` , `STEPS` and `ALPHA` get replaced in the name of the job with the corresponding value.