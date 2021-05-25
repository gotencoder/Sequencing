#This script will take in a list of TCGA data IDs and compare them with teh IDs in the HG38 manifest list (txt file)
#It will then obtain the file IDs from the corresponding match and will copy these files to a given directory

import pandas as pd
import numpy as np
import shutil
import os
import openpyxl




#Loop over the indexes in the excel file
excel_file = 'XIST_pos_potential_males_for_Imran_1023_RSEM_cutoff.xlsx'

workbook = openpyxl.load_workbook(excel_file)

sheet = workbook.active

index_list = []

for row in sheet.iter_rows(min_row=2):
        for cell in row:
            if (cell.value!=None):
                #print(cell.value, end="")
                index_list += [cell.value]

        #print()




filename = 'tcga_WXS_BAM_HG38_FILES_gdc_sample_sheet.tsv'
case_id = index_list #['TCGA-BQ-7050']# This will an input from a excel file

i=0
df = pd.read_csv(filename, sep='\t')
col_list = list(df.columns)  #List column names
#print(col_list)
sample_type_tum = ['Primary Tumor', 'Metastatic']# 
sample_type_normal = ['Blood Derived Normal', 'Solid Tissue Normal'] #Two types of normals we can have

#Now check that the ID are present

ref_list = df['Case ID']

list1_as_set = set(index_list)
intersection = list1_as_set.intersection(ref_list)

case_id = [] #Reset the case id as we need the IDs that are present in the table

for z in intersection:
	case_id += [z]


for i in range(len(case_id)):
    #Get the index that matches the case_id
    index_tum = np.where((df['Case ID']==case_id[i]) & ( (df['Sample Type']==sample_type_tum[0]) | (df['Sample Type']==sample_type_tum[1]) ) )[0] #Get the index for the tumour

    index_norm = np.where((df['Case ID']==case_id[i]) & ( (df['Sample Type'] == sample_type_normal[0]) | (df['Sample Type'] == sample_type_normal[1]) ))[0] #Get the index for the tumour


    #We now want both the file_id and filename
    file_id_tum = np.array(df['File ID'][index_tum])[0]
    file_name_tum = np.array(df['File Name'][index_tum])[0] #Our BAM file

    file_id_norm = np.array(df['File ID'][index_norm])[0]
    file_name_norm = np.array(df['File Name'][index_norm])[0] #Our BAM file


    #print(file_id_tum)
    #print(file_name_tum)

    #print(file_id_norm)
    #print(file_name_norm)


    #Now we look to copy thos files to our directory

    home_dir = os.getcwd()
    hg38_dir = '../../../../tcga-artemis/tcga_WXS/tcga_WXS_BAM_HG38_FILES/' #Set relative path


    # Now get the normal and tumour file paths
    tum_path = hg38_dir + file_id_tum +'/'
    norm_path = hg38_dir + file_id_norm + '/' 


    path1_os = os.listdir(tum_path)

    
    for file_name in path1_os:
	    if (file_name[-3:-1]=='ba'):
		    print (file_name)
	        #shutil.copy(tum_path + file_name,'./')
                #print (file_name)
    	    

    path2_os = os.listdir(norm_path)


    for filename in path2_os:
            if (filename[-3:-1]=='ba'):
                    shutil.copy(norm_path + filename,'./')
                #print (filename)


		









