import os
from fnmatch import fnmatch

root = './'
pattern = "*.pyc"

all_files = []

for path, subdirs, files in os.walk(root):
    for name in files:
        if fnmatch(name, pattern):
            all_files.append(os.path.join(path, name))

for f in all_files:
    os.remove(f)
print(" ".join((str(len(all_files)), pattern, "files removed.")))
