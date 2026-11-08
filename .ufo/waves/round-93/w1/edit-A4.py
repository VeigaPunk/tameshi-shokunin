import sys
p=sys.argv[1]
open(p,"a").write("""
| id | note |
|---|---|
| C01 | `x\\|y` pipe in code |
""")
