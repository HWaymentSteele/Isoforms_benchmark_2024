import mdtraj as md
import numpy as np
import pandas as pd

model_selections={
'HBD': [[1,104]],#
'NFS': [[2,79]],#
'SETD': [[84,257],[268,287]], 
'EIF6': [[1,31],[105,205]], 
'IL4': [[0,114]], 
'MK14': [[3,256]], 
'PPAC': [[1,122]],
'TIP30': [[4,101]],
'CASP9': [[182,266]],
'CD2A': [[1,95]],
'CHIA': [[1,233]],
'TRDMT': [[1,58]], 
'AUHM': [[48,114]], 
'HER1': [[1,53]],
'MYG': [[1,95]],
'TF65': [[0,96]],
'WDR1': [[1,515]],
'PTGE': [[0,77]]
}

ref_selections={
'HBD': [[0,103]],
'NFS': [[7,29],[31,86]],
'SETD': [[59,251]], 
'EIF6': [[1,31],[124,224]],
'IL4': [[0,29],[45,130]],
'MK14': [[0,253]], 
'PPAC': [[0,39],[73,155]], 
'TIP30': [[0,97]], 
'CASP9': [[154,238]], 
'CD2A': [[52,146]],
'CHIA': [[141,373]], 
'TRDMT': [[0,57]], 
'AUHM': [[0,66]],
'HER1': [[95,147]], 
'MYG': [[55,149]], 
'TF65': [[0,36],[46,106]], 
'WDR1': [[0,514]],
'PTGE': [[0,63],[96,110]],
}

def parse_selections(sel_list):
    lst = []
    for sels in sel_list:
        lst.extend(range(sels[0],sels[1]))
    return lst

def get_contact_map(pdb_file, size=None, start_pos=0, end_pos=-1, cutoff=0.5):
    '''
    cutoff in nm
    '''
    
    pdb_obj = md.load_pdb(pdb_file)
    distances, pairs = md.compute_contacts(pdb_obj)
    contacts= md.geometry.squareform(distances, pairs)[0]
    if size is None:
        size = contacts.shape[0]
        
    arr=np.zeros([size, size])
    arr[np.where(contacts[start_pos:end_pos, start_pos:end_pos]<cutoff)]=1

    return arr

def get_n_contacts(contact_map):
    return np.sum(contact_map)/2/contact_map.shape[0]

def read_pLDDT(pdb_file):
    vals=[]

    with open(pdb_file,'r') as f:
        for lin in f.readlines()[1:-3]:
            fields = lin.split()
            if len(fields)>3 and fields[2] =='CA':
                vals.append(float(fields[-2]))

    if 'ESMF' in pdb_file and 'WDR1' not in pdb_file:
        vals = [100*x for x in vals]

    return vals

def read_SAP(pdb_file):
    seqs,saps=[],[]
    with open(pdb_file,'r') as f:
        for line in f:
            if not "per_res_sap" in line:
                continue

            sp = line.strip().split()
            seqpos = int(sp[0].split("_")[-1])
            sap = float(sp[1])

            seqs.append(seqpos)
            saps.append(sap)

    sorted_inds = np.argsort(seqs)
    #print([seqs[x] for x in sorted_inds])
    sap_vals = [saps[x] for x in sorted_inds]

    return sap_vals

def get_SAP_score(ID, model):
    ref_SAP = read_SAP('SAP_calculations/%s_REF_0001.pdb' % ID)
    mdl_SAP = read_SAP('SAP_calculations/%s_%s_0001.pdb' % (ID,model))
    plddt = read_pLDDT(model_paths[model] % ID)
    ref_SAP_masked = [ref_SAP[x] for x in parse_selections(ref_selections[ID])]
    mdl_SAP_masked = [mdl_SAP[x] for x in parse_selections(model_selections[ID])]
    plddt_masked = [plddt[x] for x in parse_selections(model_selections[ID])]

    print(len(ref_SAP_masked), len(mdl_SAP_masked))

    score = np.mean(np.subtract(mdl_SAP_masked, ref_SAP_masked) * plddt_masked)

    outputs = {'ref_SAP': ref_SAP, 'mdl_SAP': mdl_SAP, 'plddt': plddt, 'plddt_masked': plddt_masked,
    'ref_SAP_masked': ref_SAP_masked, 'mdl_SAP_masked': mdl_SAP_masked, 'score': score}

    return outputs


model_paths={'AF2': "models/AF2/%s_AF2.pdb",
'AF2_noMSA': "models/AF2_no_msa/%s_AF2_noMsa.pdb",
'OF':"models/omegafold/%s_OF.pdb",
'ESMF':"models/esmfold/%s_ESMF.pdb",
'RGN2_pre':"models/RGN2_pre/%s_RGN2_pre.pdb",
'RGN2':"models/RGN2/%s_RGN2.pdb"}

REF_path = 'models/ref_pdbs/%s_REF.pdb'

print('ID,model,n_contacts_by_length')

outputs_list = []
for ID in model_selections.keys():
    for model, path in model_paths.items():

        # get num contacts
        model_path = path % ID
        contact_map = get_contact_map(model_path)
        contacts = get_n_contacts(contact_map)
        print(','.join([ID,model,str(contacts)]))

        # get SAP_score
        outputs = get_SAP_score(ID, model)
        outputs['ID'] = ID
        outputs['model'] = model
        outputs['n_contacts'] = contacts
        outputs_list.append(outputs)

tmp = pd.DataFrame.from_records(outputs_list)

print(tmp.head())

tmp.to_json('outputs_19dec2022.json.zip')


