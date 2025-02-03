import subprocess

def run_suffixerator(arguments):
    #output dir?
    command = "gt suffixerator -db {} -indexname {} -tis -suf -lcp -des -ssp -sds -dna".format(arguments["fasta"],
                                                                                                arguments["gff"])

    print(command)
