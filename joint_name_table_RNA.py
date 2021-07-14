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




#excel_file = 'TGCT_and_PanCan_MAF_DNA_VAF_only_TPM_geq_2.xlsx'
#excel_file = 'male_non_escaping_chrX_somatic_MAF_10_lineage_TPM_geq2.xlsx'
#excel_file = 'female_non_escaping_chrX_somatic_MAF_10_lineage_TPM_geq2.xlsx'


#df = pd.read_excel(excel_file,engine='openpyxl')

csv_file = 'TCGA-HC-7740_complete_MAF_TPM_geq2.csv'

df = pd.read_csv(csv_file)


#Wanted columns ['Truncated_Barcodes','Start_Position','Chromosome']
chr_column = df['Chromosome']
chr_start_column = df['Start_Position']
tumour_sample_column = df['Truncated_Barcodes']

column_list = len(chr_column)


#Now that we have the required chromosomal positions - we need to figure out how to run ASEreadcounter on these regions
#We first want all of the unique elemts in the tumour_sample_column:
#For each unique ID: we want to get the corresponding start and end position 
#So we can loop over each unique id: retuning their rows and hence we can extract the start and end pos


#Now that we have the required chromosomal positions - we need to figure out how to run ASEreadcounter on these regions
#We first want all of the unique elemts in the tumour_sample_column:
#For each unique ID: we want to get the corresponding start and end position 
#So we can loop over each unique id: retuning their rows and hence we can extract the start and end pos

#unique_id = list(np.unique(tumour_sample_column))

#index_list = [elem+'A' for ind, elem in enumerate(unique_id)]

unique_id = list(np.unique(tumour_sample_column))

case_id = [elem[:-3] for ind, elem in enumerate(unique_id)]


filename = 'gdc_sample_sheet.2019-06-24.tsv'

i=0
df = pd.read_csv(filename, sep='\t')
col_list = list(df.columns)  #List column names
#print(col_list)
sample_type_tum = ['Primary Tumor', 'Metastatic','Primary Blood Derived Cancer - Peripheral Blood']# 
sample_type_normal = ['Blood Derived Normal', 'Solid Tissue Normal'] #Two types of normals we can have

#Now check that the ID are present

ref_list = list(df['Case ID'])

#list1_as_set = set(ref_list)
#intersection = list1_as_set.intersection(index_list) 
#intersection_as_list = list(intersection)

#case_id = intersection_as_list



hg38_dir = '/tcga/tcga_RNASeq/tcga_RNASeq_BAM_FILES/' #Set relative path



sample_list_for_titan = []
i=0
tum_path = []
norm_path = []
total_index_paths = []
norm_case_id = []
tum_filename = []
norm_filename = []
wanted_extension = '01A'
for i in range(len(case_id)):
    if (case_id[i] in ref_list)==False:
        print (i)
        continue 
    #Get the index that matches the case_id
    index_tum = np.where((df['Case ID']==case_id[i]) & ( (df['Sample Type']==sample_type_tum[0]) | (df['Sample Type']==sample_type_tum[1]) | (df['Sample Type']==sample_type_tum[2]) ) )[0] #ref_list.index(case_id[i]) #Get the index for the tumour
    
    index_norm = np.where((df['Case ID']==case_id[i]) & ( (df['Sample Type'] == sample_type_normal[0]) | (df['Sample Type'] == sample_type_normal[1]) ))[0] #Get the index for the tumour
    
    if len(index_tum)>1:
        for z in range(len(index_tum)):
            if df['Sample ID'][z][-3:]==wanted_extension:
                index_tum = index_tum[z]
                print ('Multiple tumour samples Detected')

    #We now want both the file_id and filename
    file_id_tum = df['File ID'][index_tum]
    file_name_tum = df['File Name'][index_tum] #Our BAM file

    file_id_norm = df['File ID'][index_norm]
    file_name_norm = df['File Name'][index_norm] #Our BAM file

    # Now get the normal and tumour file paths
    tum_path += [hg38_dir + file_id_tum +'/' + file_name_tum]
    norm_path += [hg38_dir + file_id_norm +'/' + file_name_norm]

    #total_index_paths += [hg38_dir + file_id_tum +'/']
    tum_filename += [file_name_tum]
    norm_filename += [file_name_norm]
    norm_case_id += [case_id[i]]

'''
#Write out the joing filename + case ID 
output_norm_case_id = 'TCGA_maf_RNA_female_non_escape.txt'

with open(output_norm_case_id, 'w') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(zip(norm_case_id,tum_path))
'''




