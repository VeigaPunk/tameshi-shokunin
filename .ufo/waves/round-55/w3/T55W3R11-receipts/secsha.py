import hashlib, importlib.util, subprocess, sys
spec = importlib.util.spec_from_file_location("m18", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py")
m18 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m18)
rev = sys.argv[1]; repo = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
raw = subprocess.run(["git","-C",repo,"cat-file","blob",f"{rev}:SKILL.md"], capture_output=True, check=True).stdout
secs = m18.sectionize(raw)
for s in secs:
    if s["heading"].startswith("### Round-13 gate/probe registry"):
        print("HEADING:", s["heading"]); print("start", s["start"], "end", s["end"]); print("sha256", s["sha256"])
        body = "\n".join(raw.decode('utf-8','surrogateescape').split('\n')[s["start"]-1:s["end"]-1])
        print("---body-bytes---", len(body.encode('utf-8','surrogateescape')))
        print("first", repr(body.split("\n")[0])); print("last", repr(body.split("\n")[-1]))
print("total_sections", len(secs))
