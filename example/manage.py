#!/usr/bin/python

import sys
import shutil
import virtualenv
import subprocess
from os import path

PROJECT_ROOT = path.abspath(path.dirname(__file__))
REQUIREMENTS = path.join(PROJECT_ROOT, 'requirements.pip')

VE_ROOT = path.join(PROJECT_ROOT, '.ve')
VE_TIMESTAMP = path.join(VE_ROOT, 'timestamp')
VE_ACTIVATE = path.join(VE_ROOT, 'bin', 'activate_this.py')

envtime = path.exists(VE_ROOT) and path.getmtime(VE_ROOT) or 0
envreqs = path.exists(VE_TIMESTAMP) and path.getmtime(VE_TIMESTAMP) or 0
envspec = path.getmtime(REQUIREMENTS)

def go_to_ve():
    # going into ve
    if not VE_ROOT in sys.prefix:
        retcode = 3
        while retcode == 3:
            if sys.platform == 'win32':
                python = path.join(VE_ROOT, 'Scripts', 'python.exe')
            else:
                python = path.join(VE_ROOT, 'bin', 'python')
            try:
                retcode = subprocess.call([python, __file__] + sys.argv[1:])
            except KeyboardInterrupt:
                retcode = 1
        sys.exit(retcode)

update_ve = 'update_ve' in sys.argv
if update_ve or envtime < envspec or envreqs < envspec:
    if update_ve:
        # install ve
        if envtime < envspec:
            if path.exists(VE_ROOT):
                shutil.rmtree(VE_ROOT)
            virtualenv.logger = virtualenv.Logger(consumers=[])
            virtualenv.create_environment(VE_ROOT, site_packages=True)

        go_to_ve()

        # check requirements
        if update_ve or envreqs < envspec:
            import pip
            pip.main(initial_args=['install', '-r', REQUIREMENTS, '--upgrade'])
            file(VE_TIMESTAMP, 'w').close()
        sys.exit(0)
    else:
        print "VirtualEnv need to be updated"
        print "Run ./manage.py update_ve"
        sys.exit(1)

go_to_ve()

# Wizzy run engine

# test params
import sys
sys.path.append(path.join(PROJECT_ROOT, '../'))
# end test

def main():
    from airy.core import manager
    manager.execute(PROJECT_ROOT, sys.argv)

if __name__ == "__main__":
    main()

