#!/usr/bin/python

from os import path
import sys

PROJECT_ROOT = path.abspath(path.dirname(__file__))

# Airy run engine

def main():
    from airy.core import ve
    ve.check_ve(PROJECT_ROOT, sys.argv)
    from airy.core import manager
    manager.execute(PROJECT_ROOT, sys.argv)

if __name__ == "__main__":
    main()

