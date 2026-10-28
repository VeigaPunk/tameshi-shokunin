import os, pathlib, sys, time
root = pathlib.Path(sys.argv[1]); n = int(sys.argv[2])
end = pathlib.Path(sys.argv[3])
made = 0
while not end.exists():
    d = root / ('noise-%d' % made); d.mkdir(parents=True, exist_ok=True); made += 1
    time.sleep(0.01)
(root / 'COUNT').write_text(str(made))
