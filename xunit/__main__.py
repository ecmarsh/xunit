import sys

from .tests import Test


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    Test.run()


if __name__ == '__main__':
    sys.exit(main() or 0)
