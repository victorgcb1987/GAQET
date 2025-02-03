import subprocess

def run_suffixerator(arguments):
    #output dir
    out = arguments["output"]
    #suffixerator command
    cmd1 = "gt suffixerator -db {} -indexname {} -tis -suf -lcp -des -ssp -sds -dna".format(arguments["fasta"],
                                                                                                arguments["fasta"])
    #run suffixerator
    run1 = subprocess.run(cmd1, shell=True, stderr=subprocess.PIPE)

    return{"command":cmd1, "retruncode":run1.returncode}

def run_harvest(arguments):
    #harvest command
    cmd2 = "gt ltrharvest -index {} -minlenltr 100 -maxlenltr 7000 -mintsd 4 -maxtsd 6 -motif TGCA -motifmis 1 -similar 85 -vic 10 -seed 20 -seqids yes > genome.fa.harvest.scn".format(arguments["fasta"])
    #run harvest
    run2 = subprocess.run(cmd2, shell=True,stderr=subprocess.PIPE)

    return{"command":cmd2, "retruncode":run2.returncode}

def run_finder(arguments):
    #finder command
    cmd3 = "LTR_FINDER_parallel -seq {} -threads {} -harvest_out -size 1000000 -time 300".format(arguments["fasta"],
                                                                                                arguments["threads"])
    #run finder
    run3 = subprocess.run(cmd3, shell=True, stderr=subprocess.PIPE)

    return{"command":cmd3, "returncode":run3.returncode}