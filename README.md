# Repo for learning MD simulations with GROMACS

## Set up

For loading modules on the HITS cluster:
```
module load Stage/2025b  GCC/14.3.0  OpenMPI/5.0.8
```

For cpu only nodes:
```
module load GROMACS/2025.2
```

For gpu nodes:
```
module load GROMACS/2025.3-CUDA-12.9.1
```

## Visualization in PyMol
1. Load the PDB file
```
load structure_name.pdb
```
2. Load the trajectory file onto the PDB structure
```
load traj_file.xtc, structure_name
```