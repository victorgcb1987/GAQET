import subprocess

def run_busco(arguments):
    #Creating output dir
    output_dir = arguments["output"] / "RunBusco_{}".format(arguments["lineage"])
    #Command to run BUSCO
    command = "busco -i {} -c {} -l {} -m {} -o {}".format(arguments["input_file"],
                                                           arguments["threads"],
                                                           arguments["lineage"],
                                                           arguments["mode"],
                                                           output_dir)
    #Check if BUSCO is already done
    if output_dir.exists():
        #Show a message if it is
        return {"command": command, "msg": "BUSCO already done",
                "out_fpath": output_dir}
    #But if is not done
    else:
        #Run BUSCO with command
        run_ = subprocess.run(command, shell=True, stderr=subprocess.PIPE)
        #Is process has gone well
        if run_.returncode == 0:
            msg = "BUSCO run succesfully"
        #But if not
        else:
            msg = "BUSCO Failed: \n {}".format(run_.stderr)
        #Return command, final message and output dir path
        return {"command": command, "msg": msg,
                "out_fpath": output_dir}