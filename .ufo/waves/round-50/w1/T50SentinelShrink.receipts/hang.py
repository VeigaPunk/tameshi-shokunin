import subprocess, sys, time
child = ('import os, subprocess, sys\n'
         'p = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])\n'
         'print("child exiting", flush=True)\n')
t0 = time.monotonic()
try:
    subprocess.run([sys.executable, '-c', child], capture_output=True, timeout=2)
    print('returned', time.monotonic() - t0)
except subprocess.TimeoutExpired:
    print('TimeoutExpired after %.1fs' % (time.monotonic() - t0))
