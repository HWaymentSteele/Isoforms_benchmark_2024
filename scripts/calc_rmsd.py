from pymol import cmd, util
import sys

model_list=['AF2','AF2_no_msa','OF','EF','RGN2_pre','RGN2']

ref_selections={
'HBD': 'resi 1-104',
'SETD': 'resi 59-251',
'NFS': 'resi 7-84',
'EIF6':'(resi 1-31 or resi 124-224)',
'IL4': '(resi 0-28 or resi 45-129)',
'MK14': 'resi 4-310',
'PPAC': '(resi 1-38 or resi 74-155)',
'TIP30': 'resi 5-101',
'CASP9': 'resi 316-416',
'CD2A': 'resi 52-146',
'CHIA': 'resi 141-373',
'TRDMT': 'resi 2-58',
'AUHM': 'resi 74-139',
'HER1': 'resi 113-164',
'MYG': 'resi 55-149',
'TF65': '(resi 186-221 or resi 232-292)',
'WDR1': 'resi 1-517',
'PTGE': '(resi 1-62 or resi 96-110)'
}

model_selections={
'HBD': 'resi 1-104',
'SETD': 'resi 84-287',
'NFS': 'resi 2-76',
'EIF6': '(resi 1-31 or resi 105-205)',
'IL4': 'resi 1-114',
'MK14': 'resi 1-307',
'PPAC': 'resi 2-122',
'TIP30': 'resi 5-101',
'CASP9': 'resi 166-266',
'CD2A': 'resi 1-95',
'CHIA': 'resi 1-233',
'TRDMT': 'resi 2-58',
'AUHM': 'resi 49-114',
'HER1': 'resi 2-53',
'MYG': 'resi 1-95',
'PTGE': 'resi 1-77',
'TF65': 'resi 1-97',
'WDR1': 'resi 1-517'
}

header = ['ID']+model_list

f1 = open('ref_RMSD_output.csv','w')
f1.write(','.join(header)+'\n')
f2 = open('pairwise_dists.csv','w')
f2.write("ID,model1,model2,RMSD\n")

for ID in model_selections.keys():
	print(ID)
	cmd.load('models/ref_pdbs/%s_REF.pdb' % (ID), 'ref')
	cmd.load("models/AF2/%s_AF2.pdb" % ID,"AF2")
	cmd.load("models/AF2_no_msa/%s_AF2_noMSA.pdb" % ID,"AF2_no_msa")
	cmd.load("models/omegafold/%s_OF.pdb" % ID,"OF")
	cmd.load("models/esmfold/%s_ESMF.pdb" % ID,"EF")
	cmd.load("models/RGN2_pre/%s_RGN2_pre.pdb" % ID,"RGN2_pre")	
	cmd.load("models/RGN2/%s_RGN2.pdb" % ID,"RGN2")

	cmd.set('valence', 0)
	cmd.remove('hydrogens')
	
	output_list=[ID]
	for mdl in model_list:
		rms = cmd.align("ref and name CA and %s" % ref_selections[ID], "%s and name CA and %s" % (mdl, model_selections[ID]))[0]
		output_list.append(rms)

	f1.write(','.join([str(x) for x in output_list])+'\n')

	for i, mdl1 in enumerate(model_list):
		for j, mdl2 in enumerate(model_list[i+1:]):
			mdl_sele = model_selections[ID]
			rms = cmd.align("%s and name CA and %s" %(mdl1, mdl_sele), "%s and name CA and %s" %(mdl2, mdl_sele))[0]
			f2.write("%s,%s,%s,%.6f\n" % (ID, mdl1, mdl2, rms))

	cmd.delete('all')

f1.close()
f2.close()
