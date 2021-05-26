import allel
import numpy as np
import matplotlib.pylab as plt
import matplotlib as mpl
from matplotlib.pyplot import cm
from matplotlib import rc
import glob
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#rc('text', usetex=True)



#file1 = 'C440.TCGA-HU-A4HD-10A-01D-A25E-08.3_gdc_realn.g.vcf'

file_list = glob.glob('*.vcf') #Gets all files ending with .bam
num_file = len(file_list)


for i in range(num_file):

    callset = allel.read_vcf(file_list[i],fields='*') #This extracts everything from a vcf
    callset.keys()
    #Get the allelic depths (AD in file) and also get the coords

    gt = allel.GenotypeArray(callset['calldata/GT'])

    count_het_sites = gt.count_het(axis=1) #This counts the het sites, =0 if (0/0 or 1/1) and =1 if alternate (0/1, 1/0)


    #Let us get the AF values and POS coordinates for chr17 and chrX and plot both of them
    chr17_index = np.where(callset['variants/CHROM']=='chr17')[0]
    chrX_index = np.where(callset['variants/CHROM']=='chrX')[0]

    chr17_pos = callset['variants/POS'][chr17_index] #Gets the positions on chr17
    chrX_pos = callset['variants/POS'][chrX_index] #Gets the positions on chrX

    chr17_AD = callset['calldata/AD'][chr17_index]
    chrX_AD = callset['calldata/AD'][chrX_index]

    #Now let us compute the ref/total allelic fraction : 

    chr17_AD_4d = chr17_AD[:,0]
    chrX_AD_4d = chrX_AD[:,0]


    chr17_AF = chr17_AD_4d[:,0] / (chr17_AD_4d[:,0] + chr17_AD_4d[:,1])
    chrX_AF = chrX_AD_4d[:,0] / (chrX_AD_4d[:,0] + chrX_AD_4d[:,1])



    #Now we can plot
    plt.ion()
    mpl.rcParams['axes.linewidth'] = 1.5
    ms=1.5
    lw = 2.0
    axis_labelsize = 12
    axis_fontsize = 12
    fig, axes = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=False, gridspec_kw={'hspace': 0, 'wspace': 0},figsize=(5,5))#,figsize=(6,4) inside to change the plot image
    (ax1)= axes

    ax1.semilogx(chr17_pos,chr17_AF,c='b',linestyle='',ms=ms,marker='o')

    ax1.set_ylim(-0.1,1.1)
    ax1.set_xlim(1e5, chr17_pos[-1])
    ax1.set_ylabel('AF',fontsize=axis_fontsize+3)
    ax1.set_xlabel('chr17 Pos',fontsize=axis_fontsize+3)
    ax1.minorticks_on()
    ax1.tick_params(which="both",bottom=True, top=True, left=True, right=True,direction='in',width=1.5,labelsize=axis_labelsize)
    ax1.tick_params(labelbottom=True, labeltop=False, labelleft=True, labelright=False) #Determines if you label them


    plt.tight_layout()
    plt.show() 
    plt.savefig(file_list[i] + '.chr17.pdf',format='pdf',bbox_inches='tight')
    plt.close()

    plt.ion()
    mpl.rcParams['axes.linewidth'] = 1.5
    ms=1.5
    lw = 2.0
    axis_labelsize = 12
    axis_fontsize = 12
    fig, axes = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=False, gridspec_kw={'hspace': 0, 'wspace': 0},figsize=(5,5))#,figsize=(6,4) inside to change the plot image
    (ax1)= axes

    ax1.semilogx(chrX_pos,chrX_AF,c='b',linestyle='',ms=ms,marker='o')

    ax1.set_ylim(-0.1,1.1)
    ax1.set_xlim(1e5, chr17_pos[-1])
    ax1.set_ylabel('AF',fontsize=axis_fontsize+3)
    ax1.set_xlabel('chrX Pos',fontsize=axis_fontsize+3)
    ax1.minorticks_on()
    ax1.tick_params(which="both",bottom=True, top=True, left=True, right=True,direction='in',width=1.5,labelsize=axis_labelsize)
    ax1.tick_params(labelbottom=True, labeltop=False, labelleft=True, labelright=False) #Determines if you label them


    plt.tight_layout()
    plt.show() 
    plt.savefig(file_list[i] + '.chrX.pdf',format='pdf',bbox_inches='tight')
    plt.close()







