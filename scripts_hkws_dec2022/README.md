

# To calculate per-residue SAP (surface aggregation propensity) score

If you have an existing Rosetta build, you can calculate the per-residue SAP score of any structure model by running

```
/PATH/TO/rosetta/3.13/source/bin/rosetta_scripts.default.linuxgccrelease -parser:protocol per_res_sap.xml -beta_nov16 -renumber_pdb -s <MODEL>.pdb
```

You can visualize the SAP scores on your structure model by opening PyMOL in the same directory as <MODEL>.pdb, opening <MODEL>.pdb, and then type

```
run per_res_sap.py
```

We provide here a copy of `per_res_sap.xml` and `per_res_sap.py` but take no credit for them, they were originally developed by Brian Coventry (Rosetta documentation [here](https://www.rosettacommons.org/docs/latest/rosetta_basics/scoring/sap-constraint).)


