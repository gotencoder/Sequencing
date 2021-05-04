#!/bin/bash
#SBATCH --job-name=seq_pre_test2
#SBATCH --cpus-per-task=10
#SBATCH --mem-per-cpu=4G
#SBATCH --mail-type=END,FAIL         
#SBATCH --mail-user=imrant_nasim@dfci.harvard.edu
#SBATCH -o Seq_pre_%j.out
#SBATCH -e Seq_pre_%j.err

#Load required modules - load manually via command line anyway
module load picard/2.25.0

#Make a temp dir in /cluster/czlab and clear it
mkdir -p /cluster/czlab/temp;
rm -rf /cluster/czlab/temp/*;

#Use RevertSam to generate unmapped BAM from the Aligned BAM
#java -Xmx8g -Djava.io.tmpdir=/cluster/czlab/temp -jar /czlab/chzhang/github/picard-public/dist/picard.jar RevertSam INPUT=TCGA-BP-4756-01A-01D-1366-10_SOLiD.bam OUTPUT=TCGA-BP-4756-01A-01D-1366-10_unmapped_take2.bam VALIDATION_STRINGENCY=SILENT   &>> tmp_dir_test_take2.log



#Generate Fastq files from the unmapped bam file (generated above)
#Step 2: Generate fastq files from unmapped bam
# VALIDATION_STRINGENCY=SILENT IS VERY IMPORTANT! - otherwise you will get code crashing
#java -Xmx8g -Djava.io.tmpdir=/cluster/czlab/temp -jar /czlab/chzhang/github/picard-public/dist/picard.jar SamToFastq  INPUT=TCGA-BP-4756-01A-01D-1366-10_unmapped.bam FASTQ=TCGA-BP-4756-01A-01D-1366-10_take2.1.fastq.gz SECOND_END_FASTQ=TCGA-BP-4756-01A-01D-1366-10_take2.2.fastq.gz INCLUDE_NON_PF_READS=true VALIDATION_STRINGENCY=SILENT  &>> TCGA-BP-4756-01A-01D-1366-10_take2.SamToFastq.log
#java -Xmx8g -Djava.io.tmpdir=/cluster/czlab/temp -jar /czlab/chzhang/github/picard-public/dist/picard.jar SamToFastq  INPUT=6484_snippet_unmapped.bam FASTQ=6484_snippet_take2.1.fastq.gz SECOND_END_FASTQ=6484_snippet_take2.2.fastq.gz INCLUDE_NON_PF_READS=true VALIDATION_STRINGENCY=SILENT  &>> snippet_take2.SamToFastq.log




