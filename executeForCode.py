
from muaompc import ldt
import sys

def main():
    prefix='bcg'  # basic code generation
    fileName = sys.argv[1]
    print fileName
    ldt.setup_mpc_problem(fileName, prefix=prefix)

if __name__ == '__main__':
    main()