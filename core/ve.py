"Virtualenv utils"
import sys
import subprocess
import virtualenv
import shutil
from os import path

def check_ve(project_root, argv):
    VE_ROOT = path.join(project_root, '.ve')
    VE_TIMESTAMP = path.join(VE_ROOT, 'timestamp')
    REQUIREMENTS = path.join(project_root, 'requirements.pip')

    envtime = path.exists(VE_ROOT) and path.getmtime(VE_ROOT) or 0
    envreqs = path.exists(VE_TIMESTAMP) and path.getmtime(VE_TIMESTAMP) or 0
    envspec = path.getmtime(REQUIREMENTS)

    def go_to_ve(ve_root):
        # going into ve
        if not ve_root in sys.prefix:
            retcode = 3
            while retcode == 3:
                if sys.platform == 'win32':
                    python = path.join(VE_ROOT, 'Scripts', 'python.exe')
                else:
                    python = path.join(VE_ROOT, 'bin', 'python')
                try:
                    retcode = subprocess.call([python, path.join(project_root, 'manage.py')] + argv[1:])
                except KeyboardInterrupt:
                    retcode = 1
            sys.exit(retcode)

    update_ve = 'update_ve' in argv
    if update_ve or envtime < envspec or envreqs < envspec:
        if update_ve:
            # install ve
            if envtime < envspec:
                if path.exists(VE_ROOT):
                    shutil.rmtree(VE_ROOT)
                virtualenv.logger = virtualenv.Logger(consumers=[])
                virtualenv.create_environment(VE_ROOT, site_packages=True)

            go_to_ve(VE_ROOT)

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

    go_to_ve(VE_ROOT)
