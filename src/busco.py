import subprocess

def run_gffread(arguments):
    #gffread -y proteins.fasta -g ncbi_dataset/data/GCF_000001735.4/GCF_000001735.4_TAIR10.1_genomic.fna genomic_clean.gff
    outdir = arguments["output"] / "BUSCOCompleteness"
    out_file = out_dir / "{}.proteins.fasta".format(arguments["ref_assembly"].stem)
    cmd = "gffread -y {} -g {} {}".format(outfile, 
                                            arguments["ref_assembly"],
                                            arguments["annotation"])

    #Add input sequences file for BUSCO
    arguments["input"] = out_file
    if out_file.exists():
        #Show a message if it is
        return {"command": cmd, "msg": "Extract sequences already done",
                "out_fpath": out_file}
    #But if is not done
    else:
        #Run BUSCO with command
        run_ = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
        #Is process has gone well
        if run_.returncode == 0:
            msg = "GFFread run succesfully"
        #But if not
        else:
            msg = "GFFread Failed: \n {}".format(run_.stderr)
        #Return command, final message and output dir path
        return {"command": cmd, "msg": msg,
                "out_fpath": out_file, "returncode": run_.returncode}


def run_busco(arguments):
    #Creating output dir
    outdir = arguments["output"] / "BUSCOCompleteness"
    if not outdir.exists():
        outdir.mkdir(parents=True, exist_ok=True)
    #Command to run BUSCO
    cmd = "busco -i {} -c {} -o {}".format(arguments["input"],
                                                    arguments["threads"],
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