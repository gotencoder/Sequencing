#!/bin/bash
#SBATCH --cpus-per-task=24
#SBATCH --mem-per-cpu=4G
#SBATCH -o DTRCC_14_LKidney_bwa-mem_%j.out
#SBATCH -e DTRCC_14_LKidney_bwa-mem_%j.err
module load bwa/0.7.17-r1188
module load samtools/1.9.1
#Step 1: Align DTRCC_14_LKidney/DTRCC_14_LKidney.1.fastq.gz and DTRCC_14_LKidney/DTRCC_14_LKidney.2.fastq.gz with bwa mem
bwa mem -t 24 /czlab/References/GRCh38/primary_assembly_plus_sponge/hg38.primary_assembly_plus_sponge.fa -Y -M DTRCC_14_LKidney/DTRCC_14_LKidney.1.fastq.gz DTRCC_14_LKidney/DTRCC_14_LKidney.2.fastq.gz 2>> DTRCC_14_LKidney.bwa_mem.log | samtools view -b - > DTRCC_14_LKidney.aligned.bam 2>> DTRCC_14_LKidney.bwa_mem.log
