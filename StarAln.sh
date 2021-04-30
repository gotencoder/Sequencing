#!/bin/bash

STAR_dir_oh75='/czlab/References/GRCh38/primary_assembly_plus_sponge/STAR_75overhang'
STAR_dir_oh150='/czlab/References/GRCh38/primary_assembly_plus_sponge/STAR_150overhang'
STAR_dir_oh100='/czlab/References/GRCh38/primary_assembly_plus_sponge/STAR_100overhang'

STAR_dir=${STAR_dir_oh100};
tmp_dir='./tmp';
#mkdir -p ${tmp_dir}
BA_SNP_vcf=HCC1954.vcf;

newSTAR='/czlab/Software/STAR/bin/Linux_x86_64/STAR';
input="SRR8616174_all.unmapped.bam";
output_prefix=HCC1954.SRR8616174.
${newSTAR} --runMode alignReads --runThreadN 8 \
	--genomeDir ${STAR_dir}\
	--twopassMode Basic \
	--alignSJoverhangMin 10 --alignSJDBoverhangMin 1 \
	--readFilesIn ${input} \
	--readFilesType SAM PE --readFilesCommand "samtools view" \
	--outFileNamePrefix ${output_prefix} \
	--outSAMtype BAM SortedByCoordinate \
	--quantMode TranscriptomeSAM GeneCounts \
	--outSAMunmapped Within KeepPairs \
	--outMultimapperOrder Random \
	--chimOutType WithinBAM SoftClip \
	--varVCFfile ${BA_SNP_vcf} \
	--outSAMattributes vA vG NH HI AS nM 
exit

--outTmpDir ${tmp_dir} \
--outSAMtype SAM \
	--outSAMorder PairedKeepInputOrder \
input="SRR8616174_1.fastq SRR8616174_2.fastq"
output_prefix=HCC1954.SRR8616174-allCombined.

${newSTAR} --runMode alignReads --runThreadN 8 \
	--genomeDir ${STAR_dir}\
	--twopassMode Basic \
	--alignSJoverhangMin 10 --alignSJDBoverhangMin 1 \
	--readFilesIn ${input} \
	--outFileNamePrefix ${output_prefix} \
	--outSAMtype BAM SortedByCoordinate \
	--outSAMunmapped Within KeepPairs \
	--outMultimapperOrder Random \
	--quantMode TranscriptomeSAM GeneCounts \
	--chimOutType WithinBAM SoftClip \
	--varVCFfile ${BA_SNP_vcf} \
	--outSAMattributes vA vG NH HI AS nM 
exit
--readFilesType SAM PE --readFilesCommand "samtools view" \ 
--outTmpDir ${tmp_dir} \
--outSAMtype SAM \
	--outSAMorder PairedKeepInputOrder \
	


#--genomeFastaFiles \ # for additional sequences such as spike-ins
#--readFilesIn ${reads1} ${reads2} --readFilesCommand zcat 
#--sjdbGTFfile --sjdbOverhang  # Not needed when the GTF is used during genome generation

# For short insert libraries
#--peOverlapNbasesMin 15 --peOverlapMMp 0.1

# For unmapped reads
# --outReadsUnmapped
for file in *.input
do
	prefix=`echo ${file} | sed "s:.input::"`
	python run_STAR.py /xchip/gtex/resources/STAR_genomes/STAR_genome_hg38_oh75 /cga/meyerson/References/GRCh38/gencode/gencode.v25.annotation.gtf ${file} ${prefix}
done

