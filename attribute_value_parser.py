import re
class AttributeValueParser:
    def __init__(self):
        pass
        #Pattern for getting b from [[a|b]]
        self.patternPipeLink = re.compile(r"\[\[(?:[^\[]*?)\|(.*?)\]\]")
        
        #Pattern for getting a from [[a]]
        self.patternLink = re.compile(r'\[\[(.*?)\]\]')
        
        #Pattern for getting list name from {{list name| or {{list name}}
        self.patternList = re.compile(r'\{\{([^|]+?)(?:[ ]*)(?:\||\})')
        
        #Pattern for getting entries from a "bulleted list"
        self.patternBulletedList = re.compile("^(?:\{\{(?:.*?))(?=\|)|(?:\|*)class=(?:.*?)\||(?:\|*)list_style=(?:.*?)\||(?:\|*)style=(?:.*?)\||(?:\|*)item(?:\d*)_style=(?:.*?)\||\|(.*?)(?=\|)|\|([^\|]*?)\}\}$")
        
        #Pattern for getting entries from a "flatlist"
        self.patternFlatlist= re.compile("^(?:\{\{(?:.*?))\||(?:\|*)(?:[ ]*)class=(?:.*?)\||(?:\|*)(?:[ ]*)list_style=(?:.*?)\||(?:\|*)(?:[ ]*)style=(?:.*?)\||(?:\|*)(?:[ ]*)indent=(?:.*?)\||(?:\|*)(?:[ ]*)item(?:\d*)_style=(?:.*?)\||(?:\*|\#)(?:[ ]*)([^\*\#]+)(?=(?:\||\*|\#))|(?:\||\*|\#)(?:[ ]*)([^\*\#\}]*?)\}\}$")
    
        #Pattern for getting entries from a "startflatlist"
        self.patternStartflatlist = re.compile("^\{\{(?:.*?)\}\}|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*]+)(?=\*)|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*]+)\{\{(?:.*?)\}\}$")
        
        #Pattern for getting entries from an "endplainlist"
        self.patternEndplainlist  = re.compile("^\{\{(?:.*?)\}\}|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*]+)(?=\*)|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*]+)\{\{(?:.*?)\}\}$")

        #Pattern for getting entries from a "Plainlist"
        self.patternPlainlist = re.compile("^(?:\{\{(?:.*?))\||(?:\|*)(?:[ ]*)class=(?:.*?)\||(?:\|*)(?:[ ]*)list_style=(?:.*?)\||(?:\|*)(?:[ ]*)style=(?:.*?)\||(?:\|*)(?:[ ]*)indent=(?:.*?)\||(?:\|*)(?:[ ]*)item(?:\d*)_style=(?:.*?)\||(?:\*|\#)(?:[ ]*)([^\*\#]+)(?=(?:\||\*|\#))|(?:\||\*|\#)(?:[ ]*)([^\*\#\}]*?)\}\}$")
        
        #Pattern for getting entries from an "endflowlist"
        self.patternEndflowlist = re.compile("^\{\{(?:.*?)\}\}|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*]+)(?=\*)|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*]+)\{\{(?:.*?)\}\}$")
        
        #Pattern for getting entries from a "flowlist"
        self.patternFlowlist = re.compile("^(?:\{\{(?:.*?))\||(?:\|*)(?:[ ]*)class=(?:.*?)\||(?:\|*)(?:[ ]*)list_style=(?:.*?)\||(?:\|*)(?:[ ]*)style=(?:.*?)\||(?:\|*)(?:[ ]*)indent=(?:.*?)\||(?:\|*)(?:[ ]*)item(?:\d*)_style=(?:.*?)\||(?:\*|\#)(?:[ ]*)([^\*\#]+)(?=(?:\||\*|\#))|(?:\||\*|\#)(?:[ ]*)([^\*\#\}]*?)\}\}$")

        #Pattern for getting entries from a "hlist"
        self.patternHlist = re.compile("^\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)list_style(?:[ ]*)=(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?:\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\|)|(?:\||\*|\#)*(?:[ ]*)([^\|\*\#]+)(?=(?:\||\#|\*))|(?:\||\*|\#)*(?:[ ]*)([^\|\*\#]+)\}\}$")
           
        #Pattern for getting entries from an "unbulleted list"
        self.patternUnbulletedList = re.compile("^\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)list_style(?:[ ]*)=(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?:\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\|)|(?:\||\*|\#)*(?:[ ]*)([^\|\*\#]+)(?=(?:\||\#|\*))|(?:\||\*|\#)*(?:[ ]*)([^\|\*\#]+)\}\}$")

        #Pattern for getting entries from a "pagelist"
        self.patternPagelist = re.compile("^\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)list_style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)nspace(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)delim(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:(?:\||\*|\#)+)(?:[ ]*)(.*?)(?=\||\*|\#)|(?:(?:\||\*|\#)+)(?:[ ]*)(.*?)\}\}$")

        #Pattern for getting entries from an "ordered list"
        self.patternOrderedList = re.compile("^\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)list_style_type(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_value(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)start(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:(?:\||\*|\#)+)(?:[ ]*)(.*?)(?=\|)|(?:(?:\||\*|\#)+)(?:[ ]*)(.*?)\}\}$")

        #Pattern for getting entries from a "toolbar"
        self.patternToolbar = re.compile("^\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)class(?:[ ]*)=(?:.*?)(?:\}\}|\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?:\}\}|\|)|(?:\|*)(?:[ ]*)separator(?:[ ]*)=(?:.*?)(?:\}\}|\|)|\|(.*?)(?=\|)|\|([^\|]*?)\}\}$")
                                     
                      
    def parseAttributeValue(self, value, verbose=False, logFileName=None):
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
        #TODO: Should the different patterns for all types of Wikilists be precompiled beforehand? 

        #Could be an image: ignore these before trying to parse it
        if any([value.endswith(fileExt) for fileExt in (".svg")]):
            if verbose:
                print "File extension found - attribute value", value, "was purged from records."
            return ""
            
        #First, replace all Wiki article links in the string.
        #    Step 1: Shit of the form [[blabla|derpderp]] should become derpderp
        if verbose:
                print "Entering link conversion of type 1 ([[a|b]])."
                print "    Value before was:", value
        value = self.patternPipeLink.sub(r"\g<1>", value)
        if verbose:
                print "    Value after became:", value
                
        #    Step 2: Shit of the form [[derpderp]] should become derpderp
        if verbose:
                print "Entering link conversion of type 2 ([[a]])."
                print "    Value before was:", value
        value = self.patternLink.sub(r"\g<1>", value)
        if verbose:
            print "    Value after became:", value
        
        #Now that we're done with that, we want to check if the attribute value is a list.
        if verbose:
                print "Checking if attribute value is a list..."
        match = self.patternList.match(value) #We can actually use match since we are only explicitly looking for matches at the beginning.
        if match:
            if verbose:
                print "List detected."
            listType = match.group(1)
            if verbose:
                print "    List type:", listType
            #Now that we have obtained the list type, we want to do different things depending on which list type it is.
            if listType == "bulleted list":
                if verbose:
                    print '    "bulleted list" detected.'

                #Returns a list of tuples with all matches, where each group corresponds to one tuple.
                return self.patternBulletedList.findall(value)
                
            elif listType == "flatlist":
                if verbose:
                    print '    "flatlist" detected.'
                #Note: We do NOT need to have a subcase for endflatlist environment, since that is initiated by {{startflatlist}}
                return self.patternFlatlist.findall(value)
                
            elif listType == "startflatlist":
                if verbose:
                    print '    "startflatlist" detected.'
                
                #Returns a list of tuples with all matches, where each group corresponds to one tuple.
                return self.patternStartflatlist.findall(value)
                
            elif listType == "plainlist":
                if verbose:
                    print '    some type of plainlist detected...'
                #A subcase for endplainlist environment:
                if value.endswith("{{endplainlist}}"):
                    if verbose:
                        print '    "endplainlist" detected.'
                    return self.patternEndplainlist.findall(value)
                else:
                    if verbose:
                        print '    "plainlist" detected.'
                return self.patternPlainlist.findall(value)
            
            elif listType == "flowlist":
                if verbose:
                    print '    some type of flowlist detected...'
                #A subcase for endflowlist environment:
                if value.endswith("{{endflowlist}}"):
                    if verbose:
                            print '    "endflowlist" detected.'
                    return self.patternEndflowlist.findall(value)
                else:
                    if verbose:
                            print '    "flowlist" detected.'
                    return patternFlowlist.findall(value)              
                
            elif listType == "hlist":
                if verbose:
                    print '    "hlist" detected.'

                #Returns a list of tuples with all matches, where each group corresponds to one tuple.
                return self.patternHlist.findall(value)
                
            elif listType == "unbulleted list":
                if verbose:
                    print '    "unbulleted list" detected.'

                #Returns a list of tuples with all matches, where each group corresponds to one tuple.
                return self.patternUnbulletedList.findall(value)
                
            elif listType == "pagelist":
                if verbose:
                    print '    "pagelist" detected.'

                #Returns a list of tuples with all matches, where each group corresponds to one tuple.
                return self.patternPagelist.findall(value)
                
            elif listType == "ordered list":
                if verbose:
                    print '    "ordered list" detected.'

                #Returns a list of tuples with all matches, where each group corresponds to one tuple.
                return self.patternOrderedList.findall(value)
                
            elif listType == "toolbar":
                if verbose:
                    print '    "toolbar" detected.'

                #Returns a list of tuples with all matches, where each group corresponds to one tuple.
                return self.patternToolbar.findall(value)
                
        else:
            #No list was found...
            if verbose:
                    print 'No list was found.'
                    print 'Returning', value
            return value
        
        
def test(verbose=False):
    testValues = [
        ('',''),
        ('germany','germany'),
        ('[[germany]]','germany'),
        ('[[confusingLink|germany]]','germany'),
        ('[[confusingLink|germany]] ister','germany ister'),
        
        #not yet working:
        ('[[confusingLink | germany]] ister','germany ister'),
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
