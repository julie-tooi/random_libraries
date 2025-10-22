# Script purpose is to collect results of RNAplfold and prepare for visualisation
# can collect both open_en and probs results

from glob import glob
import argparse


def detect_base(position, sequence_name, sequence_collection):
    position_in_seq = int(position) - 1

    if sequence_name in sequence_collection:
        return sequence_collection[sequence_name][position_in_seq]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='Path to folder with folding results', required=True)
    parser.add_argument('-o', '--output', type=str, help='Path to output', required=True)
    parser.add_argument('-s', '--sample', type=str, help='Sample name', required=True)
    parser.add_argument('-f', '--fasta', type=str, help='Path to fasta file with target sequences', required=True)
    parser.add_argument('-t', '--type', type=str, help='Type of information (probabilities or open energies)',
                        choices=["prob", "en"], required=True)

    args = parser.parse_args()

    path_to_input = args.input
    path_to_output = args.output
    sample_name = args.sample
    path_to_fasta = args.fasta
    info_type = args.type

    target_collection = dict()

    with open(path_to_fasta, 'r') as fasta_handler:
        for line in fasta_handler:
            if ">" in line:
                read_name = line.strip()[1:]
                sequence = next(fasta_handler)

                target_collection[read_name] = sequence

    if info_type == "prob":

        batch = glob(f"{path_to_input}/*_lunp")

        with open(path_to_output, 'w') as output:
            output.write("sample,read_id,position,l1,l2,base\n")
            for file in batch:
                file_name = file.split("/")[-1].split("_lunp")[0].replace("_", ":")
                with open(file, 'r') as file_handler:
                    file_handler.readline()
                    file_handler.readline()

                    for line in file_handler:
                        line = line.strip().split("\t")
                        position = line[0]
                        l1, l2 = line[1], line[2]
                        base = detect_base(position, file_name, target_collection)

                        new_line = ",".join((sample_name, file_name,
                                             position, l1, l2, base))
                        output.write(new_line + "\n")

    elif info_type == "en":
        batch = glob(f"{path_to_input}/*_openen")

        with open(path_to_output, 'w') as output:
            output.write("sample,read_id,position,l1,l2,l3,l4,l5,base\n")
            for file in batch:
                file_name = file.split("/")[-1].split("_openen")[0].replace("_", ":")
                with open(file, 'r') as file_handler:
                    file_handler.readline()
                    file_handler.readline()

                    for line in file_handler:
                        line = line.strip().split("\t")
                        position = line[0]
                        l1, l2, l3, l4, l5 = line[1], line[2], line[3], line[4], line[5]

                        base = detect_base(position, file_name, target_collection)

                        new_line = ",".join((sample_name, file_name,
                                             position, l1, l2, l3, l4, l5, base))
                        output.write(new_line + "\n")

    print("done")
