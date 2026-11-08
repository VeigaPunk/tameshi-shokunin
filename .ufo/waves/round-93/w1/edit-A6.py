import sys
p=sys.argv[1]
open(p,"a").write("""
| survivor | lanes hit | effect |
|---|---|---|
| | 20 | nothing |
| C12 | 20 | something |
""")
