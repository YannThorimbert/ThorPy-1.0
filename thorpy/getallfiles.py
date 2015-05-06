import os
from fnmatch import fnmatch


def get_all_files(root="./", pattern="*.py"):
    all_files = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                fname = os.path.normpath(os.path.join(path, name))
                all_files.append(fname)
    return all_files


def get_all_files_beginning_with(beg, root="./", pattern="*.py"):
    all_files = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                fname = os.path.normpath(os.path.join(path, name))
                if name.startswith(beg):
                    all_files.append(fname)
    return all_files