# Recognition of aberrant structures by EF-Tu

## Project description

Experiments with *in vitro* molecule selection by proteins can demonstrate 
the optimal tRNA structure accepted by protein. 

Test protein in this case: EF-Tu (from *R. culicivorax*), which can accept 
truncated tRNAs. 
Test molecule: mt-tRNA-Ile.

The experiment layout and library preparation steps (designed by Nadine Grafl):

![pools](plots/pools_prep.png)

## Data analysis steps

Analysis consists of several parts: 

1. Check library statistics, quality control
2. Prepare target sequences
3. Folding with following analysis

Before enrichment analysis, initial randomized pool were checked. 
Bias towards G and T bases was found, as a characteristic of molecules production.

![initial](plots/initial_pool.png)

### Pipeline

#### Requirements

What was used: 

snakemake 7.32.4

python 3.10.16

biopython 1.79


#### Preprocessing

Reads trimming (in `reads_preprocessing`):

`snakemake --cores N --config input_dir="path/to/input" output_dir="path/to/output`

Collect run statistics

```
python scripts/statistics_collection/run_statistics.py

usage: run_statistics.py [-h] -i_raw INPUT_RAW -i_tr INPUT_TRIMMED -o OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  -i_raw INPUT_RAW, --input_raw INPUT_RAW
                        Path to raw reads in fastq.gz format
  -i_tr INPUT_TRIMMED, --input_trimmed INPUT_TRIMMED
                        Path to reads in fastq.gz format (all stages)
  -o OUTPUT, --output OUTPUT
                        Path to collected stats
```

Read length distribution:

```
python scripts/statistics_collection/length_distribution_per_sample.py

usage: length_distribution_per_sample.py [-h] -i INPUT -o OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to reads in fastq.gz format (fully processed
                        T7_HH_HDV)
  -o OUTPUT, --output OUTPUT
                        Path to collected read length distribution
```

#### Prepare targets for folding

On this step two different files with targets are made: targets with length 50 and 51.
As we know that they can be analyzed together, and first base added unspecifically - two files can be simply unified with `cat`
(they have the same length 50)

```
usage: targets_from_reads.py [-h] -i INPUT -o OUTPUT [-t TOP]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input reads in fastq.gz format
  -o OUTPUT, --output OUTPUT
                        Output reads in fasta format (path without the
                        .extension)
  -t TOP, --top TOP     Print top of not unique targets
```

#### Folding

Generating open energies
`RNAplfold -O < inserts_i50_51.fasta`

Probability of being unpair:
`RNAplfold -u 2 < inserts_i50_51_fasta`

Collect folding results:
