import subprocess

def run_stringtie(arguments):
    outdir = arguments["output"]
    output_name = outdir / arguments["bam"].name
    cmd = "stringtie -o {}.gtf -p {} {}".format(output_name,
                                                arguments["threads"],
                                                arguments["bam"])

    outfile = arguments["output"] / "{}.gtf".format(arguments["bam"].name)
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
    gtffile = arguments["output"] / "{}.gtf".format(arguments["bam"].name)
    outdir = arguments["output"]
    output_name = outdir / arguments["bam"].name
    cmd = "gffcompare -r {} {} -o {}".format(arguments["gff"],
                                            gtffile,
                                            output_name)
    
    outfile = arguments["output"] / "{}.stats".format(arguments["bam"].name)
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
    statsfile = arguments["output"] / "{}.stats".format(arguments["bam"].name)
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