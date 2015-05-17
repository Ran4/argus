#!/usr/bin/env python2
import sys

import termcolor

def performUnitTests(verbose):
    print "#"*79
    print "UNIT TESTING STARTED"
    print "#"*79
    
    
    WARNING = '\033[93m'
    #use termcolor module instead!
    
    warningMessage = termcolor.colored("Problem with unittest!",
            "yellow")
    bigDivider = "#"*79
    divider = "#"*39
    
    try:
        import xmlwikiparser2
        xmlwikiparser2.test(verbose)
    except:
        print warningMessage
    print divider
    
    try:
        import attribute_value_parser
        attribute_value_parser.test(verbose)
    except:
        print warningMessage
    print divider

    try:
        import attribute_key_parser
        attribute_key_parser.test(verbose)
    except:
        print warningMessage
    print divider
    
    
    print bigDivider
    print "UNIT TESTING COMPLETED"
    print bigDivider

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        if arg.lower() in ["-v","--verbose"]:
            verbose = True
            break
    else:
        verbose = False
    performUnitTests(verbose)
