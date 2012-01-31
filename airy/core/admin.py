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

    elif command == 'startapp':
        startapp(*args)

    else:
        print "Error: unknown command '%s'" % command

def help():
    print 'Usage: python %s <command>' % sys.argv[0]
    print """
Available commands:

    startproject <project_name>:

        Creates a new project in a folder named <project_name>

    startapp <app_name>:

        Creates a new app in a folder named <app_name>

    help:

        Displays this help

"""

def startproject(project_name):
    admin_path = os.path.abspath(os.path.dirname(__file__))
    skeleton_path = os.path.join(admin_path, '../skeleton/project')
    shutil.copytree(skeleton_path, os.path.join(os.getcwd(), project_name))
    print "Created project '%s'." % project_name

def startapp(app_name):
    admin_path = os.path.abspath(os.path.dirname(__file__))
    skeleton_path = os.path.join(admin_path, '../skeleton/app')
    shutil.copytree(skeleton_path, os.path.join(os.getcwd(), app_name))
    print "Created app '%s'." % app_name



