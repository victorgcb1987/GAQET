import argparse
import sys

from csv import DictReader
from pathlib import Path

from src.agat import run_agat
from src.busco import run_busco
import src.LTR_retriever as LTR
from src.stringtie import run_stringtie, run_gffcompare, calculate_annotation_scores


#Function to create arguments and help
def parse_arguments():
    description = 'Tool with four modules to summarise the metrics and evaluate the quality of a genome annotation'
    parser = argparse.ArgumentParser(description=description)

    help_input = "(Required) Input File of Files"
    parser.add_argument("--input", "-i", type=str,
                        help=help_input, required=True)
    
    help_threads = "(Optional) Threads to use"
    parser.add_argument("--threads", "-t", type=int,
                        help=help_threads, default=1)

    help_output = "(Required) Output path"
    parser.add_argument("--output_dir", "-o", type=str,
                        help=help_output, required=True)
    
    if len(sys.argv)==1:
        parser.print_help()
        exit()
    return parser.parse_args()

#Function to compile de arguments into a dictionary
def get_arguments():
    parser = parse_arguments()
    fof_fpath = Path(parser.input)
    if not fof_fpath.exists():
        raise RuntimeError("Fof does not exist")
    else:
        samples = {}
        with open(fof_fpath) as fof_fhand:
            samples = {line["name"]: line for line in DictReader(fof_fhand, delimiter="\t")}
                       
    return {"input": samples,
            "threads": parser.threads,
            "output": Path(parser.output)}


def main():
    arguments = get_arguments()
    out_dir =  arguments["output"]
    if not out_dir.exists():
        out_dir.mkdir(parents=True, exist_ok=True)
    stats = {}                                          #diccionario para guardar los resultados de cada modulo por cada especie
    for name, values in arguments["input"].items():     #aqui no se deberia abrir samples????
        stats[name] = {}
        name_dir = out_dir/name
        values["output"] = name_dir
        if not name_dir.exists():
            name_dir.mkdir(parents=True, exist_ok=True)

        agat_statistics = run_agat(values)
        stats[name]["agat_statistics"] = agat_statistics

        busco_results = run_busco(values)
        stats[name]["busco_results"] = busco_results

        outdir =  LTR.create_outdir(values)
        suffixerator =  LTR.run_suffixerator(values)
        if "returncode" in suffixerator:
            if suffixerator["returncode"] == 1:
                raise RuntimeError("Suffixerator has failed")
        harvest = LTR.run_harvest(values)
        finder = LTR.run_finder(values)
        cat = LTR.concatenate_outputs(values)
        LTR = LTR.run_LTR_retriever(values)
        LAI = LTR.LTRrun_LAI(values)
        stats[name]["LAI"] = LAI

        stringtie = run_stringtie(values)
        gffcompare = run_gffcompare(values)
        annotation_scores = calculate_annotation_scores(values)
        stats[name]["annotation_scores"] = annotation_scores



if __name__ == "__main__":
    main()