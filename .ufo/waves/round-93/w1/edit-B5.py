import sys
p=sys.argv[1]
rows=open("/fast/scratch/hyaku/tameshi-r93/R93C1/flip_rows.txt").read().strip().splitlines()
tr="".join("<tr><td>%s</td><td>%s</td></tr>"%(r.split()[0],r.split()[1]) for r in rows)
open(p,"a").write("\n<table><tr><th>id</th><th>verdict</th></tr>%s</table>\n" % tr)
