import argparse

import sys


def config_argv(director):
    parser = _config_parser()

    args = parser.parse_args()

    director.display = args.display

    if args.sandbox:
        director.sandbox_dir = args.sandbox

    director.load(args.file)

    if not args.test and not args.run and not args.apply:
        if director.validate():
            director.sandbox_run()

    if args.test or args.run:
        is_valid = director.validate()

        if is_valid:
            print "The script is valid."

    if args.backup:
        sys.stderr.write("Backup not supported yet.\n")

    if args.run:
        director.sandbox_run()

    if args.apply:
        director.apply(args.keep)


def _config_parser():
    parser = argparse.ArgumentParser(description="FileSystem Director")

    parser.add_argument(
        'file',
        help='Input file'
    )

    parser.add_argument(
        '-s',
        '--sandbox',
        help='Change the default sandbox dir'
    )

    parser.add_argument(
        '-a',
        '--apply',
        help='Apply sandbox',
        action='store_true'
    )

    parser.add_argument(
        '-d',
        '--display',
        help='Display the sandbox tree',
        action='store_true'
    )

    parser.add_argument(
        '-t',
        '--test',
        help='Test the script',
        action='store_true'
    )

    parser.add_argument(
        '-r',
        '--run',
        help='Run the script',
        action='store_true'
    )

    parser.add_argument(
        '-k',
        '--keep',
        help='Keep the sandbox directory.',
        action='store_true'
    )

    parser.add_argument(
        '-b',
        '--backup',
        help='Backup before run',
        action='store_true'
    )

    return parser