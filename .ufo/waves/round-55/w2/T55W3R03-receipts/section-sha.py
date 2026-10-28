import importlib.util, hashlib, subprocess, sys, json
REV = "9cf0146b94ddba12d454ebf7288ce6e5c5d535bb"
HEAD = "## Live-tree re-pin and entry-command monitor \u2014 round 17"
spec = importlib.util.spec_from_file_location("m18", ".ufo/evidence/round-18/measure.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
raw = subprocess.run(["git", "show", REV + ":SKILL.md"], capture_output=True, check=True).stdout
secs = mod.sectionize(raw)
hits = [s for s in secs if s["heading"] == HEAD]
assert len(hits) == 1, len(hits)
h = hits[0]
print(json.dumps({"start": h["start"], "end": h["end"], "heading": h["heading"],
                  "sha256": h["sha256"]}, ensure_ascii=False))
