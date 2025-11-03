# Script purpose is to collect results of RNAfold (MFE) and prepare for visualisation

import argparse
import os
from glob import glob

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='Path to RNAfold folding output', required=True)
    parser.add_argument('-o', '--output', type=str, help='Path to collected MFE', required=True)

    args = parser.parse_args()

    path_to_rnafold_collected = args.input
    path_to_rnafold_results = args.output


    with open(path_to_rnafold_results, 'w') as output:
        header = "\t".join([
            "read_id", "sequence", "mfe_struc", "mfe_en",
            "centroid_struc", "centroid_en",
            "mea_struc", "mea_en", "mea_dist",
            "mfe_in_ensemble", "ensemble_diversity"
        ])
        output.write(f"{header}\n")

        with open(path_to_rnafold_collected, 'r') as file_handler:
            # parce output file
            for line in file_handler:
                seq_name = line.strip()[1::]
                sequence = next(file_handler).strip()
                mfe = next(file_handler).strip()
                centriod = next(file_handler).strip()
                mea = next(file_handler).strip()
                ensemble = next(file_handler).strip()

                new_line = [seq_name, sequence]
                mfe_structure = mfe.split(" ")[0]
                if len(mfe.split(" ")) == 2:
                    mfe_en = mfe.split(" ")[1][1:-1]
                else:
                    mfe_en = mfe.split(" ")[2][:-1]
                new_line.extend([mfe_structure, mfe_en])

                centriod_structure = centriod.split(" ")[0]
                if len(centriod.split(" ")) == 2:
                    centriod_en = centriod.split(" ")[1][1:-1]
                else:
                    centriod_en = centriod.split(" ")[2][:-1]
                new_line.extend([centriod_structure, centriod_en])

                mea_structure = mea.split(" ")[0]
                if len(mea.split(" ")) == 3:
                    mea_en = mea.split(" ")[1][1:]
                    mea_dist = mea.split(" ")[2][:-1]
                else:
                    mea_en = mea.split(" ")[2]
                    mea_dist = mea.split(" ")[3][2:-1]
                new_line.extend([mea_structure, mea_en, mea_dist])

                ensemble_freq = ensemble.split(" ")[6][:-1]
                ensemble_div = ensemble.split(" ")[-1]
                new_line.extend([ensemble_freq, ensemble_div])

                new_line = "\t".join(new_line)
                output.write(f"{new_line}\n")

    # check for additional files
    folder_to_check = path_to_rnafold_collected.split("/")[:-1]
    folder_to_check = "/".join(folder_to_check) + "/*"

    files_in_folder = glob(folder_to_check)

    for one_file in files_in_folder:
        if ("_dp.ps" in one_file) or ("_ss.ps" in one_file):
            # remove file
            os.remove(one_file)
