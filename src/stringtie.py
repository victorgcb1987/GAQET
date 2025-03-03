import subprocess

def run_stringtie(arguments):
    outdir = arguments["output"] / "RNASeqCheck"
    if not outdir.exists()
        outdir.mkdir(parents=True, exist_ok=True)
    output_name = outdir / arguments["alignments"].name
    cmd = "stringtie -o {}.gtf -p {} {}".format(output_name,
                                                arguments["threads"],
                                                arguments["alignments"])

    outfile = arguments["output"] / "{}.gtf".format(arguments["alignments"].name)
    if outfile.exists():
        return {"command": cmd, "msg": "stringtie already done",
                "out_fpath": outdir}
    else:
        run_ = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
        if run_.returncode == 0:
            msg = "stringtie ran successfully"
        else:
            msg = "stringtie Failed: \n {}".format(run_.stderr)
        return {"command": cmd, "msg": msg,
                "out_fpath": outdir, "returncode": run_.returncode}



def run_gffcompare(arguments):
    outdir = arguments["output"] / "RNASeqCheck"
    gtffile = outdir / "{}.gtf".format(arguments["alignments"].stem)
    output_name = outdir / arguments["alignments"].stem
    cmd = "gffcompare -r {} {} -o {}.stats".format(arguments["reference_annotation"],
                                            gtffile,
                                            output_name)
    
    outfile = arguments["output"] / "{}.stats".format(arguments["alignments"].name)
    if outfile.exists():
        return {"command": cmd, "msg": "gffcompare already done",
                "out_fpath": outdir}
    else:
        run_ = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE)
        if run_.returncode == 0:
            msg = "gffcompare ran successfully"
        else:
            msg = "gffcompare Failed: \n {}".format(run_.stderr)
        return {"command": cmd, "msg": msg,
                "out_fpath": outdir, "returncode": run_.returncode}



def calculate_annotation_scores(arguments):
    statsfile = arguments["output"] / "RNASeqCheck"/ "{}.stats".format(arguments["alignments"].name)
    annotation_scores = {}
    f1_checks = ["Transcript level:", "Locus level:"]
    number_check = ["Matching transcripts:", "Matching loci:"]
    f1_scores = {}
    with open(statsfile) as stats_fhand:
        for line in stats_fhand:
            for check in f1_checks:
                if check in line:
                    line = line.strip()
                    line = line.split()
                    sensivity = float(line[2])
                    precision = float(line[4])
                    f1_calc = 2*(sensitivity*precision)/(sensitivity+precision)
                    f1_scores[check.split()+"_f1"] = f1_calc
            for check in number_check:
                line = line.strip()
                line = line.split()
                matching_number = line[-1]
                f1_scores[check] = matching_number
    return f1_scores