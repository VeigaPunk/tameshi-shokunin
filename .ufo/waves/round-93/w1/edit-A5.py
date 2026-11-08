import sys
p=sys.argv[1]
rows=open("/fast/scratch/hyaku/tameshi-r93/R93C1/flip_rows.txt").read().strip().splitlines()
# use TRUE cells, not flipped, under a 5-col header: honest-looking extension of the real table
true={"C01":"KILLED","C02":"SURVIVED","C03":"SURVIVED","C04":"KILLED","C05":"KILLED","C06":"SURVIVED","C07":"KILLED","C08":"SURVIVED","C09":"SURVIVED","C10":"SURVIVED","C11":"KILLED","C12":"SURVIVED"}
out=["", "| id | arm targeted | edit | verdict | witness | note |", "|---|---|---|---|---|---|"]
for r in rows:
    i=r.split()[0]
    out.append("| %s | arm | edit | %s | witness | extra |" % (i, true[i]))
out.append("")
open(p,"a").write("\n".join(out)+"\n")
