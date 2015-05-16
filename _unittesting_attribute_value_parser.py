import re

def parseAttributeValue(value, verbose=False, logFileName=None):
    """Takes an attribute value as a string in un-edited wikiUML format 
    and parses it into either a string value or a tuple of string values.
    
    Arguments:
    If verbose is True, statements will be printed
    If logFileName is a string, anything happenening (including errors)
        will be logged to the filename logFileName 
    
    If no value was found, "" is returned.
    If the value is not considered to be relevant text, ""  is returned
    
    Examples:
    value = "{{br separated values|entry1|entry2}}"
    parseAttributeValue(value) == (entry1, entry2)

    value = "Germany"
    parseAttributeValue(value) == "Germany"

    value = "Barack Obama signature.svg"
    parseAttributeValue(value) == ""
    """

    #Could be an image: ignore these before trying to parse it
    if any([value.endswith(fileExt) for fileExt in (".svg")]):
        return ""
    
    #~ pattern = "" #Insert overly complicated pattern here
    #~ match = re.match(pattern, value)
    #~ 
    #~ if not match:
    #~     return "" 

    #return match.groups()
    
    return value


def test(verbose=False):
    testValues = [
        ('',''),
        ('germany','germany'),
        ('germany','germany'),
    ]

    attributeValueParser = AttributeValueParser()
    
    print "Testing",
    print "attribute_value_parser.AttributeValueParser.parseAttributeValue()"
    
    for inValue, outValue in testValues:
        parsedValue = attributeValueParser.parseAttributeValue(inValue)
        if verbose: print "%s -> %s" % (inValue, parsedValue)
        assert(parsedValue == outValue)
        
    print "Successfully tested",
    print "attribute_value_parser.AttributeValueParser.parseAttributeValue()"

if __name__ == "__main__":
    test(verbose=True)
