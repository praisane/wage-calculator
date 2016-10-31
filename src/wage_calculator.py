#!/usr/local/bin/python3
# encoding: utf-8
import sys

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from wage_parser import WageParser

def main(argv=None): 
    try:
        # Setup argument parser
        parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-s", "--statistics", dest="print_stats", action="store_true", default=False , help="print out more detailed statistics")
        parser.add_argument(dest="in_file", help="the input CSV file")

        args = parser.parse_args()

        wage_parser = WageParser(args.in_file)
        wages = wage_parser.parse()

        print("Monthly wages for %s/%s\n" % wage_parser.month())
        for wage in wages:
            print("%s, %s, $%d.00" % (wage.person_id, wage.name, wage.wage))
            if args.print_stats:
                print("\tTotal hours worked %d, evening hours %d, overtime hours %d" % (wage.hours, wage.evening_hours, wage.overtime_hours))

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0

if __name__ == "__main__":
    sys.exit(main())