from __future__ import print_function
import sys
import fileinput
import getallfiles
from tempfile import mkstemp
from shutil import move
from os import remove, close


OKAY_BEFORE = ["", " ", ".", "=", "(", "[", "+", "-", "%", "/", "*"]
OKAY_AFTER = ["", " ", "\n", "[", "]", "(", ")", "#", ",", ":", "+", "-", "%", "/",
              "*", ".", "="]


def exact_replace(
        txt,
        src,
        target,
        okay_before=OKAY_BEFORE,
        okay_after=OKAY_AFTER):
    beg = 0
    indices = []
    L = len(src)
    count = 0
    while beg < len(txt):
        found = txt.find(src, beg)
        if found == 0 and "" in okay_before:
            if txt[L] in okay_after:
                indices.append(found)
        elif found > 0:
            if txt[found - 1] in okay_before:
                if found + L < len(txt):
                    if txt[found + L] in okay_after:
                        indices.append(found)
                elif "" in okay_after:
                    indices.append(found)
        else:
            break
        beg = found + L
    new_txt = ""
    beg = 0
    for i in indices:
        new_txt += txt[beg:i] + target
        beg = i + L
    new_txt += txt[beg:]
    return new_txt, len(indices)


def replace_in_all_files_simple(
        textsource,
        texttarget,
        root="./",
        pattern="*.py",
        exception="wordreplace.py"):
    """Doesn't care about exact match. Replace ANY pattern!!!!"""
    files = getallfiles.get_all_files(root, pattern)
    if exception in files:
        files.remove(exception)
    for filename in files:
        replace_in_file_simple(filename, textsource, texttarget)
# for line in fileinput.input(filename, inplace=True):
##            print(line.replace(textsource, texttarget), end='')


def replace_in_file_simple(filename, pattern, subst):
    for line in fileinput.input(filename, inplace=True):
        print(line.replace(pattern, subst), end='')


def replace_in_file(file_path, pattern, subst):
    # Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path, 'w')
    old_file = open(file_path)
    for line in old_file:
        new_line, count = exact_replace(line, pattern, subst)
        if count > 0:
            print(str(count) +
                  " word" +
                  "s" *
                  (count > 1) +
                  " replaced in file " +
                  file_path)
        new_file.write(new_line)
    # close temp file
    new_file.close()
    close(fh)
    old_file.close()
    # Remove original file
    remove(file_path)
    # Move new file
    move(abs_path, file_path)


def replace_in_all_files(pattern, subst, root="./", filepattern="*.py",
                         exception="wordreplace.py", replace_type="precise"):
    if replace_type == "precise":
        replace_function = replace_in_file
    elif replace_type == "simple":
        replace_function = replace_in_file_simple
    else:
        raise Exception("Replace type not recognized.")
    files = getallfiles.get_all_files(root, filepattern)
    if exception in files:
        files.remove(exception)
    for filename in files:
        replace_function(filename, pattern, subst)


def mega_replace(replacements, replace_type, root="./", filepattern="*.py",
                 exception="wordreplace.py"):
    print("mega replacing of " +  str(replacements), replace_type)
    for pattern in replacements:
        replace_in_all_files(pattern, replacements[pattern], root, filepattern,
                             exception, replace_type)

def set_private(word, method="precise"):
    print("set_private")
    mega_replace({word : "_"+word}, method)

##set_private("states", "precise")

##textsource = "PRESS_EVENT"
##texttarget = "EVENT_PRESS"
##replace_in_all_files(textsource, texttarget, "precise")

mega_replace({'h_center' : 'h_store'}, "precise")

# replacements = {"from elements" : "from thorpy.elements",
# "from alphabet" : "from thorpy.alphabet",
# "from graph" : "from thorpy.graph",
# "from menus" : "from thorpy.menus",
# "from miscgui" : "from thorpy.miscgui",
# "from painting": "from thorpy.painting",
# "from utils" : "from thorpy.utils"
# }
##mega_replace(replacements, "simple")
