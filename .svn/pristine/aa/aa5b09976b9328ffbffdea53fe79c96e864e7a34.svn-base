#! /usr/bin/env python
# coding: utf-8

"""
Run xgettext on all the python file in the directory
This command only works on linux
"""

import os
import argparse


scriptdir = os.path.realpath(os.path.dirname(__file__))
appdir = os.path.realpath(os.path.dirname(scriptdir))
le2mdir = os.path.join(appdir, "le2m")


def _scan(dirtoscan):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(dirtoscan):
        for f in filenames:
            if f.endswith(".py") and "__init__" not in f:
                files.append(os.path.join(dirpath, f))
    return files


def main(part="le2m", keyword="le2mtrans", lang="fr_FR"):
    global le2mdir
    if part == "le2m":
        dirtoscan = le2mdir
    else:
        dirtoscan = os.path.join(le2mdir, "parts", part)

    files = _scan(dirtoscan)

    os.chdir(dirtoscan)
    os.system("xgettext {} --keyword={} -p {}/locale/{}/LC_MESSAGES "
              "-d {}new".format(" ".join(files), keyword, dirtoscan, lang,
                                "le2m" if not part else part))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--part", action="store",
                        default="le2m",
                        help="The part from which to extract words")
    parser.add_argument("-k", "--keyword", action="store",
                        default="le2mtrans",
                        help="The keyword to search with xgettext")
    parser.add_argument("-l", "--lang", default="fr_FR",
                        help="The language")

    options = parser.parse_args()
    if options.part != "le2m":
        if options.keyword == "le2mtrans":
            parser.error("The keyword cannot be le2mtrans")
    print("Command line args: {}".format(options))

    main(options.part, options.keyword, options.lang)