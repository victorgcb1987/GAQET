import subprocess


def run_busco(arguments):
    #Creating output dir
    outdir = arguments["output"] / "BUSCOCompleteness" / "RunBusco_{}".format(arguments["lineage"])
    if not outdir.exists()
        outdir.mkdir(parents=True, exist_ok=True)
    #Command to run BUSCO
    cmd = "busco -i {} -c {} -l {} -m {} -o {}".format(arguments["input_file"],
                                                           arguments["threads"],
                                                           arguments["lineage"],
                                                           arguments["mode"],
                                                           outdir)
    #Check if BUSCO is already done
    if outdir.exists():
        #Show a message if it is
        return {"command": cmd, "msg": "BUSCO already done",
                "out_fpath": outdir}
    #But if is not done
    else:
        #Run BUSCO with command
        run_ = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
        #Is process has gone well
        if run_.returncode == 0:
            msg = "BUSCO run succesfully"
        #But if not
        else:
            msg = "BUSCO Failed: \n {}".format(run_.stderr)
        #Return command, final message and output dir path
        return {"command": cmd, "msg": msg,
                "out_fpath": outdir, "returncode": run_.returncode}