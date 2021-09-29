#!/bin/bash
#SBATCH --job-name=seq_post_test
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=16G
#SBATCH --mail-type=END,FAIL         
#SBATCH --mail-user=imrant_nasim@dfci.harvard.edu
#SBATCH -o Seq_post_%j.out
#SBATCH -e Seq_post_%j.err

#Load required modules - load manually via command line anyway
#module load picard/2.25.0
module load bwa/0.7.17-r1188
module load samtools/1.10
module load gatk/4.1.2.0

#Make a temporary directory
mkdir -p /cluster/czlab/temp;
rm -rf /cluster/czlab/temp/*;

#There are multiple steps invloved in the post processing - so we will consider each step individually
#Step 1: Merge aligned bam with unmapped bam and match paired alignments
java -Xmx8g  -Djava.io.tmpdir=/cluster/czlab/temp -jar /czlab/bin/HitsPairing.jar INPUT=TCGA-BP-4756-01A-01D-1366-10_aligned_sort.bam OUTPUT=TCGA-BP-4756-01A-01D-1366-10_sort MATE_PAIR=false DISABLE_INSERT_INFERENCE=false SORT_ORDER=coordinate CHIMERA_KB_MIN=2000 IF_PROPER_FR=true IF_PROPER_RF=false IF_PROPER_FF=false VALIDATION_STRINGENCY=SILENT PREFERRED_ORIENTATION=FR UNMAPPED=TCGA-BP-4756-01A-01D-1366-10_unmapped_sort.bam ADD_RG=true MAX_RECORDS_IN_RAM=500000  &>> TCGA-BP-4756-01A-01D-1366-10_sort.HitsPairing.log 
#Step 1 alternative (I wonder wheather this will work as the same as the above step)
#java -Xmx10g  -Djava.io.tmpdir=/cluster/czlab/temp2 -jar /data/programs/picard/2.25.0/picard.jar MergeBamAlignment ALIGNED=TCGA-BP-4756-01A-01D-1366-10_take2.aligned.bam UNMAPPED=TCGA-BP-4756-01A-01D-1366-10_unmapped.bam O=TCGA-BP-4756-01A-01D-1366-10_merge_alignments.bam R=/czlab/References/GRCh38/Homo_sapiens_assembly38.fasta SORT_ORDER=coordinate VALIDATION_STRINGENCY=SILENT &>> TCGA-BP-4756-01A-01D-1366-10_merge.log
#Step 2: Mark duplicates for primary reads
#java -Xmx10g  -Djava.io.tmpdir=/cluster/czlab/temp -jar /czlab/chzhang/github/picard-public/dist/picard.jar MarkDuplicates INPUT=blah.paired.bam OUTPUT=blah.primary-deduped.bam VALIDATION_STRINGENCY=SILENT MAX_RECORDS_IN_RAM=1000000 MAX_FILE_HANDLES_FOR_READ_ENDS_MAP=1000 SORTING_COLLECTION_SIZE_RATIO=0.15 METRICS_FILE=DTRCC_14_LKidney.duplicate_metrics ASSUME_SORTED=true &>> blah.MarkDuplicates.log 
#Step 3: Sort primary-deduped bam by read name
#java -Xmx8g -Djava.io.tmpdir=/cluster/czlab/temp -jar /czlab/chzhang/github/picard-public/dist/picard.jar SortSam INPUT=blah.primary-deduped.bam OUTPUT=blah.primary-deduped.RNsorted.bam VALIDATION_STRINGENCY=SILENT SORT_ORDER=queryname &>> blah.SortSam.log 
#Step 4: Mark secondary/supplementary duplicates
#java -Xmx8g -Djava.io.tmpdir=/cluster/czlab/temp -jar /czlab/bin/MarkDuplicatesForNonPrimary.jar INPUT=blah.primary-deduped.RNsorted.bam OUTPUT=blah.bam SORT_ORDER=coordinate VALIDATION_STRINGENCY=SILENT  CREATE_INDEX=true &>> blah.MarkDuplicatesForNonPrimary.log 
#Step 5: Get discordant reads
#java -Xmx4g -Djava.io.tmpdir=/cluster/czlab/temp  -jar /czlab/bin/GetDiscordantReadsFromQuerynameSortedBam.jar INPUT=blah.primary-deduped.RNsorted.bam EXPECTED_ORIENTATION=FR MAX_INSERT=2000 DISABLE_INSERT_INFERENCE=false SORT_ORDER=coordinate IS_SAMPLE=1000000  MINIMUM_MAPPING_QUALITY=1 MAXIMUM_MISMATCHES=10 OUTPUT_DIR=/path/to/wanted/dir &>> blah.GetDiscordantReadsFromQuerynameSortedBam.log 
#Step 6: Collect read depths (Notes below)
# 1) interval-merging-rule OVERLAPPING_ONLY ---- STANDARD GATK OPTION
# 2) read-filter ---- Essentially applying filters to check that the INPUT file is of the correct quality (quality control before analysis)
# 3) minimum-mapping-quality ---- parameter that relates to the MappingQualityReadFilter 
# 4) max-fragment-length ---- parameter that relates to the FragmentLengthReadFilter
# 5) filter-too-short ---- parameter that relates to the OverclippedReadFilter
#java -Djava.io.tmpdir=/cluster/czlab/temp -Xmx8000m -jar /czlab/chzhang/github/gatk4/build/libs/gatk.jar CollectReadCounts -R /czlab/References/GRCh38/Homo_sapiens_assembly38.fasta --interval-merging-rule OVERLAPPING_ONLY --read-filter PassesVendorQualityCheckReadFilter --read-filter HasReadGroupReadFilter  --read-filter NotDuplicateReadFilter --read-filter MappingQualityAvailableReadFilter --read-filter PairedReadFilter 	--read-filter FragmentLengthReadFilter --max-fragment-length 1000 --read-filter MateOnSameContigOrNoMappedMateReadFilter --read-filter MateDifferentStrandReadFilter  --read-filter NotSupplementaryAlignmentReadFilter --read-filter NotSecondaryAlignmentReadFilter --read-filter FirstOfPairReadFilter --read-filter MappingQualityReadFilter --minimum-mapping-quality 30 --read-filter OverclippedReadFilter --filter-too-short 50  	    -L /czlab/References/GRCh38/hg38.10kb.interval_list --seconds-between-progress-updates 100 -I DTRCC_14_LKidney.bam -O DTRCC_14_LKidney.10kb_counts.txt --format TSV &>> DTRCC_14_LKidney.CollectRC.log 
#java -Xmx8000m -Djava.io.tmpdir=/cluster/czlab/temp -jar /czlab/chzhang/github/gatk4/build/libs/gatk.jar CollectReadCounts -R /czlab/References/GRCh38/Homo_sapiens_assembly38.fasta --interval-merging-rule OVERLAPPING_ONLY --read-filter PassesVendorQualityCheckReadFilter --read-filter HasReadGroupReadFilter  --read-filter NotDuplicateReadFilter --read-filter MappingQualityAvailableReadFilter --read-filter PairedReadFilter 	--read-filter FragmentLengthReadFilter --max-fragment-length 1000 --read-filter MateOnSameContigOrNoMappedMateReadFilter --read-filter MateDifferentStrandReadFilter  --read-filter NotSupplementaryAlignmentReadFilter --read-filter NotSecondaryAlignmentReadFilter --read-filter FirstOfPairReadFilter --read-filter MappingQualityReadFilter --minimum-mapping-quality 30 --read-filter OverclippedReadFilter --filter-too-short 50  	    -L /czlab/References/GRCh38/hg38.10kb.interval_list --seconds-between-progress-updates 100 INPUT=DTRCC_14_LKidney.bam OUTPUT=blah.10kb_counts.txt --format TSV &>> blah.CollectRC.log 
#Step 7: Collect Allelic Counts
# As with Step 6 - all of these read filters are compulsory
#java -Djava.io.tmpdir=/cluster/czlab/temp -Xmx8000m -jar /czlab/chzhang/github/gatk4/build/libs/gatk.jar ASEReadCounter -R /czlab/References/GRCh38/Homo_sapiens_assembly38.fasta --read-filter PassesVendorQualityCheckReadFilter --read-filter HasReadGroupReadFilter  --read-filter NotDuplicateReadFilter --read-filter MappingQualityAvailableReadFilter --read-filter MappingQualityReadFilter --minimum-mapping-quality 30 --read-filter OverclippedReadFilter --filter-too-short 25 --read-filter GoodCigarReadFilter --read-filter AmbiguousBaseReadFilter  	    -V /czlab/References/GRCh38/Broad/1000G_phase3_v4_20130502.snp.1percentAF.sites.hg38.vcf.gz --lenient --seconds-between-progress-updates 100 -I DTRCC_14_LKidney.bam -O DTRCC_14_LKidney.hetSNP.AD.txt --verbosity ERROR &>> DTRCC_14_LKidney.CollectAD.log 
#java -Xmx8000m -Djava.io.tmpdir=/cluster/czlab/temp -jar /czlab/chzhang/github/gatk4/build/libs/gatk.jar ASEReadCounter -R /czlab/References/GRCh38/Homo_sapiens_assembly38.fasta --read-filter PassesVendorQualityCheckReadFilter --read-filter HasReadGroupReadFilter  --read-filter NotDuplicateReadFilter --read-filter MappingQualityAvailableReadFilter --read-filter MappingQualityReadFilter --minimum-mapping-quality 30 --read-filter OverclippedReadFilter --filter-too-short 25 --read-filter GoodCigarReadFilter --read-filter AmbiguousBaseReadFilter  	    -V /czlab/References/GRCh38/Broad/1000G_phase3_v4_20130502.snp.1percentAF.sites.hg38.vcf.gz --lenient --seconds-between-progress-updates 100 INPUT=blah.bam OUTPUT=blah.hetSNP.AD.txt --verbosity ERROR &>> blah.CollectAD.log 
#Step 8: Clear up
#rm -rf /cluster/czlab/temp;
