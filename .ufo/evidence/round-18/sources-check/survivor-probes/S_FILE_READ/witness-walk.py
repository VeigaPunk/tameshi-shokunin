import hashlib, os, stat, sys
print('# witness manifest: the probe-suite.sh witness builder (its PYEOF block, extracted verbatim) run once into a scratch dir;')
print('# paths relative to each witness --self; names as Python bytes literals; content sha256 or the open() errno;')
print('# entries are stat/opened relative to their directory fd (os.fwalk), so the >PATH_MAX entry is listable')
for line in sys.stdin.read().splitlines():
    name, self_path, detail = (line.split('\t') + [''])[:3]
    s = os.fsencode(self_path)
    print('WITNESS %s --self-length=%d expected-detail=%s' % (name, len(s), detail or '-'))
    for dirpath, dirnames, filenames, dirfd in os.fwalk(s):
        dirnames.sort()
        for fn in sorted(filenames):
            p = os.path.join(dirpath, fn)
            st = os.lstat(fn, dir_fd=dirfd)
            try:
                fd = os.open(fn, os.O_RDONLY, dir_fd=dirfd)
                with open(fd, 'rb') as fh:
                    content = 'sha256=' + hashlib.sha256(fh.read()).hexdigest()
            except OSError as e:
                content = 'open-error=%s' % os.strerror(e.errno)
            print('  %r mode=%s size=%d abs-path-length=%d %s' % (os.path.relpath(p, s), oct(stat.S_IMODE(st.st_mode)), st.st_size, len(p), content))
print('PC_PATH_MAX(/tmp)=%d' % os.pathconf('/tmp', 'PC_PATH_MAX'))
