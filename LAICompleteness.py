import argparse
import sys

from pathlib import Path

#from src.LTR_retriever import

def parse_arguments():
    description = "Module to assess the completeness of the genome assembly in term of LTR elements (LTR Assembly Index, LAI)"
    parser = argparse.ArgumentParser(description=description)

    #inputs
    help_fasta = "(Required) Specify the genome sequence file (FASTA)"
    parser.add_argument("--fasta", "-f", type=str, 
                        help=help_fasta, required=True)
    
    help_gff = "(Required) "
    parser.add_argument("--gff", "-g", type=str,
                        help=help_gff)

    #help_inharvest = ###

    #help_infinder = ###

    #help_output = ###

    if len(sys.argv)==1:
        parser.print_help()
        exit()
    return parser.parse_args()


def get_arguments():
    parser = parse_arguments()
    return {"fasta": Path(parser.fasta),
            "gff": Path(parser.gff),
            } 
            ###


def main():
    arguments = get_arguments() 
    print(arguments)
    suffixerator = run_suffixerator(arguments)
    print(suffixerator)
    #if resuls_harvester["returncode"] != 1 and resuls_finder


if __name__ == "__main__":
    main()