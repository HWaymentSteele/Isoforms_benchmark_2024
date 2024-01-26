#module load gcc/4.8.5 rosetta
for x in ../incisive_isoforms/models/omegafold/*.pdb; do
/n/app/rosetta/3.13/source/bin/rosetta_scripts.default.linuxgccrelease -parser:protocol per_res_sap.xml -beta_nov16 -renumber_pdb -s $x
done
