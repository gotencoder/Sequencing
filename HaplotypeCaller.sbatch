#!/bin/bash
#SBATCH --job-name=seq_post_test
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=16G
#SBATCH --mail-type=END,FAIL         
#SBATCH --mail-user=imrant_nasim@dfci.harvard.edu
#SBATCH -o Seq_post_%j.out
#SBATCH -e Seq_post_%j.err

#Load required modules - load manually via command line anyway
#module load picard/2.25.0 #Either load in this version or CZs version


#Make a temporary directory
mkdir -p /cluster/czlab/temp;
rm -rf /cluster/czlab/temp/*;


#Set reference paths
hg38_ref='/czlab/References/GRCh38/Homo_sapiens_assembly38.fasta'
GATK='/czlab/chzhang/github/gatk4/build/libs/gatk.jar'


#Set file names
#INPUT_FILE='/czlab/inasim/TCGA_data/X_ist/C440.TCGA-HU-A4HD-10A-01D-A25E-08.3_gdc_realn.bam'
#INPUT_FILE='C440.TCGA-HU-A4HD-10A-01D-A25E-08.3_gdc_realn.bam'
#output_file="$(basename "$INPUT_FILE" .bam)_prac."
#log_file='logfile.'

#Set chromosome list
#CHR_list=('chr1' 'chr2' 'chr3' 'chr4' 'chr5' 'chr6' 'chr7' 'chr8' 'chr9' 'chr10' 'chr11' 'chr12' 'chr13' 'chr14' 'chr15' 'chr16' 'chr17' 'chr18' 'chr19' 'chr20' 'chr21' 'chr22' 'chrX' 'chrY')
CHR_list=('chr17' 'chrX') #You can also set individual chromosomes



for j in *.bam
do
for i in "${CHR_list[@]}"
do
  java -Xmx8000m -Djava.io.tmpdir=/cluster/czlab/temp -jar $GATK \
      HaplotypeCaller \
     -R $hg38_ref \
     -I $j \
     -L $i \
     -O "$(basename "$j" .bam)_prac."$i"_g.vcf" &>> "$(basename "$j" .bam)_log."$i".log"
done
done

#Clean temp dir
rm -rf /cluster/czlab/temp;
