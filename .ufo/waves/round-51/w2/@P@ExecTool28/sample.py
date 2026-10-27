import os
dest = os.path.join("tests", "expected.json")
os.replace(dest, "actual.json")
