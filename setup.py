import subprocess
import sys
from setuptools import setup
from setuptools.command.install import install

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        subprocess.check_call([sys.executable, '-m', 'pytest', 'tests'])

setup(cmdclass={'install': PostInstallCommand})