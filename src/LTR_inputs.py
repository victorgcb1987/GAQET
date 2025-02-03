import subprocess

def run_suffixerator(arguments):
    #output dir?
    #suffixerator command
    command = "gt suffixerator -db {} -indexname {} -tis -suf -lcp -des -ssp -sds -dna".format(arguments["fasta"],
                                                                                                arguments["gff"])

    print(command)

    #run suffixerator
    run_ = subprocess.run(command, shell=True, stderr=subprocess.PIPE)

    return{"command":command, "retruncode":run_.returncode}
