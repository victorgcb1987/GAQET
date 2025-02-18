import os
import subprocess
import shutil

from pathlib import Path


def create_outdir(arguments):
    #Output directory (to save LTR_retriever input and output files) path
    outdir = arguments["output"]
    outfile = outdir / arguments["fasta"].name
    #If outdir exists, show this message
    # if outdir.exists():
    #     msg = "The output directory {} exists".format(arguments["output"])
    #     if  outfile.exists():
    #         msg += " - Fasta file is already in the output directory"
    #     else:
    #         shutil.copyfile(arguments["fasta"], outfile)
    #         msg += " - Fasta file has been successfully copied to the output directory"
    # #Otherwise, create outdir and show this other message
    # else:
    #     outdir.mkdir(parents=True, exist_ok=True)
    #     shutil.copyfile(arguments["fasta"], outfile)
    #     msg = "The output directory {} has been successfully created - Fasta file has been successfully copied to the output directory".format(arguments["output"])
    # #Return the proper message
    if not outdir.exists():
        outdir.mkdir(parents=True)
    if not out_file.exists():
        cmd = f"ln -s {str(arguments["fasta"])} {str(out_file)}"
        cmd = run(shell=True)
    msg = "blao"

    return{msg}




def run_suffixerator(arguments):
    #output dir path + name for output files
    index = arguments["output"] / arguments["fasta"].name
    #suffixerator command
    cmd = "gt suffixerator -db {} -indexname {} -tis -suf -lcp -des -ssp -sds -dna".format(arguments["fasta"], index)

    #Check if suffixerator is already done
    md5 = arguments["output"] / "{}.md5".format(arguments["fasta"].name)
    if md5.exists():
        #Show a message if it is
        return {"command": cmd, "msg": "suffixerator already done",
                "out_fpath": index}
    #But if is not done
    else:
        #Run suffixerator
        run_ = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
        #If process has gone well, send this message
        if run_.returncode == 0:
            msg = "suffixerator ran successfully"
        #Otherwise, send this error message
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
    #Otherwise, send this error message
    else:
        #Run harvest
        run_ = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
        #If process has gone well, send this message
        if run_.returncode == 0:
            msg = "HARVEST ran successfully"
        #But if not
        else:
            msg = "HARVEST Failed: \n {}".format(run_.stderr)
        #Return command, final message and output dir path
        return {"command": cmd, "msg": msg,
                "out_fpath": out, "returncode": run_.returncode}




def run_finder(arguments):
    #finder command
    cwd = Path(os.getcwd())
    cmd = "LTR_FINDER_parallel -seq {} -threads {} -harvest_out -size 1000000 -time 300".format(arguments["fasta"],
                                                                                                arguments["threads"])

    #Check if FINDER is already done
    out_file = arguments["output"] / "{}.finder.combine.scn".format(arguments["fasta"].name)
    if out_file.exists():
        #Show a message if it is
        return {"command": cmd, "msg": "harvest already done",
                "out_fpath": arguments["output"]}
    #But if is not done
    else:
        #Change the working directory to the "output" path
        os.chdir(arguments["output"])
        #Run finder
        run_ = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
        #If process has gone well, send this message
        if run_.returncode == 0:
            msg = "FINDER ran successfully"
        #Otherwise, send this error message
        else:
            msg = " FINDER Failed: \n {}".format(run_.stderr)
        #Restore the original working directory
        os.chdir(cwd)
        #Return command, final message and output dir path
        return {"command": cmd, "msg": msg,
                "out_fpath": arguments["output"], "returncode": run_.returncode}




def concatenate_outputs(arguments):
    outpath = arguments["output"] / arguments["fasta"].name 
    cmd = "cat {}.harvest.scn {}.finder.combine.scn > {}.rawLTR.scn".format(outpath, 
                                                                            outpath, 
                                                                            outpath)

    #Check if "cat" is already done
    out_file = arguments["output"] / "{}.rawLTR.scn".format(arguments["fasta"].name)
    if out_file.exists():
        #Show a message if it is
        return {"command": cmd, "msg": "Concatenation of the output files from Harvest and Finder successfully completed.",
                "out_fpath": arguments["output"]}
    #But if is not done
    else:
        #Run command
        run_ = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
        #If process has gone well, send this message
        if run_.returncode == 0:
            msg = "Concatenation of the output files from Harvest and Finder successfully completed."
        #Otherwise, send this error message
        else:
            msg = "Failed: \n {}".format(run_.stderr)
        #Return command, final message and output dir path
        return {"command": cmd, "msg": msg,
                "out_fpath": arguments["output"], "returncode": run_.returncode}




def run_LTR_retriever(arguments):
    cwd = Path(os.getcwd())
    cmd = "LTR_retriever -genome {} -inharvest {}.rawLTR.scn -threads {}".format(arguments["fasta"].name,
                                                                                arguments["fasta"].name,
                                                                                arguments["threads"])
    outfile = arguments["output"] / "{}.out".format(arguments["fasta"].name)
    if outfile.exists():
        return {"command": cmd, "msg": "LTR_retriever already done",
                "out_fpath": arguments["output"]}
    else:
        os.chdir(arguments["output"])
        run_ = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
        if run_.returncode == 0:
            msg = "LTR_retriever ran successfully"
        else:
            msg = "LTR_retriever Failed: \n {}".format(run_.stderr)
        os.chdir(cwd)
        return {"command": cmd, "msg": msg,
                "out_fpath": arguments["output"], "returncode": run_.returncode}




def run_LAI(arguments):
    cwd = Path(os.getcwd())
    cmd = "LAI -genome {} -intact {}.pass.list -all {}.out".format(arguments["fasta"].name,
                                                                            arguments["fasta"].name,
                                                                            arguments["fasta"].name)
    outfile = arguments["output"] / "{}.LAI.LTR.ava.out".format(arguments["fasta"].name)
    if outfile.exists():
        return {"command": cmd, "msg": "LAI already done",
                "out_fpath": arguments["output"]}
    else:
        os.chdir(arguments["output"])
        run_ = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
        if run_.returncode == 0:
            msg = "LAI ran successfully"
        else:
            msg = "LAI Failed: \n {}".format(run_.stderr)
        os.chdir(cwd)
        return {"command": cmd, "msg": msg,
                "out_fpath": arguments["output"], "returncode": run_.returncode}