import argparse
import os
import shutil
import subprocess
import sys
import time
import zipfile

import frontdoor


REGISTRY = frontdoor.CommandRegistry('ci')
cmd = REGISTRY.decorate
ROOT=os.path.dirname(os.path.realpath(__file__))


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def from_root(path):
    """Returns a path relative to the root directory."""
    if os.name == 'nt':
        path = path.replace('/', '\\')
    return os.path.join(ROOT, path)


OUTPUT_DIR = from_root('output')
BUILD_DIR = os.path.join(OUTPUT_DIR, 'build')
SRC_DIR = ROOT


@cmd('clean', 'Wipes out build directory.')
def clean(args):
    mkdir(BUILD_DIR)
    shutil.rmtree(BUILD_DIR)
    print(' * spotless! *')


@cmd('build', 'Build stuff')
def build(args):
    def _build(shared):
        shared_str = 'shared' if shared else 'static'
        print('Building {} libs'.format(shared_str))

        b_dir = os.path.join(BUILD_DIR, shared_str) if shared_str else BUILD_DIR

        if shared:
            shared_opt = '-DBUILD_SHARED_LIBS=true'
        else:
            shared_opt = ''
        mkdir(b_dir)
        subprocess.check_call(
            'cmake -G "Visual Studio 14 2015 Win64" -H{} -B{} {}'
            .format(SRC_DIR, b_dir, shared_opt),
            shell=True,
            cwd=b_dir)
        subprocess.check_call(
            'cmake --build {} --config {} '.format(
                b_dir, 'debug'),
            shell=True,
            cwd=b_dir)

    _build(False)
    _build(True)


@cmd('luarocks', 'Makes directory with interpetter for Lua Rocks')
def lurocks(args):
    d_dir = os.path.join(OUTPUT_DIR, 'luarocks-interpreter')
    try:
        shutil.rmtree(d_dir)
    except:
        pass
    shutil.copytree(src=os.path.join(BUILD_DIR, 'shared/Debug'),
                    dst=d_dir)
    for ext in ['dll', 'exp', 'lib', 'pdb']:
        shutil.copy(os.path.join(d_dir, 'lua.{}'.format(ext)),
                    os.path.join(d_dir, 'lua5.3.{}'.format(ext)))
    shutil.copytree(src=from_root('include'),
                    dst=os.path.join(d_dir, 'include'))


if __name__ == "__main__":
    # Fix goofy bug when using Windows command prompt to ssh into Vagrant box
    # that puts \r into the strings.
    args = [arg.strip() for arg in sys.argv[1:]]
    result = REGISTRY.dispatch(args)
    sys.exit(result)
