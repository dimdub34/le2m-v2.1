#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess


def run(args):
    try:
        nombre_clients = int(args[1])
    except ValueError:
        print(u"You must enter an integer that corresponds to the number of "
              u"remotes you want to start")
        sys.exit(1)
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    cmd = ["python", "clientrun.py"]
    cmd.extend(sys.argv[2:])
    for i in range(nombre_clients):
        subprocess.Popen(cmd)


if __name__ == "__main__":
    run(sys.argv)
