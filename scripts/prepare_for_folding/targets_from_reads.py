# Script purpose is to have the exact target sequences that we expected
# separate 50 and 51 sequences, prepare targets for folding and clustering

import gzip
from collections import defaultdict
from Bio import SeqIO
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input reads in fastq.gz format", type=str, required=True)
    parser.add_argument("-o", "--output", help="Output reads in fasta format (path without the .extension)", type=str, required=True)
    parser.add_argument("-t", "--top", help="Print top of not unique targets", type=int, default=1)

    args = parser.parse_args()

    path_to_reads = args.input
    path_to_output = args.output
    top_targets = args.top

    # can be used to check top of not unique reads
    sequence_collection_number = defaultdict(int)

    count_50 = 0
    count_51 = 0

    with open(f"{path_to_output}_i50.fasta", 'w') as output_handler_i50, \
            open(f"{path_to_output}_i51.fasta", 'w') as output_handler_i51, \
            open(f"{path_to_output}_i50_51.fasta", 'w') as output_handler_i50_51:
        with open(f"{path_to_output}_only_targets.csv", 'w') as output_targets:
            with gzip.open(path_to_reads, "rt") as file_handle:

                sample_name = path_to_output.split("/")[-1].split("_")[0]

                for record in SeqIO.parse(file_handle, "fastq"):

                    sequence = str(record.seq)

                    if "N" not in sequence:

                        sequence_collection_number[sequence] += 1

                        sequence_len = len(sequence)

                        if sequence_len == 50:
                            if sequence[0:5] == "CTTAA" and \
                                    sequence[13:36] == "AATTTAAATTGATAATTTAAATT" \
                                    and sequence[41:] == "TTAAGACCA":

                                count_50 += 1

                                output_handler_i50.write(">" + record.name + "\n")
                                output_handler_i50.write(sequence + "\n")

                                output_handler_i50_51.write(">" + record.name + "\n")
                                output_handler_i50_51.write(sequence + "\n")

                                target_sequence = f"{sequence[5:13]}{sequence[36:41]}"
                                output_targets.write(f"{sample_name},{target_sequence}\n")

                        if sequence_len == 51:
                            if sequence[1:6] == "CTTAA" and \
                                    sequence[14:37] == "AATTTAAATTGATAATTTAAATT" \
                                    and sequence[42:] == "TTAAGACCA":

                                count_51 += 1

                                output_handler_i51.write(">" + record.name + "\n")
                                output_handler_i51.write(f"{sequence[1:]}" + "\n")

                                output_handler_i50_51.write(">" + record.name + "\n")
                                output_handler_i50_51.write(f"{sequence[1:]}" + "\n")

                                target_sequence = f"{sequence[6:14]}{sequence[37:42]}"
                                output_targets.write(f"{sample_name},{target_sequence}\n")

    print(f"Numer if reads: insertion 50b {count_50}, 51b {count_51} ")

    all_frequencies = []

    for sequence in sequence_collection_number:
        all_frequencies.append(sequence_collection_number[sequence])

    all_frequencies.sort()
    top = all_frequencies[-top_targets:]

    for sequence in sequence_collection_number:
        if sequence_collection_number[sequence] in top:
            print("Number of targets: ", sequence_collection_number[sequence])
            print("Sequence: ", sequence)
