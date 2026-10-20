#!/usr/bin/env python3
# Evidence fixture (ExitReview round-12). Child that returns a fixed exit per invocation.
# argv: STATE_FILE EXIT_SEQ(comma list) MODE(same|stderr-diff)
# State file holds the invocation counter; a fresh state file is used per case.
import os
import sys

state, seq, mode = sys.argv[1], sys.argv[2], sys.argv[3]
n = int(open(state).read()) if os.path.exists(state) else 0
with open(state, "w") as f:
    f.write(str(n + 1))
codes = [int(x) for x in seq.split(",")]
sys.stdout.write("ok\n")
sys.stderr.write(f"err-{n}\n" if mode == "stderr-diff" else "ok\n")
sys.exit(codes[n])
