# Script purpose - collect run statistics on different trim stages
# Number of reads after trimming steps collected for 50- and 51-length insertions separately
# Additionally, number of unique reads collected, to check the selection process

import argparse
import gzip
from collections import defaultdict
from glob import glob
from Bio import SeqIO


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i_raw", "--input_raw", help="Path to raw reads in fastq.gz format", type=str, required=True)
    parser.add_argument("-i_tr", "--input_trimmed", help="Path to reads in fastq.gz format (all stages)", type=str, required=True)
    parser.add_argument("-o", "--output", help="Path to collected stats", type=str, required=True)

    args = parser.parse_args()

    raw_reads = glob(args.input_raw)
    trimmed_reads = glob(args.input_trimmed)
    path_to_output = args.output

    stats_collection = defaultdict(list)

    # total number of raw reads
    for raw_sample in raw_reads:
        raw_sample_name = raw_sample.split("/")[-1].split("_R1_")[0]
        reads_number = 0
        with gzip.open(raw_sample, "rt") as file_handle:
            for record in SeqIO.parse(file_handle, "fastq"):
                if record.seq:
                    reads_number += 1

        stats_collection[raw_sample_name].append(("raw_reads", reads_number))

    for trimmed_sample in trimmed_reads:
        raw_sample_name = trimmed_sample.split("/")[-1].split("_R1_")[0]

        reads_number = 0
        neg_control_reads_number = 0

        unique_reads_ins_50 = set()
        reads_number_50 = 0
        unique_reads_ins_51 = set()
        reads_number_51 = 0

        with gzip.open(trimmed_sample, "rt") as file_handle:
            for record in SeqIO.parse(file_handle, "fastq"):
                # total reads number
                if record.seq:
                    reads_number += 1
                    # check control reads
                    if "AAACTTTTAGCAGGATTTCGAATCCTAATTTATATAAGTTTTCCA" in record.seq:
                        neg_control_reads_number += 1
                    # check test molecule
                    elif "N" not in record.seq:
                        if "_T7_HH_HDV." in trimmed_sample:
                            if len(record.seq) == 50:
                                unique_reads_ins_50.add(str(record.seq))
                                reads_number_50 += 1
                            if len(record.seq) == 51:
                                unique_reads_ins_51.add(str(record.seq))
                                reads_number_51 += 1
        if "_T7." in trimmed_sample:
            stats_collection[raw_sample_name].append(("T7", reads_number, neg_control_reads_number))
        elif "_T7_HH." in trimmed_sample:
            stats_collection[raw_sample_name].append(("HH", reads_number, neg_control_reads_number))
        elif "_T7_HH_HDV." in trimmed_sample:
            stats_collection[raw_sample_name].append(("HDV",
                                                      reads_number,
                                                      neg_control_reads_number,
                                                      reads_number_50, len(unique_reads_ins_50),
                                                      reads_number_51, len(unique_reads_ins_51)))
        elif "_trimmed." in trimmed_sample:
            stats_collection[raw_sample_name].append(("illumina", reads_number, neg_control_reads_number))

    with open(path_to_output, 'w') as output_handler:
        header = ["stat"]

        sample_names = list(stats_collection.keys())
        sample_names.sort()
        header.extend(sample_names)
        header = ",".join(header)

        output_handler.write(f"{header}\n")

        grouped_stats = defaultdict(list)
        stats_order = ["Total reads number", "Reads number after Illumina adapter trim",
                       "Reads number after Illumina adapter and T7 trim",
                       "Reads number after Illumina adapter; T7 and HH trim",
                       "Reads number after Illumina adapter; T7; HH and HDV trim",
                       "Reads number with tRNAArg insertion",
                       "Reads number tRNAIle (50-insertion)",
                       "Unique reads number tRNAIle (50-insertion)",
                       "Reads number tRNAIle (51-insertion)",
                       "Unique reads number tRNAIle (51-insertion)"]

        for sample_name in sample_names:
            stats_per_sample = stats_collection[sample_name]
            stats_per_sample.sort()

            total_reads_number = stats_per_sample[-1][1]

            for stats in stats_per_sample:
                if stats[0] == "raw_reads":
                    grouped_stats["Total reads number"].append(str(stats[1]))

                elif stats[0] == "illumina":
                    grouped_stats["Reads number after " \
                                  "Illumina adapter trim"].append(f"{str(stats[1])}"
                                                                  f" ({str(int(round(stats[1]/total_reads_number, 2)*100))}%)")

                elif stats[0] == "T7":
                    grouped_stats["Reads number after " \
                                  "Illumina adapter and T7 trim"].append(f"{str(stats[1])}"
                                                                         f" ({str(int(round(stats[1]/total_reads_number, 2)*100))}%)")

                elif stats[0] == "HH":
                    grouped_stats["Reads number after " \
                                  "Illumina adapter; T7 and " \
                                  "HH trim"].append(f"{stats[1]}"
                                                    f" ({str(int(round(stats[1]/total_reads_number, 2)*100))}%)")
                elif stats[0] == "HDV":
                    grouped_stats["Reads number after " \
                                  "Illumina adapter; T7; " \
                                  "HH and HDV trim"].append(f"{stats[1]}"
                                                            f" ({str(int(round(stats[1]/total_reads_number, 2)*100))}%)")

                    grouped_stats["Reads number with " \
                                  "tRNAArg insertion"].append(f"{stats[2]}"
                                                              f" ({str(int(round(stats[2]/total_reads_number, 2)*100))}%)")
                    grouped_stats["Reads number tRNAIle " \
                                  "(50-insertion)"].append(f"{stats[3]}"
                                                           f" ({str(int(round(stats[3]/total_reads_number, 2)*100))}%)")
                    grouped_stats["Unique reads number " \
                                  "tRNAIle (50-insertion)"].append(f"{stats[4]}"
                                                                   f" ({str(int(round(stats[4]/total_reads_number, 2)*100))}%)")
                    grouped_stats["Reads number tRNAIle " \
                                  "(51-insertion)"].append(f"{stats[5]}"
                                                           f" ({str(int(round(stats[5]/total_reads_number, 2)*100))}%)")
                    grouped_stats["Unique reads number " \
                                  "tRNAIle (51-insertion)"].append(f"{stats[6]}"
                                                                   f" ({str(int(round(stats[6]/total_reads_number, 2)*100))}%)")

        for collected_stats in stats_order:
            new_line = [collected_stats]
            new_line.extend(grouped_stats[collected_stats])

            new_line = ",".join(new_line)

            output_handler.write(f"{new_line}\n")

    print("done")