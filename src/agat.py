import subprocess

def run_agat(arguments):
    #Creating output dir
    outdir = arguments["output"] / "RunAgat" 
    outdir.mkdir(parents=True, exist_ok=True)
    out_fpath = outdir / "ResultAgat.txt"

    #Creating command to run AGAT as a list
    cmd = ["agat_sp_statistics.pl", "--gff", "{}".format(arguments["annotation"]), "-o", "{}".format(out_fpath)]

#Check if AGAT is already done
    if out_fpath.exists():
        #Show a message if it is
        return {"command": cmd, "msg": "AGAT already done",
                "out_fpath": out_fpath, "returncode": 99}
    #But if is not done
    else:
        #Run AGAT with command
        command = ' '.join(cmd)
        print(command)
        run_ = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        #Is process has gone well
        print(run_.returncode)
        if run_.returncode == 0:
            msg = "AGAT run successfully"
        #But if not
        else:
            msg = "AGAT Failed: \n {}".format(run_.stdout)
        #Return command, final message and output dir path
        return {"command": command, "msg": msg,
                "out_fpath": out_fpath}


#def get_agat_results(agat_results):
# def get_agat_statistics(agat_statistics):
#     with open(agat_statistics) as input:
#         for line in input:
#             if "%" in line:
#                 return line.strip()

#    return = "NG:1212112;NT:34345334"

#Gene_Models (N)	Transcript_Models (N)	CDS_Models (N)	Exons (N)	UTR5' (N)	UTR3' (N)	Overlapping_Gene_Models (N)	Single Exon Gene Models (N)	Single Exon Transcripts (N)	Total Gene Space (Mb)	Mean Gene Model Length (bp)	Mean CDS Model Length (bp)	Mean Exon Length (bp)	Mean Intron Length (bp)	Longest Gene Model Length (bp)	Longest CDS Model Length (bp)	Longest Intron Length (bp)	Shortest Gene Model Length (bp)	Shortest CDS Model Length (bp)	Shortest Intron Length (bp)