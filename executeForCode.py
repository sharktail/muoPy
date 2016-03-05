
from muaompc import ldt
import sys
import Settings

def main():
    prefix = Settings.Prefix
    #prefix='bcg'  # basic code generation
    fileName = sys.argv[1]
    destdir = sys.argv[2]
    ldt.setup_mpc_problem(fileName, prefix=prefix, destdir=destdir)

if __name__ == '__main__':
    main()