import sys
p=sys.argv[1]
open(p,"a").write("""
| id | lane | effect |
|---|---|---|
| C01 | x-lane | nothing |
| C02 | y-lane | nothing |
| C12 | z-lane | nothing |
""")
