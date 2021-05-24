#!/bin/bash
#SBATCH --job-name=seq_post_test
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=16G
#SBATCH --mail-type=END,FAIL         
#SBATCH --mail-user=imrant_nasim@dfci.harvard.edu
#SBATCH -o Seq_post_%j.out
#SBATCH -e Seq_post_%j.err

#Load in the modules
module load samtools/1.10


#Loop over all the bam files and extract the chrY bams

for i in *.bam
do
   samtools view -b $i chrY > "$(basename "$i" .bam)_chrY.bam"
done
