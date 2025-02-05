import subprocess

def run_suffixerator(arguments):
    #creating output dir: output path + dir /w fasta file name
    index = arguments["output"] / arguments["fasta"].name
    #suffixerator command
    cmd = "gt suffixerator -db {} -indexname {} -tis -suf -lcp -des -ssp -sds -dna".format(arguments["fasta"], index)

    #Check if suffixerator is already done
    if "{}.md5".format(arguments["fasta"].name) in index:
        #Show a message if it is
        return {"command": cmd, "msg": "suffixerator already done",
                "out_fpath": index}
    #But if is not done
    else:
        #Run suffixerator
        run_ = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
        #Is process has gone well
        if run_.returncode == 0:
            msg = "suffixerator run succesfully"
        #But if not
        else:
            msg = "suffixerator Failed: \n {}".format(run_.stderr)
        #Return command, final message and output dir path
        return {"command": cmd, "msg": msg,
                "out_fpath": index, "returncode": run_.returncode}


def run_harvest(arguments):
    #taking suffixerator output dir to use it as input
    index = arguments["output"] / arguments["fasta"].name
    #creating output: output path + file .harvest.scn /w fasta file name
    out = arguments["output"] / "{}.harvest.scn".format(arguments["fasta"].name)
    #harvest command
    cmd = "gt ltrharvest -index {} -minlenltr 100 -maxlenltr 7000 -mintsd 4 -maxtsd 6 -motif TGCA -motifmis 1 -similar 85 -vic 10 -seed 20 -seqids yes > {}".format(index, out)

    #Check if HARVEST is already done
    if out.exists():
        #Show a message if it is
        return {"command": cmd, "msg": "harvest already done",
                "out_fpath": out}
    #But if is not done
    else:
        #Run harvest
        run_ = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
        #Is process has gone well
        if run_.returncode == 0:
            msg = "harvest run succesfully"
        #But if not
        else:
            msg = "harvest Failed: \n {}".format(run_.stderr)
        #Return command, final message and output dir path
        return {"command": cmd, "msg": msg,
                "out_fpath": out, "returncode": run_.returncode}


def run_finder(arguments):
    #finder command
    cmd = "LTR_FINDER_parallel -seq {} -threads {} -harvest_out -size 1000000 -time 300 -o {}".format(arguments["fasta"],
                                                                                                arguments["threads"],
                                                                                                arguments["output"])

    #Check if FINDER is already done
    if "{}.finder.combine.scn".format(arguments["fasta"]) in arguments["output"]:
        #Show a message if it is
        return {"command": cmd, "msg": "harvest already done",
                "out_fpath": arguments["output"]}
    #But if is not done
    else:
        #Run harvest
        run_ = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
        #Is process has gone well
        if run_.returncode == 0:
            msg = "harvest run succesfully"
        #But if not
        else:
            msg = "harvest Failed: \n {}".format(run_.stderr)
        #Return command, final message and output dir path
        return {"command": cmd, "msg": msg,
                "out_fpath": arguments["output"], "returncode": run_.returncode}


#def run_catfiles(arguments):
