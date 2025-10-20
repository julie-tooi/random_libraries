# Analysis description

## Project description

Experiments with *in vitro* molecule selection by proteins can demonstrate 
the optimal tRNA structure accepted by protein. 
Test protein in this case: EF-Tu (from *R. culicivorax*), which can accept 
truncated tRNAs. Test molecule: mt-tRNA-Ile.

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

#### Preprocessing

Reads trimming (in `reads_preprocessing`):

`snakemake --cores N --config input_dir="path/to/input" output_dir="path/to/output`

Collect run statistics

`python scripts/statistics_collection/run_statistics.py`

Read length distribution:

`python scripts/statistics_collection/length_distribution_per_sample.py`

