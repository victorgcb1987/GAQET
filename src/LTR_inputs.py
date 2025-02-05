import subprocess

def run_suffixerator(arguments):
    #creating output dir: output path + dir /w fasta file name
    index = arguments["output"] / arguments["fasta"].name
    #suffixerator command
    cmd = "gt suffixerator -db {} -indexname {} -tis -suf -lcp -des -ssp -sds -dna".format(arguments["fasta"], index)
    #run suffixerator
    run = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)

    return{"command":cmd, "returncode":run.returncode}

def run_harvest(arguments):
    #taking suffixerator output dir to use it as input
    index = arguments["output"] / arguments["fasta"].name
    #creating output: output path + file .harvest.scn /w fasta file name
    out = arguments["output"] / "{}.harvest.scn".format(arguments["fasta"].name)
    #harvest command
    cmd = "gt ltrharvest -index {} -minlenltr 100 -maxlenltr 7000 -mintsd 4 -maxtsd 6 -motif TGCA -motifmis 1 -similar 85 -vic 10 -seed 20 -seqids yes > {}".format(index, out)
    #run harvest
    run = subprocess.run(cmd, shell=True,stderr=subprocess.PIPE)

    return{"command":cmd, "returncode":run.returncode}

def run_finder(arguments):
    #finder command
    cmd = "LTR_FINDER_parallel -seq {} -threads {} -harvest_out -size 1000000 -time 300 -o {}".format(arguments["fasta"],
                                                                                                arguments["threads"],
                                                                                                arguments["output"])
    #run finder
    run = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)

    return{"command":cmd, "returncode":run.returncode}