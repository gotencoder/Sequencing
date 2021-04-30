#!/bin/bash
#SBATCH -c 2
#SBATCH --mem=16G
#SBATCH -o DTRCC_14_LKidney_%j.out
#SBATCH -e DTRCC_14_LKidney_%j.err
#Step 0: Clear directory for temporary files
mkdir -p /cluster/singlecellcenter/DTRCC_14_LKidney;
rm -rf /cluster/singlecellcenter/DTRCC_14_LKidney/*;
#Step 1: Merge aligned bam with unmapped bam and match paired alignments
#java -Xmx10g -jar /czlab/bin/HitsPairing.jar TMP_DIR=/cluster/singlecellcenter/DTRCC_14_LKidney INPUT=DTRCC_14_LKidney.aligned.bam OUTPUT=DTRCC_14_LKidney MATE_PAIR=false DISABLE_INSERT_INFERENCE=false SORT_ORDER=coordinate CHIMERA_KB_MIN=2000 IF_PROPER_FR=true IF_PROPER_RF=false IF_PROPER_FF=false VALIDATION_STRINGENCY=SILENT PREFERRED_ORIENTATION=FR UNMAPPED=DTRCC_14_LKidney.unmapped.bam ADD_RG=true &>> DTRCC_14_LKidney.HitsPairing.log 
#Step 2: Mark duplicates for primary reads
#java -Xmx10g -jar /czlab/chzhang/github/picard-public/dist/picard.jar MarkDuplicates TMP_DIR=/cluster/singlecellcenter/DTRCC_14_LKidney INPUT=DTRCC_14_LKidney.paired.bam OUTPUT=DTRCC_14_LKidney.primary-deduped.bam VALIDATION_STRINGENCY=SILENT MAX_RECORDS_IN_RAM=1000000 MAX_FILE_HANDLES_FOR_READ_ENDS_MAP=1000 SORTING_COLLECTION_SIZE_RATIO=0.15 METRICS_FILE=DTRCC_14_LKidney.duplicate_metrics ASSUME_SORTED=true &>> DTRCC_14_LKidney.MarkDuplicates.log 
#Step 3: Sort primary-deduped bam by read name
#java -Xmx8g -jar /czlab/chzhang/github/picard-public/dist/picard.jar SortSam TMP_DIR=/cluster/singlecellcenter/DTRCC_14_LKidney INPUT=DTRCC_14_LKidney.primary-deduped.bam OUTPUT=DTRCC_14_LKidney.primary-deduped.RNsorted.bam VALIDATION_STRINGENCY=SILENT SORT_ORDER=queryname &>> DTRCC_14_LKidney.SortSam.log 
#Step 4: Mark secondary/supplementary duplicates
java -Xmx8g -jar /czlab/bin/MarkDuplicatesForNonPrimary.jar TMP_DIR=/cluster/singlecellcenter/DTRCC_14_LKidney INPUT=DTRCC_14_LKidney.primary-deduped.RNsorted.bam OUTPUT=DTRCC_14_LKidney.bam SORT_ORDER=coordinate VALIDATION_STRINGENCY=SILENT  CREATE_INDEX=true &>> DTRCC_14_LKidney.MarkDuplicatesForNonPrimary.log 
#Step 5: Get discordant reads
#java -Xmx4g -jar /czlab/bin/GetDiscordantReadsFromQuerynameSortedBam.jar TMP_DIR=/cluster/singlecellcenter/DTRCC_14_LKidney INPUT=DTRCC_14_LKidney.primary-deduped.RNsorted.bam EXPECTED_ORIENTATION=FR MAX_INSERT=2000 DISABLE_INSERT_INFERENCE=false SORT_ORDER=coordinate IS_SAMPLE=1000000  MINIMUM_MAPPING_QUALITY=1 MAXIMUM_MISMATCHES=10 OUTPUT_DIR=/czlab/SequenceProcessing/Alignment &>> DTRCC_14_LKidney.GetDiscordantReadsFromQuerynameSortedBam.log 
#Step 6: Collect read depths
 java -Djava.io.tmpdir=/cluster/singlecellcenter/DTRCC_14_LKidney -Xmx8000m -jar /czlab/chzhang/github/gatk4/build/libs/gatk.jar CollectReadCounts -R /czlab/References/GRCh38/Homo_sapiens_assembly38.fasta --interval-merging-rule OVERLAPPING_ONLY --read-filter PassesVendorQualityCheckReadFilter --read-filter HasReadGroupReadFilter  --read-filter NotDuplicateReadFilter --read-filter MappingQualityAvailableReadFilter --read-filter PairedReadFilter 	--read-filter FragmentLengthReadFilter --max-fragment-length 1000 --read-filter MateOnSameContigOrNoMappedMateReadFilter --read-filter MateDifferentStrandReadFilter  --read-filter NotSupplementaryAlignmentReadFilter --read-filter NotSecondaryAlignmentReadFilter --read-filter FirstOfPairReadFilter --read-filter MappingQualityReadFilter --minimum-mapping-quality 30 --read-filter OverclippedReadFilter --filter-too-short 50  	    -L /czlab/References/GRCh38/hg38.10kb.interval_list --seconds-between-progress-updates 100 -I DTRCC_14_LKidney.bam -O DTRCC_14_LKidney.10kb_counts.txt --format TSV &>> DTRCC_14_LKidney.CollectRC.log 
#Step 7: Collect Allelic Counts
 java -Djava.io.tmpdir=/cluster/singlecellcenter/DTRCC_14_LKidney -Xmx8000m -jar /czlab/chzhang/github/gatk4/build/libs/gatk.jar ASEReadCounter -R /czlab/References/GRCh38/Homo_sapiens_assembly38.fasta --read-filter PassesVendorQualityCheckReadFilter --read-filter HasReadGroupReadFilter  --read-filter NotDuplicateReadFilter --read-filter MappingQualityAvailableReadFilter --read-filter MappingQualityReadFilter --minimum-mapping-quality 30 --read-filter OverclippedReadFilter --filter-too-short 25 --read-filter GoodCigarReadFilter --read-filter AmbiguousBaseReadFilter  	    -V /czlab/References/GRCh38/Broad/1000G_phase3_v4_20130502.snp.1percentAF.sites.hg38.vcf.gz --lenient --seconds-between-progress-updates 100 -I DTRCC_14_LKidney.bam -O DTRCC_14_LKidney.hetSNP.AD.txt --verbosity ERROR &>> DTRCC_14_LKidney.CollectAD.log 
#Step 8: Clear up
rm -rf /cluster/singlecellcenter/DTRCC_14_LKidney;
