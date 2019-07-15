import sys
import argparse

from .tests import Test, TestCaseTest


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', dest='test', action='store_true',
                        help='run tests')

    args = parser.parse_args()

    if args.test:
        Test.run(TestCaseTest)


if __name__ == '__main__':
    sys.exit(main() or 0)
