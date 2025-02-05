import argparse
import sys

from pathlib import Path

from src.LTR_inputs import create_outdir
from src.LTR_inputs import run_suffixerator
from src.LTR_inputs import run_harvest
from src.LTR_inputs import run_finder
#from src.LTR_retriever import

#parses command-line arguments
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

    #threads
    help_threads = "Number of threads to run the program"
    parser.add_argument("--threads", "-t", type=int,
                        help=help_threads, default=1)

    #output
    help_output = "(Required) Output path"
    parser.add_argument("--output", "-o", type=str,
                        help=help_output) #required=True

    if len(sys.argv)==1:
        parser.print_help()
        exit()
    return parser.parse_args()


#stores command-line arguments in a dictionary with proper data types
def get_arguments():
    parser = parse_arguments()
    return {"fasta": Path(parser.fasta),
            "gff": Path(parser.gff),
            "threads": parser.threads,
            "output": Path(parser.output)} 
            ###


#main function
def main():
    arguments = get_arguments()
    #function to create the output directory if this does not exist
    outdir = create_outdir(arguments)
    print(outdir)
    finder = run_finder(arguments)
    print(finder)
    suffixerator = run_suffixerator(arguments)
    print(suffixerator)
    harvest = run_harvest(arguments)
    print(harvest)

    #if resuls_harvester["returncode"] != 1 and resuls_finder


if __name__ == "__main__":
    main()