import sys
p=sys.argv[1]
rows=open("/fast/scratch/hyaku/tameshi-r93/R93C1/flip_rows.txt").read().strip().splitlines()
out=["", "| id | verdict  |", "|---|---|"]
for r in rows:
    i,v=r.split()
    out.append("| %s | %s |" % (i, v))
out.append("")
open(p,"a").write("\n".join(out)+"\n")
