#!/usr/local/bin/python3
# encoding: utf-8
'''
 -- shortdesc

 is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2016 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from wage_parser import WageParser

__all__ = []
__version__ = 0.1
__date__ = '2016-10-28'
__updated__ = '2016-10-28'

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): 
    try:
        # Setup argument parser
        parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter)
#         parser.add_argument("-r", "--recursive", dest="recurse", action="store_true", help="recurse into subfolders [default: %(default)s]")
#         parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument(dest="in_file", help="the input CSV file")

        args = parser.parse_args()

        wage_parser = WageParser(args.in_file)
        wages = wage_parser.parse()

        print("Monthly wages for %s/%s\n" % wage_parser.month())
        for wage in wages:
            print("%s, %s, $%d.00" % (wage.person_id, wage.name, wage.wage))

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0

if __name__ == "__main__":
    sys.exit(main())