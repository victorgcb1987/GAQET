import subprocess

def run_agat(arguments):
    #Creating output dir
    output_dir = arguments["output"] / "RunAgat" 
    output_dir.mkdir(parents=True, exist_ok=True)
    out_fpath = output_dir / "ResultAgat.txt"

    #Creating command to run AGAT as a list
    cmd = ["agat_sp_statistics.pl", "-i", "{}".format(str(arguments["gff"])), "-o", "{}".format(out_fpath)]

    #Adding "distribution" to command if it has been selected
    if arguments["distribution"]:
        dist_arg = ["-d"]
        cmd += dist_arg
    #Adding "plot" to command if it has been selected
    if arguments["plot"]:
        plot_arg = ["-p"]
        cmd += plot_arg

    #Adding "genome size" to command if it has a different value than default
    if arguments["gs"] > 0:
        size_arg = ["-g {}".format(arguments["gs"])]
        cmd += size_arg

#Check if AGAT is already done
    if out_fpath.exists():
        #Show a message if it is
        return {"command": cmd, "msg": "AGAT already done",
                "out_fpath": out_fpath}
    #But if is not done
    else:
        #Run AGAT with command
        run_ = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
        #Is process has gone well
        if run_.returncode == 0:
            msg = "AGAT run succesfully"
        #But if not
        else:
            msg = "AGAT Failed: \n {}".format(run_.stderr)
        #Return command, final message and output dir path
        return {"command": cmd, "msg": msg,
                "out_fpath": out_fpath}
