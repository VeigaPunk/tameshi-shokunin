import os, signal, subprocess, sys
S = '/fast/scratch/hyaku/tameshi-r50/T50SentinelShrink'
rev, mode, work, secs = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
log = open(work + '.stdout', 'w')
p = subprocess.Popen([sys.executable, '-u', S + '/harness/drive.py', rev, mode, work],
                     stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
try:
    print('driver rc=%r after <=%.0fs' % (p.wait(timeout=secs), secs))
except subprocess.TimeoutExpired:
    os.killpg(os.getpgid(p.pid), signal.SIGKILL)
    print('driver STILL RUNNING after %.0fs -> killed (counter has no read timeout)' % secs)
