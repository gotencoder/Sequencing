#cluster specifications
#module load samtools
#module load bcftools
#initialize conda
#activate conda env

module load bcftools/1.10.2
module load samtools/1.10
module load R/4.04 

python3 TCGA_DS_script.py
valslist='LIFTOVER_whole_exome_agilent_1.1_refseq_plus_3_boosters.targetIntervals.with_chr.hg38.bed LIFTOVER_hg18_nimblegen_exome_version_2.hg38.bed LIFTOVER_VCRome_2_1_hg19_primary_targets.hg38.bed LIFTOVER_SeqCap_EZ_Exome_v2.hg38.bed LIFTOVER_SeqCap_EZ_Exome_v3_hg19_capture_targets.hg38.bed LIFTOVER_SureSelect_Human_All_Exon_V2_Regions.hg38.bed'

x=0
for N in ${valslist}; do \
        mv ${N} /czlab/inasim/${N}
        value_temp="s,abcdefgh,/czlab/inasim/${N},g"
        value_second="samples_baitset_${x}.yaml"
        rm /czlab/inasim/TitanCNA/scripts/snakemake/config/config.yaml
        cp config_template.yaml /czlab/inasim/TitanCNA/scripts/snakemake/config/config.yaml
        sed -i -e $value_temp /czlab/inasim/TitanCNA/scripts/snakemake/config/config.yaml
        rm /czlab/inasim/TitanCNA/scripts/snakemake/config/samples.yaml
        cp /czlab/inasim/$value_second /czlab/inasim/TitanCNA/scripts/snakemake/config/samples.yaml
        cd /czlab/inasim/TitanCNA/scripts/snakemake/
        snakemake -s TitanCNA.snakefile --cores 10
        mkdir /czlab/inasim/results_${x}
        mkdir /czlab/inasim/logs_${x}
        mv /czlab/inasim/TitanCNA/scripts/snakemake/results/ /czlab/inasim/results_${x}/
        mv /czlab/inasim/TitanCNA/scripts/snakemake/logs/ /czlab/inasim/logs_${x}/
        x=$(( $x + 1 ))
done