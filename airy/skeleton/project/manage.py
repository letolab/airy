#!/usr/bin/python

from os import path

PROJECT_ROOT = path.abspath(path.dirname(__file__))

# Airy run engine

# test params
import sys
sys.path.append(path.join(PROJECT_ROOT, '../airy'))
# end test

def main():
    from airy.core import ve
    ve.check_ve(PROJECT_ROOT, sys.argv)
    from airy.core import manager
    manager.execute(PROJECT_ROOT, sys.argv)

if __name__ == "__main__":
    main()

