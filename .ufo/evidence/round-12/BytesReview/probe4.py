# P10-P12: argv NUL, file byte round-trip, text-mode readback. Stdlib only.
import subprocess, tempfile
try:
    subprocess.run(["/bin/echo", "a\0b"], stdin=subprocess.DEVNULL, capture_output=True); print("P10 NUL in argv: accepted")
except ValueError as e: print("P10 NUL in argv: ValueError:", e)
d = tempfile.mkdtemp(dir="/tmp/bytesreview")
data = b"a\r\n\0\xff\n"
with open(f"{d}/stdout.1", "wb") as f: f.write(data)
with open(f"{d}/stdout.1", "rb") as f: print("P11 rb roundtrip equal:", f.read() == data)
with open(f"{d}/stdout.1", "r", encoding="utf-8", errors="surrogateescape", newline=None) as f: t = f.read()
print("P12 text-mode readback differs:", t.encode("utf-8", "surrogateescape") != data)
