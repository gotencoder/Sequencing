#This script will take in a list of TCGA data IDs and compare them with teh IDs in the HG38 manifest list (txt file)
#It will then obtain the file IDs from the corresponding match and will copy these files to a given directory

import pandas as pd
import numpy as np
import shutil
import os
import openpyxl
import matplotlib as mpl
import matplotlib.pylab as plt





#Loop over the indexes in the excel file
excel_file = '6_4_TPM_geq3_XIST_pos_cutoff_IDs_for_Imran.xlsx'

workbook = openpyxl.load_workbook(excel_file)

sheet = workbook.active

index_list = []
concat=True
for row in sheet.iter_rows(min_row=3,max_col=1):
        for cell in row:
            if (cell.value!=None):
                #print(cell.value, end="")
                if (concat==True):
                    index_list += [cell.value[:-3]]
                else:
                    index_list += [cell.value]

        #print()




filename = 'tcga_WXS_BAM_HG38_FILES_gdc_sample_sheet.tsv'

i=0
df = pd.read_csv(filename, sep='\t')
col_list = list(df.columns)  #List column names
#print(col_list)
sample_type_tum = ['Primary Tumor', 'Metastatic','Primary Blood Derived Cancer - Peripheral Blood']# 
sample_type_normal = ['Blood Derived Normal', 'Solid Tissue Normal'] #Two types of normals we can have

#Now check that the ID are present

ref_list = df['Case ID']

list1_as_set = set(ref_list)
intersection = list1_as_set.intersection(index_list) 
intersection_as_list = list(intersection)

case_id = intersection_as_list


#We need to check that the normal and tumour is present
temp_list = []
for i in range(len(case_id)):
    if (len(np.where(df['Case ID']==case_id[i])[0]) >=2):
        temp_list += [case_id[i]]
        print (i)
    else:
        continue    

case_id = temp_list


hg38_dir = '/tcga-artemis/tcga_WXS/tcga_WXS_BAM_HG38_FILES/' #Set relative path



sample_list_for_titan = []
i=0
tum_path = []
norm_path = []
for i in range(len(case_id)):
    #Get the index that matches the case_id
    index_tum = np.where((df['Case ID']==case_id[i]) & ( (df['Sample Type']==sample_type_tum[0]) | (df['Sample Type']==sample_type_tum[1]) | (df['Sample Type']==sample_type_tum[2]) ) )[0] #Get the index for the tumour

    index_norm = np.where((df['Case ID']==case_id[i]) & ( (df['Sample Type'] == sample_type_normal[0]) | (df['Sample Type'] == sample_type_normal[1]) ))[0] #Get the index for the tumour


    #We now want both the file_id and filename
    file_id_tum = np.array(df['File ID'][index_tum])[0]
    file_name_tum = np.array(df['File Name'][index_tum])[0] #Our BAM file

    file_id_norm = np.array(df['File ID'][index_norm])[0]
    file_name_norm = np.array(df['File Name'][index_norm])[0] #Our BAM file

    # Now get the normal and tumour file paths
    tum_path += [hg38_dir + file_id_tum +'/' + file_name_tum]
    norm_path += [hg38_dir + file_id_norm + '/' + file_name_norm]

'''
#Now write two files, 1) normal and 2) tumour
output_norm = 'TCGA_norm_list.txt'
output_tum = 'TCGA_tum_list.txt'

textfile_norm = open(output_norm, "w")
for element in norm_path:
    textfile_norm. write(element + "\n")
textfile_norm.close()

i=0
textfile_tum = open(output_tum, "w")
for i in tum_path:
    textfile_tum. write(i + "\n")
textfile_tum.close()
'''