import sys
p=sys.argv[1]
open(p,"a").write("""
| id | outcome |
|---|---|
| **C01** | killed |
| **C02** | survived |
""")
