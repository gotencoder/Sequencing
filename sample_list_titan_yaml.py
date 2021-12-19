import pandas as pd
import numpy as np
import shutil
import os
import openpyxl
import matplotlib as mpl
import matplotlib.pylab as plt
import yaml



'''#Load in our excel file
excel_file = 'LUSC_and_TGCT_revised.xlsx'

df = pd.read_excel(excel_file,engine='openpyxl')
tumour_sample_column = np.array( [elem[:-3] for i, elem in enumerate(list(df['Truncated_Barcodes']))] )'''


#excel_file = '6_4_TPM_geq3_XIST_pos_cutoff_IDs_for_Imran.xlsx'
#excel_file = 'XIST_neg_NSGCTs.xlsx'
#excel_file = 'samples_to_rerun_new_extension.xlsx'
excel_file = 'TCGA_tRCCs_purity_ploidy.xlsx'
df = pd.read_excel(excel_file,engine='openpyxl')
#csv_file = 'random_172_XISTpos_females.csv'
#csv_file = 'random_86_XISTneg_males.csv'
#df = pd.read_csv(csv_file)
tumour_sample_column = np.array( [elem[:-3] for i, elem in enumerate(list(df['Barcode']))] )
#tumour_sample_column = np.array( [elem[:-3] for i, elem in enumerate(list(df['Tumor_Sample_Barcode']))] )

#tumour_sample_column = np.array(['TCGA-77-6843'])

filename = 'tcga_WXS_BAM_HG38_FILES_gdc_sample_sheet.tsv'

i=0
df = pd.read_csv(filename, sep='\t')
col_list = list(df.columns)  #List column names
#print(col_list)
sample_type_tum = ['Primary Tumor', 'Metastatic','Primary Blood Derived Cancer - Peripheral Blood']# 
#sample_type_tum = ['Recurrent Tumor','Additional - New Primary']
sample_type_normal = ['Blood Derived Normal', 'Solid Tissue Normal'] #Two types of normals we can have

#Now check that the ID are present

ref_list = df['Case ID']

'''list1_as_set = set(index_list)
intersection = list1_as_set.intersection(ref_list)

case_id = [] #Reset the case id as we need the IDs that are present in the table

for z in intersection:
        case_id += [z]'''

#Get unique TCGA ids so we can obtain their path
case_id = np.unique(tumour_sample_column)
n_data = len(case_id)


sample_list_for_titan1 = []
sample_list_for_titan2 = []
total_n = len(case_id)
wanted_index = []
for i in range(n_data):
    #Get the index that matches the case_id
    index_tum = np.where((df['Case ID']==case_id[i]) & ( (df['Sample Type']==sample_type_tum[0]) | (df['Sample Type']==sample_type_tum[1]) ) )[0] #Get the index for the tumour

    index_norm = np.where((df['Case ID']==case_id[i]) & ( (df['Sample Type'] == sample_type_normal[0]) | (df['Sample Type'] == sample_type_normal[1]) ))[0] #Get the index for the tumour
 
    if (len(index_tum)==0 or len(index_norm)==0):
        print (i)
        continue

    #We now want both the file_id and filename
    file_id_tum = np.array(df['File ID'][index_tum])[0]
    file_name_tum = np.array(df['File Name'][index_tum])[0] #Our BAM file

    file_id_norm = np.array(df['File ID'][index_norm])[0]
    file_name_norm = np.array(df['File Name'][index_norm])[0] #Our BAM file

    #Now we look to copy thos files to our directory

    home_dir = os.getcwd()
    hg38_dir = '/tcga-artemis/tcga_WXS/tcga_WXS_BAM_HG38_FILES/' #Set relative path


    # Now get the normal and tumour file paths
    tum_path = hg38_dir + file_id_tum +'/'
    norm_path = hg38_dir + file_id_norm + '/' 


    path1_os = os.listdir(tum_path)

    
    for file_name in path1_os:
	    if (file_name[-3:]=='bam'):
	        #print (file_name)
                tum_file = file_name
	       

    path2_os = os.listdir(norm_path)


    for filename in path2_os:
            if (filename[-3:]=='bam'):
                    #shutil.copy(norm_path + filename,'./')
                print (filename)
                normal_file=filename
    
    #We now want a script to output the filenames and directories
    sample_list_for_titan1 += [case_id[i]+'_tumour_sample_'+str(i+1)]# +': '+tum_path+tum_file]    #+1 to start from 1        
    sample_list_for_titan1 += [case_id[i]+'_normal_sample_'+str(i+1)]#+': '+norm_path+normal_file]    
    sample_list_for_titan2 += [tum_path+tum_file]
    sample_list_for_titan2 += [norm_path+normal_file]
    wanted_index += [i]


i=0
pairings_text1 = []
pairings_text2 = []
for i in wanted_index:
    pairings_text1 += [case_id[i]+'_tumour_sample_'+str(i+1)]#+': '+'normal_sample_'+str(i+1)]
    pairings_text2 += [case_id[i]+'_normal_sample_'+str(i+1)]


#Now make nested dictionaries
#res1 = [{a: b} for (a, b) in zip(sample_list_for_titan1, sample_list_for_titan2)]
#res2 = [{c: d} for (c, d) in zip(pairings_text1, pairings_text2)]


#Define dictionary
dict1 = {}
dict1['samples'] = {}
dict1['pairings'] = {}

i=0
for i in range(len(sample_list_for_titan1)):
    dict1['samples'][sample_list_for_titan1[i]] = sample_list_for_titan2[i]

i=0
for i in range(len(pairings_text1)):
    dict1['pairings'][pairings_text1[i]] = pairings_text2[i]


#We need to save as a yaml file

#dict_file = [{'samples' : res1},{'pairings' : res2 }]
'''
output_file = 'samples_trcc.yaml'
with open(output_file, 'w') as file:
    documents = yaml.dump(dict1, file)

print(yaml.dump(dict1, sort_keys=False))
'''
#Print out the tumour/normal sample reference with their corresponding sample id 


    



