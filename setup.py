import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "airy",
    version = "0.1",
    author = "LetoLab Ltd",
    author_email = "team@letolab.com",
    description = ("Web Application Framework"),
    long_description=read('README'),
    license = "BSD",
    keywords = "web development websockets",
    url = "http://airy.letolab.com",
    packages=find_packages(),
    include_package_data=True,
    requires=[
        'simplejson',
        'ipython',
    ],
    scripts=[
        'airy/bin/airy-admin.py',
    ],
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 3 - Alpha",
    ],
)
