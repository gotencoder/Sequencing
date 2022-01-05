import csv
import pandas as pd
import numpy as np
import shutil
import os
import openpyxl
import matplotlib as mpl
import matplotlib.pylab as plt

df = pd.read_csv("TCGA_VAF_all_samples_ref_for_Titan_baitset_annotated.csv")

#change to new file with more options

uq_baitsets = ['Agilent Custom', 'Nimblegen hg18', 'Nimblegen HGSC', 'Nimblegen.SQEZ2', 'Nimblegen.SQEZ3', 'Sureselect.38']

case_id_superlist = []
extension_superlist = []

for a in uq_baitsets:
    df_temp = df[df['Baitset']==a]
    case_id_superlist.append(df_temp['Sub_ID'].tolist())
    extension_superlist.append(df_temp['Extension'].tolist())

print(len(case_id_superlist))
print(len(extension_superlist))

p=0
while p<len(case_id_superlist):
    
    case_id = case_id_superlist[p]
    extension_list = extension_superlist[p]

    filename = '/tcga-artemis/tcga_WXS/tcga_WXS_BAM_HG38_FILES_gdc_sample_sheet.tsv' #This is important
    
    i=0
    df = pd.read_csv(filename, sep='\t')
    col_list = list(df.columns)  #List column names
    sample_type_tum = ['Primary Tumor', 'Metastatic','Primary Blood Derived Cancer - Peripheral Blood']# 
    sample_type_normal = ['Blood Derived Normal', 'Solid Tissue Normal'] #Two types of normals we can have
    
    ref_list = df['Case ID']
    
    hg38_dir = '/tcga-artemis/tcga_WXS/tcga_WXS_BAM_HG38_FILES/' #Set relative path
    
    sample_list_for_titan = []
    i=0
    tum_path = []
    norm_path = []
    total_index_paths = []
    valid_case_ids = []
    tum_filename = []
    norm_filename = []
    for i in range(len(case_id)):
        #Get the index that matches the case_id
        #First check if the reference exists - if not add ['0'] so we can filter out in post-processing
        if len(np.where(df['Case ID']==case_id[i])[0])<=1:
            print (i)
            continue
    
        try:
            
            if extension_list[i] == 1:
        
                index_tum = np.where((df['Case ID']==case_id[i]) & ( (df['Sample Type']==sample_type_tum[0]) ) )[0] #Get the index for the tumour
            
            elif extension_list[i] == 3:
    
                index_tum = np.where((df['Case ID']==case_id[i]) & ( (df['Sample Type']==sample_type_tum[2]) ) )[0] #Get the index for the tumour
    
            elif extension_list[i] == 6:
                
                index_tum = np.where((df['Case ID']==case_id[i]) & ( (df['Sample Type']==sample_type_tum[1]) ) )[0] #Get the index for the tumour
    
            index_norm = np.where((df['Case ID']==case_id[i]) & ( (df['Sample Type']==sample_type_normal[0]) | (df['Sample Type']==sample_type_normal[1]) ) )[0] #Get the index for the normal            
    
            #We now want both the file_id and filename
            file_id_tum = np.array(df['File ID'][index_tum])[0]
            file_name_tum = np.array(df['File Name'][index_tum])[0] #Our BAM file
        
            #We now want both the file_id and filename
            file_id_norm = np.array(df['File ID'][index_norm])[0]
            file_name_norm = np.array(df['File Name'][index_norm])[0] #Our BAM file
    
            # Now get the normal and tumour file paths
            tum_path += [hg38_dir + file_id_tum +'/' + file_name_tum]
            norm_path += [hg38_dir + file_id_norm +'/' + file_name_norm]
    
        except:
            print(i)
            continue
    
        tum_filename.append(file_name_tum)
        norm_filename.append(file_name_norm)
        valid_case_ids.append(case_id)
        
        
    #generate config file

    base_lst = valid_case_ids
    
    lines_list = []
    
    a=0
    while a<len(base_lst):
         lines_list.append("  " + str(base_lst[a]) + "_Tumor:  " + str(tum_filename))
         lines_list.append("  " + str(base_lst[a]) + "_Normal:  " +  str(norm_filename))
         a=a+1
    
    pairings_list = []
    
    a=0
    while a<len(base_lst):
         pairings_list.append("  " + str(base_lst[a]) + "_Tumor:  " + str(base_lst[a]) + "_Normal")
         a=a+1
    
    textfile = open("samples_baitset_" + str(p) + ".yaml", "w")
    
    textfile.write("samples:" + "\n")
    
    for element in lines_list:
        textfile.write(element + "\n")
    
    textfile.write("pairings:" + "\n")
    
    for element in pairings_list:
        textfile.write(element + "\n")
    
    textfile.close()
    
    p=p+1
