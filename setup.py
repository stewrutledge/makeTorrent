from distutils.core import setup

setup(
    name='makeTorrent',
    version='0.14',
    packages=['makeTorrent'],
    install_requires=[
        'bencode',
    ],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='Basic library for creating torrents',
    long_description=open('README.rst').read(),
    author='Stewart Rutledge',
    author_email='stew.rutledge@gmail.com',
    url='https://github.com/stewrutledge/makeTorrent'
)
