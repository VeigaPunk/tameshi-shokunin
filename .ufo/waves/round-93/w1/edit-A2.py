import sys
p=sys.argv[1]
open(p,"a").write("""
| name | status | note |
|---|---|---|
| alpha | open | verdict |
| beta | shut | verdict |
""")
