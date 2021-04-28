import sys


def err_exit(msg, code=1):
    print(msg, file=sys.stderr)
    sys.exit(code)
