"""
Airy admin script
"""
import sys
import os
import shutil

def execute():

    if len(sys.argv) <= 1:
        print "No command supplied."
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == 'help':
        help()

    elif command == 'startproject':
        startproject(*args)

    else:
        print "Error: unknown command '%s'" % command

def help():
    print 'Usage: python %s <command>' % sys.argv[0]

def startproject(project_name):
    print os.path.abspath(os.path.dirname(__file__))

