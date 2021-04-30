#!/bin/bash
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=4G
#SBATCH -o DTRCC_14_LKidney_preAlignment_%j.out
#SBATCH -e DTRCC_14_LKidney_preAlignment_%j.err
#Step 0: Clear directory for temporary files
mkdir -p /cluster/singlecellcenter/DTRCC_14_LKidney;
rm -rf /cluster/singlecellcenter/DTRCC_14_LKidney/*;
#Step 1: Generate fastq files from unmapped bam
java -Xmx8g -jar /czlab/chzhang/github/picard-public/dist/picard.jar RevertSam TMP_DIR=/cluster/singlecellcenter/DTRCC_14_LKidney VALIDATION_STRINGENCY=SILENT INPUT=DTRCC_14_LKidney.bam OUTPUT=DTRCC_14_LKidney.unmapped.bam &>> DTRCC_14_LKidney.RevertSam.log 
#Step 2: Generate fastq files from unmapped bam
java -Xmx8g -jar /czlab/chzhang/github/picard-public/dist/picard.jar SamToFastq TMP_DIR=/cluster/singlecellcenter/DTRCC_14_LKidney INPUT=DTRCC_14_LKidney.unmapped.bam FASTQ=DTRCC_14_LKidney/DTRCC_14_LKidney.1.fastq.gz SECOND_END_FASTQ=DTRCC_14_LKidney/DTRCC_14_LKidney.2.fastq.gz INCLUDE_NON_PF_READS=true &>> DTRCC_14_LKidney.SamToFastq.log 
