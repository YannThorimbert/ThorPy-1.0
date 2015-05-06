from shutil import copytree
import time
import zipfile
import os


def ignore(src, names):
    ignored_names = []
    src = src.replace("\\", "/") + "/"
    for name in names:
        if not name.endswith(".py"):
            if os.path.isfile(src + name):
                ignored_names.append(name)
    return ignored_names


def ignore_pyc(src, names):
    return [name for name in names if name.endswith(".pyc")]


def get_target(target):
    tstr = time.strftime("%d_%m_%Y_%Hh%Mm%Ss")
    str_date = source + "_" + tstr
    return str_date + target


def copy(src, target=None, ignore=ignore, compress=False):
    target = get_target(target)
    copytree(src, target, ignore=ignore)
    print(src + " copied as " + target)
    if compress:
        zipf = zipfile.ZipFile(target + ".zip", 'w')
        zipdir(target, zipf)
        zipf.close()

def zipdir(path, zipfile):
    for root, dirs, files in os.walk(path):
        for f in files:
            zipfile.write(os.path.join(root, f))

def file_len(fname):
    return sum(1 for line in open(fname))

def print_stats(path):
    tot_lines = 0
    tot_files = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            tot_files += 1
            tot_lines += file_len(root+os.sep+f)
    print("Number of files: ", tot_files)
    print("Number of lines: ", tot_lines)


source = "C:/Python34/Lib/site-packages/thorpy"
comment = "_1_0_clean"
compress = False

copy(source, target=comment, ignore=ignore_pyc, compress=compress)

##print_stats(source)