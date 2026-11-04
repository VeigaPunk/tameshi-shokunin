@defect git-listing-uses-head | Listing ignores the requested historical revision and reads HEAD instead
@old     out = self._git('ls-tree', '-r', '--name-only', rev, '--', path)
@new     out = self._git('ls-tree', '-r', '--name-only', 'HEAD', '--', path)
