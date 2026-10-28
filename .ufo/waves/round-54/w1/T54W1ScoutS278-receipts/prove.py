"""Re-open S278: fetch CPython 3.12.7 Lib/tempfile.py, check :163-165, and test the note."""
import hashlib
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

URL = "https://raw.githubusercontent.com/python/cpython/v3.12.7/Lib/tempfile.py"
HERE = Path(__file__).resolve().parent
SRC = HERE / "tempfile-v3.12.7.py"
NOTE = (
    "for envname in 'TMPDIR', 'TEMP', 'TMP': "
    "dirname = _os.getenv(envname); if dirname: dirlist.append(dirname)"
)


def fetch() -> bytes:
    req = urllib.request.Request(URL, headers={"User-Agent": "T54W1ScoutS278"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        status = getattr(resp, "status", None)
        body = resp.read()
    print("HTTP", status, "BYTES", len(body))
    SRC.write_bytes(body)
    return body


def main() -> int:
    data = fetch()
    print("SHA256", hashlib.sha256(data).hexdigest())
    print("NEWLINE_KIND", "CRLF" if b"\r\n" in data else "LF")
    lines = data.splitlines()
    print("NLINES", len(lines))
    print("PYTHON", sys.version.replace("\n", " "))
    print("--- LINES 156-181 ---")
    for n in range(156, 182):
        print(f"{n}|{lines[n - 1].decode()}")
    joined = (
        lines[162].decode().strip()
        + " "
        + lines[163].decode().strip()
        + "; "
        + lines[164].decode().strip()
    )
    print("NOTE_JOIN_MATCH", joined == NOTE)
    print("JOINED", joined)
    print("--- IF DIRNAME ---")
    for sample in (None, "", " ", "/tmp", "0"):
        print(repr(sample), "truth", bool(sample), "skipped", not bool(sample))

    work = HERE / "work"
    usable = work / "usable-temp"
    missing = work / "no-such-dir"
    usable.mkdir(parents=True, exist_ok=True)
    if missing.exists():
        raise SystemExit(f"refusing to use an existing path: {missing}")

    child = r"""
import importlib.util, sys
path, mode = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("tf3127", path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
for name in ("TMPDIR", "TEMP", "TMP"):
    val = m._os.getenv(name)
    print(f"getenv {name}={val!r} skipped={not bool(val)}")
dl = m._candidate_tempdir_list()
print("dirlist_head", dl[:6])
print("dirlist_len", len(dl))
print("empty_in_dirlist", "" in dl)
print("none_in_dirlist", None in dl)
if mode == "winner":
    print("winner", m._get_default_tempdir())
"""

    def run(env_updates, mode, label):
        env = os.environ.copy()
        for key in ("TMPDIR", "TEMP", "TMP"):
            env.pop(key, None)
        for key, val in env_updates.items():
            if val is None:
                env.pop(key, None)
            else:
                env[key] = val
        print(f"=== {label} mode={mode} env={env_updates!r} ===")
        proc = subprocess.run(
            [sys.executable, "-c", child, str(SRC), mode],
            env=env,
            capture_output=True,
            text=True,
        )
        print("rc", proc.returncode)
        sys.stdout.write(proc.stdout)
        if proc.returncode != 0:
            print("STDERR", proc.stderr)
            return proc.returncode
        return 0

    cases = [
        ({}, "list", "all three absent"),
        ({"TMPDIR": ""}, "list", "TMPDIR empty, TEMP/TMP absent"),
        ({"TMPDIR": "", "TEMP": "", "TMP": ""}, "list", "all three empty"),
        ({"TMPDIR": " "}, "list", "TMPDIR single space"),
        ({"TMPDIR": "", "TEMP": str(usable)}, "winner", "empty TMPDIR, usable TEMP"),
        ({"TMPDIR": "", "TEMP": str(missing)}, "winner", "empty TMPDIR, missing TEMP"),
        ({"TMPDIR": "", "TEMP": "", "TMP": ""}, "winner", "all empty, selector"),
        ({}, "winner", "all absent, selector"),
        ({"TMPDIR": str(usable)}, "winner", "usable TMPDIR"),
    ]
    rc = 0
    for env_updates, mode, label in cases:
        rc = run(env_updates, mode, label) or rc
    print("abspath_empty_eq_cwd", os.path.abspath("") == os.getcwd())
    print("join_empty", os.path.join("", "probe"))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
