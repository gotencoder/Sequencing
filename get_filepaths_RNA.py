#This script will take in a list of TCGA data IDs and compare them with teh IDs in the HG38 manifest list (txt file)
#It will then obtain the file IDs from the corresponding match and will copy these files to a given directory
import csv
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
concat=False
for row in sheet.iter_rows(min_row=3,max_col=1):
        for cell in row:
            if (cell.value!=None):
                #print(cell.value, end="")
                if (concat==True):
                    index_list += [cell.value[:-3]]
                else:
                    index_list += [cell.value + 'A']

        #print()




filename = 'gdc_sample_sheet.2019-06-24.tsv'

i=0
df = pd.read_csv(filename, sep='\t')
col_list = list(df.columns)  #List column names
#print(col_list)
sample_type_tum = ['Primary Tumor', 'Metastatic','Primary Blood Derived Cancer - Peripheral Blood']# 
sample_type_normal = ['Blood Derived Normal', 'Solid Tissue Normal'] #Two types of normals we can have

#Now check that the ID are present

ref_list = list(df['Sample ID'])

list1_as_set = set(ref_list)
intersection = list1_as_set.intersection(index_list) 
intersection_as_list = list(intersection)

case_id = intersection_as_list



hg38_dir = '/tcga/tcga_RNASeq/tcga_RNASeq_BAM_FILES/' #Set relative path



sample_list_for_titan = []
i=0
tum_path = []
norm_path = []
total_index_paths = []
norm_case_id = []
for i in range(len(case_id)):
    #Get the index that matches the case_id
    index_tum = ref_list.index(case_id[i]) #Get the index for the tumour

    #We now want both the file_id and filename
    file_id_tum = df['File ID'][index_tum]
    file_name_tum = df['File Name'][index_tum] #Our BAM file

    # Now get the normal and tumour file paths
    tum_path += [hg38_dir + file_id_tum +'/' + file_name_tum]

    total_index_paths += [hg38_dir + file_id_tum +'/']

'''
#Now write two files, 1) normal and 2) tumour
output_tum = 'TCGA_RNA_tum_list.txt'

i=0
textfile_tum = open(output_tum, "w")
for i in tum_path:
    textfile_tum.write(i + "\n")
textfile_tum.close()
'''

