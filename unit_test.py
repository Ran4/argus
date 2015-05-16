
def performUnitTests():
    print "#"*79
    print "UNIT TESTING STARTED"
    print "#"*79
    
    import xmlwikiparser2
    xmlwikiparser2.test(verbose=True)
    print "#"*39
    
    import attribute_value_parser
    attribute_value_parser.test(verbose=False)
    print "#"*39

    import attribute_key_parser
    attribute_key_parser.test(verbose=False)
    print "#"*39
    
    
    print "#"*79
    print "UNIT TESTING COMPLETED"
    print "#"*79

if __name__ == "__main__":
    performUnitTests()
