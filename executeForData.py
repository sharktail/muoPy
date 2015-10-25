import os
import sys
from importlib import import_module

from muaompc import ldt

def mainS():
    prefix='bcg'
    filePath = sys.argv[1]
    destdir = sys.argv[2]
    sys.path.append(os.path.join(destdir, 'install_'+prefix))
    mpc = import_module(prefix+'.mpc')
    mpc.generate_mpc_data(filePath) # + 'regmpc.dat')

def main():
    codePath = sys.argv[1] #should be the absolute /path/to/downloads/code
    datfname = sys.argv[2] #should be path/to/datfile being executed
    
    codegendir = codePath
    sys.path.append(codegendir)
    mpc = import_module('src.mpc')
    mpc.generate_mpc_data(datfname)
    datname = ldt._get_name(datfname)
    datadir = os.path.join(codegendir, 'data', datname)

if __name__ == '__main__':
    main()










