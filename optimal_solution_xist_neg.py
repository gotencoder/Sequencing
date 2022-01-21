import numpy as np
import pandas as pd
import os
import glob



#Define a function to obtain the optimum ploidy solution given the two directories
def get_optimum_ploidy(direc):
	filenames = glob.glob(direc+'/*params.txt')
	optimum_ploidy = []
	seg_file = [] #Get the seg file that corresponds to the optimum ploidy solution
	sample_id_list = []
	ploidy_dif = []
	solution_list = []
	dir_len = len(direc)
	i=0
	for i in range(len(filenames)):
		#Find indexes where these samples are located
		sample_id = filenames[i][dir_len+1:dir_len+13]
		#print (filenames[i])
		#Now load in each filename and get the ploidy 
		df = pd.read_csv(filenames[i], delimiter = "\t",header=None)
		ploidy = np.float(np.array(df.loc[1][1]))
		absolute_sample_index = np.where(absolute_sample_list==sample_id)[0]
		if (len(absolute_sample_index)==0):
			continue
		absolute_ploidy = absolute_ploidy_list[absolute_sample_index]
		ploidy_dif += [np.absolute(ploidy-absolute_ploidy)]
		solution_list += [filenames[i][:-10]]
		seg_file +=  [filenames[i][:-10] + 'titan.ichor.seg.txt']
		sample_id_list += [sample_id]
		#print (ploidy_dif)

	sample_id_list = np.array(sample_id_list)
	ploidy_dif = np.array(ploidy_dif)
	seg_file = np.array(seg_file)
	unique_sample_list = np.unique(sample_id_list)
	i=0
	wanted_index = []
	wanted_seg = []
	wanted_ploidy = []
	for i in range(len(unique_sample_list)):
		unique_ind = np.where(sample_id_list==unique_sample_list[i])[0]
		ploid_val = ploidy_dif[unique_ind][0].astype('float32')
		min_ind = np.where(np.unique(ploid_val)==np.min(ploid_val))[0]
		tot_index = unique_ind[min_ind][0]
		wanted_index += [tot_index]
		wanted_ploidy += [ploidy_dif[tot_index]]
		wanted_seg += [seg_file[tot_index]]


	#Now we want to find the index of the of the minumum of ploidy diff
	#min_ind = ploidy_dif.index(min(ploidy_dif))
	#optimum_ploidy += [ploidy_dif[min_ind]]
	#sol = solution_list[min_ind]
	#Now get the segmental CN files so we can obtain the CN 
	#seg_file +=  [direc + sol + 'seg.txt']

	return wanted_ploidy,wanted_seg


def compare_optimum_solutions(ploidy2_sol, ploidy2_seg,ploidy3_sol, ploidy3_seg,ploidy4_sol, ploidy4_seg,ploidy5_sol, ploidy5_seg):
	n_sample = len(ploidy2_sol)
	i=0
	final_seg = []
	min_ploidy = []
	for i in range(n_sample):
		ploid_comp = [np.min(ploidy2_sol[i]),np.min(ploidy3_sol[i]),np.min(ploidy4_sol[i]),np.min(ploidy5_sol[i])]
		seg_comp = [ploidy2_seg[i],ploidy3_seg[i],ploidy4_seg[i],ploidy5_seg[i]]
		final_ind = ploid_comp.index(min(ploid_comp))
		final_seg += [seg_comp[final_ind]]
		min_ploidy += [np.min(ploid_comp)]

	return min_ploidy, final_seg	



#Load in the absolute values
absolute_file = 'random_86_XISTneg_males.csv'
df_abs = pd.read_csv(absolute_file)
absolute_sample_list = np.array([elem1[:-3] for ind1, elem1 in enumerate(list(df_abs['Barcode']))])
absolute_ploidy_list = np.array(df_abs['Ploidy'])
absolute_purity_list = df_abs['Purity']


#Aim of this script is to choose the optimal solution in Titan wrt ABSOLUTE
#We will do this by a ploid comparison
#We will first consider the solutions in each ploidy directory

ploidy2_dir = '/czlab/inasim/TitanCNA/scripts/snakemake/results_Xist_neg_pan_can/titan/hmm/titanCNA_ploidy2'
ploidy3_dir = '/czlab/inasim/TitanCNA/scripts/snakemake/results_Xist_neg_pan_can/titan/hmm/titanCNA_ploidy3'
ploidy4_dir = '/czlab/inasim/TitanCNA/scripts/snakemake/results_Xist_neg_pan_can/titan/hmm/titanCNA_ploidy4'
ploidy5_dir = '/czlab/inasim/TitanCNA/scripts/snakemake/results_Xist_neg_pan_can/titan/hmm/titanCNA_ploidy5'

ploidy2_sol, ploidy2_seg = get_optimum_ploidy(ploidy2_dir)
ploidy3_sol, ploidy3_seg = get_optimum_ploidy(ploidy3_dir)
ploidy4_sol, ploidy4_seg = get_optimum_ploidy(ploidy4_dir)
ploidy5_sol, ploidy5_seg = get_optimum_ploidy(ploidy5_dir)

final_ploid_dif, final_seg = compare_optimum_solutions(ploidy2_sol, ploidy2_seg,ploidy3_sol, ploidy3_seg,ploidy4_sol, ploidy4_seg,ploidy5_sol, ploidy5_seg)


opt_ploidy_dir = '/czlab/inasim/TitanCNA/scripts/snakemake/results/titan/hmm/optimalClusterSolution'
a1,b1 = get_optimum_ploidy(opt_ploidy_dir)
'''
#Now we want the parameter files in these dirs
optimum_ploidy = []
seg_file = [] #Get the seg file that corresponds to the optimum ploidy solution
filenames = glob.glob(ploidy2_dir+'/*params.txt')
for file_name in filenames:
	ploidy_dif = []
	solution_list = []
	if (file_name[-10:]=='params.txt'):
		sample_id = file_name[:12]
		print (file_name)
		#Now load in each filename and get the ploidy 
		df = pd.read_csv(file_name, delimiter = "\t",header=None)
		ploidy = np.float(df.loc[1][1])
		absolute_sample_index = np.where(absolute_sample_list==sample_id)[0]
		absolute_ploidy = absolute_ploidy_list[absolute_sample_index]
		ploidy_dif += [np.absolute(ploidy-absolute_ploidy)]
		solution_list += [file_name[-10:]]

	#Now we want to find the index of the of the minumum of ploidy diff
	min_ind = ploidy_dif.index(min(ploidy_dif))
	optimum_ploidy = ploidy_dif[min_ind]
	sol = solution_list[min_ind]
	#Now get the segmental CN files so we can obtain the CN 
	seg_file =  sol + 'seg.txt' 
'''
'''
direc = ploidy2_dir
filenames = glob.glob(direc+'/*params.txt')
optimum_ploidy = []
seg_file = [] #Get the seg file that corresponds to the optimum ploidy solution
sample_id_list = []
ploidy_dif = []
solution_list = []
dir_len = len(direc)
real_index = []
for i in range(len(filenames)):
	sample_id = filenames[i][dir_len+1:dir_len+13]
	#print (filenames[i])
	#Now load in each filename and get the ploidy 
	df = pd.read_csv(filenames[i], delimiter = "\t",header=None)
	ploidy = np.float(df.loc[1][1])
	absolute_sample_index = np.where(absolute_sample_list==sample_id)[0]
	#print (absolute_sample_index)
	if (len(absolute_sample_index)==0):
		continue

	absolute_ploidy = absolute_ploidy_list[absolute_sample_index]
	ploidy_dif += [np.absolute(ploidy-absolute_ploidy)]
	solution_list += [filenames[i][:-10]]
	seg_file +=  [filenames[i][dir_len+1:-10] + 'titan.ichor.seg.txt']
	real_index += [i]
	sample_id_list += [sample_id]
	#print (ploidy_dif)

sample_id_list = np.array(sample_id_list)
ploidy_dif = np.array(ploidy_dif)
unique_sample_list = np.unique(sample_id_list)
seg_file = np.array(seg_file)
i=0
wanted_index = []
wanted_seg = []
wanted_ploidy = []
for i in range(len(unique_sample_list)):
	unique_ind = np.where(sample_id_list==unique_sample_list[i])[0]
	ploid_val = ploidy_dif[unique_ind][0].astype('float32')
	min_ind = np.where(ploid_val==np.min(ploid_val))[0]
	tot_index = unique_ind[min_ind][0]
	wanted_index += [tot_index]
	wanted_ploidy += [ploidy_dif[tot_index]]
	wanted_seg += [seg_file[tot_index]]


i=0
#Now let us obtain the correct solutions for each ploidy case and then compare them
ploidy2_sol, ploidy2_seg = get_optimum_ploidy(ploidy2_dir)
ploidy3_sol, ploidy3_seg = get_optimum_ploidy(ploidy3_dir)

test_seg = compare_optimum_solutions(ploidy2_sol,ploidy2_seg,ploidy3_sol,ploidy3_seg)
'''

'''
#check that these arrays are equal length
if len(ploidy2_sol)==len(ploidy3_sol):
	print ('True')

n_sample = len(ploidy2_sol)
i=0
final_seg = []
for i in range(n_sample):
	ploid_comp = [np.min(ploidy2_sol[i]),np.min(ploidy3_sol[i])]
	seg_comp = [ploidy2_seg[i],ploidy3_seg[i]]
	final_ind = ploid_comp.index(min(ploid_comp))
	final_seg += [seg_comp[final_ind]]
'''
'''
#This should give us the list of seg files to analyse
#Now write to a txt file
out_file = 'optimum_solution_seg_files_xist_neg_pan_can.txt'
textfile = open(out_file, "w")

for element in final_seg:
	textfile.write(element + "\n")

textfile.close()
'''

#Get the param files for the optimum solutions and plot the 









