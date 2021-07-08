#!/usr/bin/env python3

import argparse 
import os
import sys

import ptest

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Executes all regression tests.")
    ap.add_argument("build", help="PANDA build folder.")
    ap.add_argument("datadir", nargs="+", help="Regression test data search directory")
    ap.add_argument("--extra-tests", default=[], nargs="+", help="Folders where extra tests are stored")
    ap.add_argument("--build-is-bindir", action="store_true", help="Interpret the build folder argument as PANDA bin directory.")
    ap.add_argument("--include", metavar="LIST",
        help="comma separated list of tests to include")
    ap.add_argument("--exclude", metavar="LIST",
        help="comma separated list of tests to exclude")
    ap.add_argument("--dry-run", action="store_true", help="show test names but don't actually test")
    ap.add_argument("--verbose", action="store_true", help="show verbose output")
    args = ap.parse_args()

    for d in args.datadir:
        ptest.add_data_search_dir(d)

    ptest.set_build_is_bindir(args.build_is_bindir)
    ptest.set_build_dir(os.path.abspath(args.build))
    ptest.set_dry_run(args.dry_run)
    ptest.set_verbose(args.verbose)

    # Register all tests in the test directory.
    ptest.register_tests("tests")
    # Register extra tests
    for d in args.extra_tests:
        ptest.register_tests(d)

    if args.include and args.exclude:
        print("error: include and exclude arguments are mutually exclusive")
        sys.exit(1)
    elif args.include:
        ptest.run(includes=args.include.split(","))
    elif args.exclude:
        ptest.run(excludes=args.exclude.split(","))
    else:
        ptest.run()
