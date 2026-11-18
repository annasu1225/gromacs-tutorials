## Some guidance on troubleshooting

1. Warnings:
```
 gmx grompp -f run.mdp -c pr.gro -p topol.top -n index.ndx  -maxwarn 1 -o pull.tpr
```
Solutions:

(A) Increase ```-maxwarn 1``` to ```-maxwarn 3``` allows us to tolerate more warnings

(B) Resolve the Berendsen thermostat and barostat warnings by swtiching ```Tcoupl``` to ```V-rescale``` and ```Pcoupl``` to ```C-rescale```. The ```tau_t``` and ```tau_p``` should be changed accordingly. 
