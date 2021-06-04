import pandas as pd
import numpy as np
import shutil
import os
import openpyxl
import matplotlib as mpl
import matplotlib.pylab as plt
import yaml



#Loop over the indexes in the excel file
excel_file = 'TCGA_Xena_15_TPM_cutoff_IDs_for_Imran.xlsx'

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
sample_type_tum = ['Primary Tumor', 'Metastatic']# 
sample_type_normal = ['Blood Derived Normal', 'Solid Tissue Normal'] #Two types of normals we can have

#Now check that the ID are present

ref_list = df['Case ID']

list1_as_set = set(index_list)
intersection = list1_as_set.intersection(ref_list)

case_id = [] #Reset the case id as we need the IDs that are present in the table

for z in intersection:
        case_id += [z]




sample_list_for_titan = []
total_n = len(case_id)
for i in range(1):
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
    hg38_dir = '../../../tcga-artemis/tcga_WXS/tcga_WXS_BAM_HG38_FILES/' #Set relative path


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
    sample_list_for_titan += ['tumour_sample_'+str(i+1)+': '+tum_path+tum_file]    #+1 to start from 1        
    sample_list_for_titan += ['normal_sample_'+str(i+1)+': '+norm_path+normal_file]    

'''
#Now save this to file
textfile = open("titan_sample_yaml.txt", "w")
textfile.write('samples: ' + "\n")
for element in sample_list_for_titan:
    textfile.write(element + "\n")
'''
#Now add the pairings
i=0
#textfile.write('pairings: ' + "\n")
pairings_text = []
for i in range(1):
    pairings_text += ['tumour_sample_'+str(i+1)+': '+'normal_sample_'+str(i+1)]
    #textfile.write(pairings_text + "\n")

#textfile.close()

#We need to save as a yaml file
output_file = 'output.yaml'
dict_file = [{'samples' : sample_list_for_titan},
{'pairings' : pairings_text }]

with open(output_file, 'w') as file:
    documents = yaml.dump(dict_file, file)







