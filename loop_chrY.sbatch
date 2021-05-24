#!/bin/bash
#SBATCH --job-name=seq_post_test
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=8G
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=imrant_nasim@dfci.harvard.edu
#SBATCH -o Seq_post_%j.out
#SBATCH -e Seq_post_%j.err


#Load in modules
module load samtools/1.10 #or whatever version you have

#Loop over all the bam files and extract the chrY bams

for i in *.bam
do
  echo "$(basename "$i" .bam)_chrY.bam" #This is a test to see if the renaming works!
done


for i in *.bam
do
   samtools view -b $i > "$(basename "$i" .bam)_chrY.bam"
done