import pysam
import numpy as np
import pandas as pd



def get_VAF(samfile,position,ref_base,map_quality=0,base_quality=0):
    chrom = "chrX"
    bases = list()
    alt = []
    vaf,alt_count,ref_count = 0,0,0
    for pileupcolumn in samfile.pileup(chrom, position, position+1):
        if pileupcolumn.pos==position:
            print ("\ncoverage at base %s = %s" % (pileupcolumn.pos, pileupcolumn.n))
            for r in pileupcolumn.pileups:
                        if not r.is_del and not r.is_refskip:
                            base = r.alignment.query_sequence[r.query_position-1]
                            mapq = r.alignment.mapping_quality
                            baseq = r.alignment.query_qualities[r.query_position-1]
                            if mapq >= map_quality and baseq >= base_quality:
                                bases.append(base)
            ref_count = 0
            depth = 0
            if len(bases)==0:
                vaf, ref_count, alt_count = 0,0,0 #This makes sure to return 0 for the values if the depth=0 (USEFUL FOR RNA)
                continue

            for base in bases:
                depth += 1
                if base == ref_base:
                    ref_count += 1
            alt_count = depth - ref_count
            vaf = alt_count/depth
    return vaf, ref_count, alt_count        
    




#We need to load in the excel file and the TCGA txt file containing the bam file names

excel_file = 'LUSC_and_TGCT_new.xlsx'

df = pd.read_excel(excel_file,engine='openpyxl')

chr_start_column = df['hg38_start']
tumour_sample_column = list(df['Truncated_Barcodes'])
tumour_sample_column = [elem[:-3] for ind, elem in enumerate(tumour_sample_column)]
variant_classification_column = df['Variant_Classification'] #We only want 'Silent' or 'Missense_Mutation'
#We also need the ref allele list
ref_allele_column = df['Reference_Allele']
n_data = len(tumour_sample_column)

#Load in the text file
joint_file_DNA = 'TCGA_maf_DNA_joint_list.txt'
joint_data_DNA = np.loadtxt(joint_file_DNA,dtype='str')
sample_id_DNA = joint_data_DNA[:,0]
bam_id_DNA = joint_data_DNA[:,1]

#Now load in the RNA joint data
joint_file_RNA = 'TCGA_maf_RNA_joint_list.txt'
joint_data_RNA = np.loadtxt(joint_file_RNA,dtype='str')
sample_id_RNA = np.array([elem1[:-4] for ind1, elem1 in enumerate( list(joint_data_RNA[:,0]) )])
bam_id_RNA = joint_data_RNA[:,1]


vaf_list_DNA = []
alt_list_DNA = []
ref_list_DNA = []

vaf_list_RNA = []
alt_list_RNA = []
ref_list_RNA = []

#vaf_DNA,alt_DNA,ref_DNA = 0,0,0
#vaf_RNA,alt_RNA,ref_RNA = 0,0,0

for i in range(n_data):
    sample = tumour_sample_column[i]
    position = chr_start_column[i]
    ref_base = ref_allele_column[i]

    #For the DNA
    bam_ind_DNA = np.where(sample_id_DNA==sample)[0]
    bam_file_DNA = bam_id_DNA[bam_ind_DNA][0]
    samfile_DNA = pysam.AlignmentFile(bam_file_DNA,"rb")
    vaf_DNA,alt_DNA,ref_DNA = get_VAF(samfile_DNA,position,ref_base)
    vaf_list_DNA += [vaf_DNA]
    alt_list_DNA += [alt_DNA]
    ref_list_DNA += [ref_DNA]
    #Now for the RNA
    bam_ind_RNA = np.where(sample_id_RNA==sample)[0]
    bam_file_RNA = bam_id_RNA[bam_ind_RNA][0]
    samfile_RNA = pysam.AlignmentFile(bam_file_RNA,"rb")
    vaf_RNA,alt_RNA,ref_RNA = get_VAF(samfile_RNA,position,ref_base)
    vaf_list_RNA += [vaf_RNA]
    alt_list_RNA += [alt_RNA]
    ref_list_RNA += [ref_RNA]

'''
#Now we can save these columns to the excel
df['DNA_alt_counts'] = alt_list_DNA 
df['DNA_ref_counts'] = ref_list_DNA
df['DNA_VAF'] = vaf_list_DNA

df['RNA_alt_counts'] = alt_list_RNA 
df['RNA_ref_counts'] = ref_list_RNA
df['RNA_VAF'] = vaf_list_RNA

df.to_excel('LUSC_and_TGCT_revised.xlsx')
'''
