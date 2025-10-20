# Script purpose - collect read lengths in different samples,
# prepare for visualisations

import argparse
import gzip
from collections import defaultdict
from glob import glob
from Bio import SeqIO


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Path to reads in fastq.gz format (fully processed T7_HH_HDV)", type=str, required=True)
    parser.add_argument("-o", "--output", help="Path to collected read length distribution", type=str, required=True)

    args = parser.parse_args()

    path_to_samples = args.input
    path_to_output = args.output

    samples = glob(path_to_samples)

    collection_len = dict()

    with open(path_to_output, 'w') as output:
        for sample in samples:
            sample_name = sample.split("/")[-1].split("_R1_")[0]
            sample_collection = defaultdict(int)

            with gzip.open(sample, "rt") as file_handle:
                for record in SeqIO.parse(file_handle, "fastq"):
                    sample_collection[len(record.seq)] += 1

            for read_len in sample_collection:
                output.write(f"{sample_name},{str(read_len)},{str(sample_collection[read_len])}\n")

    print("done")
