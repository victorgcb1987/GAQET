# GAQET - Genome Annotation Quality Evaluation Tool

GAQET is a Python-based tool designed to evaluate the quality of genome annotations. Using GFF and FASTA files, GAQET generates statistical reports to help identify common errors and artifacts in gene structural annotations.


## Requirements

### Python Dependencies (??????)

- Python == 3.10
- ete3
- PyYAML

### Software dependencies
- AGAT == 1.4.2 (https://github.com/NBISweden/AGAT)
- GFFread == 0.12.7 (https://github.com/gpertea/gffread)
- BUSCO == 5.8.3 (https://github.com/WenchaoLin/BUSCO-Mod)
- LTR_retriever == 3.0.2 (https://github.com/oushujun/LTR_retriever)
- StringTie == 3.0.0 (https://github.com/gpertea/stringtie)

## Installation

Clone this repository:

```bash
git clone https://github.com/victorgcb1987/GAQET.git
```

Create a conda enviroment:

```bash
conda upgrade -c bioconda --all
conda create -c bioconda -n GAQET
conda activate GAQET
conda install -c bioconda agat
conda install -c bioconda gffread
conda install -c bioconda busco
conda install -c bioconda -c conda-forge ltr_retriever
  conda install python==3.10
```


## Usage

GAQET uses as a primary input a **File of files** as follows:
```yaml
ID: "SpeciesName"
Assembly: "/path/to/assembly.fasta"
Annotation: "/path/to/annotation.gff3"
Basedir: "/path/to/GAQET/results"
Threads: N
Analysis:
  - AGAT
  - BUSCO
  - PSAURON
  - DETENGA
  - OMARK
  - PROTHOMOLOGY
OMARK_db: "/path/to/omark_db.h5"
OMARK_taxid: NCBItaxonID
BUSCO_lineages:
  -  clade1_odb10
  -  clade2_odb10
PROTHOMOLOGY_tags:
  - TREMBL: "/path/to/uniprot_trembl_db.dmnd"
  - SWISSPROT: "/path/to/uniprot_swssprot.dmnd"
  - MYDB: "/path/to/mydb.dmnd"
DETENGA_db: "rexdb-plant"


```

| Parameter     | Description                                  |
|---------------|----------------------------------------------|
| ID            | Name of the species                     |
| Assembly      | FASTA genome file                            |
| Annotation    | GFF3/GTF annotation file                    |
| Basedir       | GAQET analysis and results directory       |
| Threads       | Number of threads       |
| Analysis      | List of analysis to run. All of them are optional      |
| OMARK_db      | Path to omark db. Only needed if OMARK is in Analysis      |
| OMARK_taxid | NCBI taxid for OMARK. Only needed if OMARK is in Analysis     |
| BUSCO_lineages | List of BUSCO clades to run. Only needed if BUSCO is in Analysis      |
| PROTHOMOLOGY_tags | List of name and path to DIAMOND proteins database. Only needed if  PROTHOMOLOGY is in Analysis     |
| DETENGA_db | DeTEnGA database for interpro checks. Only needed if DETENGA is in Analysis    |


With the YAML file you can **run GAQET** as follows:

```bash
GAQET --YAML {yaml_file}
```
Some YAML config file values can be override by using **GAQET arguments**:


| Parameter     | Description                                  |
|---------------|----------------------------------------------|
| --genome, -g          | Override YAML Assembly                     |
| --annotation, -a          | Override YAML Annotation                            |
| --taxid, -t          | Override NCBI taxid                    |
| --outbase, -o   | Override YAML outbase       |



```bash
GAQET --YAML {yaml_file} -g {assembly.fasta} -a annotation.gff -t 3702 -o {outdir
```
