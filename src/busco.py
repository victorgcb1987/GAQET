import subprocess

def run_busco(arguments):
    #Creating output dir
    output_dir = arguments["output"] / "RunBusco_{}".format(arguments["lineage"])
    command = "busco -i {} -c {} -l {} -m {} -o {}".format(arguments["input_file"],
                                                           arguments["threads"],
                                                           arguments["lineage"],
                                                           arguments["mode"],
                                                           output_dir)
    if output_dir.exists():
        return {"command": command, "msg": "BUSCO already done",
                "out_fpath": output_dir}
    else:
        run_ = subprocess.run(command, shell=True, stderr=subprocess.PIPE)
        if run_.returncode == 0:
            msg = "BUSCO run succesfully"
        else:
            msg = "BUSCO Failed: \n {}".format(run_.stderr)
        return {"command": command, "msg": msg,
                "out_fpath": output_dir}


    
