import argparse, subprocess, sys
a = argparse.ArgumentParser()
a.add_argument('--repo', required=True); a.add_argument('--trusted', required=True)
a.add_argument('--candidate', required=True); a.add_argument('--path', required=True)
args = a.parse_args()
def git(*argv):
    return subprocess.run(['git','-C',args.repo,*argv],capture_output=True,text=True)
rc = git('rev-parse','--verify',args.candidate+'^{commit}')
if rc.returncode:
    print('EXECUTOR_SOURCE_UNAVAILABLE'); sys.exit(2)
def entry(rev):
    r = git('ls-tree',rev,'--',args.path)
    if r.returncode or not r.stdout.strip():
        return None
    mode, typ, oid = r.stdout.split()[0:3]
    return (mode, typ, oid)
t = entry(args.trusted); c = entry(args.candidate)
if t is None or t[1] != 'blob':
    print('EXECUTOR_SOURCE_UNAVAILABLE'); sys.exit(2)
if c is None or c[1] != 'blob' or t != c:
    print('EXECUTOR_SOURCE_DRIFT'); sys.exit(1)
print('EXECUTOR_SOURCE_BOUND'); sys.exit(0)
