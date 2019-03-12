import sys, os
import argparse
import bcpy


def main(args=None):
    parser = argparse.ArgumentParser(description='bcpy is a Python wrapper for MSSQL bcp application.'
                                                 'Type "bcpy help" for the list of commands')
    subparsers = parser.add_subparsers(help='subcommand help')
    parser_cp = subparsers.add_parser('cp', help='cp help')
    parser_cp.add_argument('source', help='source file, table or sql query')
    parser_cp.add_argument('destination', help='destination file or table')
    parser_cp.add_argument('-t', '--type', choices=['t2f', 'f2t', 'q2f'],
                           default='f2t',
                           help='t2f: table to file,\nf2t: file to table,\nq2f: query to file')
    parser_cp.add_argument('-T', '--trusted-auth', action='store_true', default=True)
    parser_cp.add_argument('-u', '--username', help='sql server username')
    parser_cp.add_argument('-p', '--password', help='sql server password')
    parser_cp.set_defaults(func=cp)
    args = parser.parse_args()
    print(args)
    if args.cp:
        args.func(args)


def cp(args):
    print(f'source: {args.source} and destination: {args.destination}')
    # print(args)


if __name__ == "__main__":
    main()