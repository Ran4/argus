
def performUnitTests():
    print "#"*79
    print "UNIT TESTING STARTED"
    print "#"*79
    
    import xmlwikiparser2
    xmlwikiparser2.test(verbose=False)
    
    import attribute_value_parser
    attribute_value_parser.test(verbose=False)

    import attribute_key_parser
    attribute_key_parser.test(verbose=False)
    
    print "#"*79
    print "UNIT TESTING COMPLETED"
    print "#"*79

if __name__ == "__main__":
    performUnitTests()
