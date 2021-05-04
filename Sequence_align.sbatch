#!/bin/bash
#SBATCH --job-name=seq_align_test
#SBATCH --cpus-per-task=24
#SBATCH --mem-per-cpu=4G
#SBATCH --mail-type=END,FAIL         
#SBATCH --mail-user=imrant_nasim@dfci.harvard.edu
#SBATCH -o Seq_align_%j.out
#SBATCH -e Seq_align_%j.err

#Load required modules - load manually via command line anyway
module load picard/2.25.0
module load bwa/0.7.17-r1188
module load samtools/1.9.1


#Align the two fastq files with the bwa (burrow-wheeler algorithm)
bwa mem -t 24 /czlab/References/GRCh38/primary_assembly_plus_sponge/hg38.primary_assembly_plus_sponge.fa -Y -M /czlab/inasim/TCGA_data/TCGA_BP_4756/temp/TCGA-BP-4756-01A-01D-1366-10_take2.1.fastq.gz /czlab/inasim/TCGA_data/TCGA_BP_4756/temp/TCGA-BP-4756-01A-01D-1366-10_take2.2.fastq.gz 2>> TCGA-BP-4756-01A-01D-1366-10_take2.bwa_mem.log | samtools view -b - > TCGA-BP-4756-01A-01D-1366-10_take2.aligned.bam 2>> TCGA-BP-4756-01A-01D-1366-10_take2.bwa_mem.log
#bwa mem -t 24 /czlab/References/GRCh38/primary_assembly_plus_sponge/hg38.primary_assembly_plus_sponge.fa -Y -M 6484_snippet_take2.1.fastq.gz 6484_snippet_take2.2.fastq.gz 2>> snippet_take2.bwa_mem.log | samtools view -b - > snippet_take2.aligned.bam 2>> snippet_take2.bwa_mem.log




