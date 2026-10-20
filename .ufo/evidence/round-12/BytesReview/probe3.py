# P8: sequential read of both pipes deadlocks; bounded by an alarm so it cannot hang.
import subprocess, signal, sys
big = "python3 -c \"import sys; sys.stdout.buffer.write(b'o'*400000); sys.stderr.buffer.write(b'e'*400000)\""
def handler(*a): raise TimeoutError
signal.signal(signal.SIGALRM, handler); signal.alarm(8)
p = subprocess.Popen(["/bin/sh","-c",big], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL)
try:
    out = p.stdout.read(); err = p.stderr.read(); p.wait(); print("P8 sequential read completed", len(out), len(err))
except TimeoutError:
    print("P8 sequential read: DEADLOCK within 8s -> must use communicate() or temp files")
finally:
    signal.alarm(0); p.kill(); p.wait()
