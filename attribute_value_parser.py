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
    
    pattern = "" #Insert overly complicated pattern here
    match = re.find(pattern, value)
    
    if not match:
        return "" 

    return match.groups()



def parseInfoBox(ib):
    for key, value in attributes:
        parsedValue = parseAttributeValue(value)
        writeToFile(json.dumps({key: parsedValue, indent=4), "output.txt")
        
    """    
    example:

    {{infobox scientist
    | residence = germany, switzerland, united states

    didriksregex("residence") == ("germany", "switzerland", "united states")
    """
        
def main():
    pass

if __name__ == "__main__":
    main()
