import subprocess

def run_agat(arguments):
    #Creating output dir
    outdir = arguments["output"] / "GenomeAnnStats"
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



def get_agat_stats(agat_statistics):
    results = {
        "Gene_Models (N)": 0,
        "Transcript_Models (N)": 0,
        "CDS_Models (N)": 0,
        "Exons (N)": 0,
        "UTR5' (N)": 0,
        "UTR3' (N)": 0,
        "Overlapping_Gene_Models (N)": 0,
        "Single Exon Gene Models (N)": 0,
        "Single Exon Transcripts (N)": 0,
        "Total Gene Space (Mb)": 0,
        "Mean Gene Model Length (bp)": 0,
        "Mean CDS Model Length (bp)": 0,
        "Mean Exon Length (bp)": 0,
        "Mean Intron Length (bp)": 0,
        "Longest Gene Model Length (bp)": 0,
        "Longest CDS Model Length (bp)": 0,
        "Longest Intron Length (bp)": 0,
        "Shortest Gene Model Length (bp)": 0,
        "Shortest CDS Model Length (bp)": 0,
        "Shortest Intron Length (bp)": 0
    }
    mapping = {
        "Number of gene": "Gene_Models (N)",
        "Number of mrna": "Transcript_Models (N)",
        "Number of cds": "CDS_Models (N)",
        "Number of exon": "Exons (N)",
        "Number of five_prime_utr": "UTR5' (N)",
        "Number of three_prime_utr": "UTR3' (N)",
        "Number gene overlapping": "Overlapping_Gene_Models (N)",
        "Number of single exon gene": "Single Exon Gene Models (N)",
        "Number of single exon mrna": "Single Exon Transcripts (N)",
        "Total gene length (bp)": "Total Gene Space (Mb)",
        "mean gene length (bp)": "Mean Gene Model Length (bp)",
        "mean cds length (bp)": "Mean CDS Model Length (bp)",
        "mean exon length (bp)": "Mean Exon Length (bp)",
        "mean intron in cds length (bp)": "Mean Intron Length (bp)",
        "Longest gene (bp)": "Longest Gene Model Length (bp)",
        "Longest cds (bp)": "Longest CDS Model Length (bp)",
        "Longest intron into cds part (bp)": "Longest Intron Length (bp)",
        "Shortest gene (bp)": "Shortest Gene Model Length (bp)",
        "Shortest cds piece (bp)": "Shortest CDS Model Length (bp)",
        "Shortest intron into cds part (bp)": "Shortest Intron Length (bp)"
    }
    with open(agat_statistics["out_fpath"], 'r') as stats_fhand:
        for line in stats_fhand:
            if not line.rstrip():
                continue
            if ':' in line:
                break
            try:
                key, val = line.rsplit(maxsplit=1)
                key = key.strip()
                val = int(val.strip())
                if key in mapping:
                    result_key = mapping[key]
                    if result_key == "Total Gene Space (Mb)":
                        results[result_key] = round(val / 1_000_000, 2)
                    else:
                        results[result_key] = val
            except ValueError:
                continue  # Skip lines that can't be parsed
    return results

#    return = "NG:1212112;NT:34345334"

#Gene_Models (N)	Transcript_Models (N)	CDS_Models (N)	Exons (N)	UTR5' (N)	UTR3' (N)	Overlapping_Gene_Models (N)	Single Exon Gene Models (N)	Single Exon Transcripts (N)	Total Gene Space (Mb)	Mean Gene Model Length (bp)	Mean CDS Model Length (bp)	Mean Exon Length (bp)	Mean Intron Length (bp)	Longest Gene Model Length (bp)	Longest CDS Model Length (bp)	Longest Intron Length (bp)	Shortest Gene Model Length (bp)	Shortest CDS Model Length (bp)	Shortest Intron Length (bp)