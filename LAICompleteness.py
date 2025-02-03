import argparse
import sys

from pathlib import Path

from src.LTR_inputs import run_suffixerator
from src.LTR_inputs import run_harvest
from src.LTR_inputs import run_finder
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

    help_output = "(Required) Output path"
    parser.add_argument("--output", "-o", type=str,
                        help=help_output) #required=True

    if len(sys.argv)==1:
        parser.print_help()
        exit()
    return parser.parse_args()


def get_arguments():
    parser = parse_arguments()
    return {"fasta": Path(parser.fasta),
            "gff": Path(parser.gff),
            "output": Path(parser.output)} 
            ###


def main():
    arguments = get_arguments() 
    print(arguments)
    suffixerator = run_suffixerator(arguments)
    harvest = run_harvest(arguments)
    finder = run_finder(arguments)

    #if resuls_harvester["returncode"] != 1 and resuls_finder


if __name__ == "__main__":
    main()