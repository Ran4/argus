import re
import itertools
class AttributeValueParser:
    def __init__(self, verbose=False):
		
		#Pattern for removing <br /> and nbsp
        self.patternBr = re.compile(r"\<br[ ]*\/\>|&nbsp;")
		
        #Pattern for getting b from [[a|b]]
        self.patternPipeLink = re.compile(r"\[\[(?:[ ]*)(?:[^\]]*?)(?:[ ]*)\|(?:[ ]*)(.*?)(?:[ ]*)\]\]")
        
        #Pattern for getting a from [[a]]
        self.patternLink = re.compile(r'\[\[(?:[ ]*)(.*?)(?:[ ]*)\]\]')
        
        #Pattern for removing the "Longitem" or "nowrap" environment
        self.patternLongitem = re.compile(r'\{\{(?:[ ]*)(?:longitem|nowrap)(?:[ ]*)\|(?:(?:(?:[ ]*)(?:style|padding|line-height)(?:[^\|]+?)\|)*)(?:[ ]*)(.*?)(?:[ ]*)\}\}')
        
        #Pattern for getting list name from {{list name| or {{list name}}
        self.patternList = re.compile(r'\{\{([^|]+?)(?:[ ]*)(?:\||\})')
        
		#TODO: Do lists starting with a {{tag}} have list attributes similar to other lists? In which format?
        
        #Pattern for getting entries from a "bulleted list"
        self.patternBulletedList = re.compile("^(?:\{\{(?:.*?))(?=\|)|\|(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)list_style(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)(.*?)(?:[ ]*)(?=\|)|\|(?:[ ]*)([^\|]*?)(?:[ ]*)\}\}$")
        
        #Pattern for getting entries from a "flatlist"
        self.patternFlatlist= re.compile("^(?:\{\{(?:.*?))(?=\|)|\|(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\||\})|(?:\|*)(?:[ ]*)list_style(?:[ ]*)=(?:.*?)(?=\||\})|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\||\})|(?:\|*)(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?=\||\})|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\||\})|(?:\*|\#)(?:[ ]*)([^\*\#]+)(?:[ ]*)(?=(?:\||\*|\#))|(?:\||\*|\#)(?:[ ]*)([^\*\#\}]+?)(?:[ ]*)\}\}$")
    
        #Pattern for getting entries from a "startflatlist"
        self.patternStartflatlist = re.compile(r"^\{\{(?:.*?)\}\}|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*]+)(?:[ ]*)(?=\*)|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*]+?)(?:[ ]*)\{\{(?:.*?)\}\}$")
        
        #Pattern for getting entries from an "endplainlist"
        self.patternEndplainlist  = re.compile(r"^\{\{(?:.*?)\}\}|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*]+?)(?:[ ]*)(?=\*)|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*]+?)(?:[ ]*)\{\{(?:.*?)\}\}$")

        #Pattern for getting entries from a "plainlist"
        self.patternPlainlist = re.compile("^(?:\{\{(?:.*?))(?=\|)|\|(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)list_style(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\||\})|(?:\*|\#)(?:[ ]*)([^\*\#]+)(?:[ ]*)(?=(?:\||\*|\#))|(?:\||\*|\#)(?:[ ]*)([^\*\#\}]*?)(?:[ ]*)\}\}$")
        
        #Pattern for getting entries from an "endflowlist"
        self.patternEndflowlist = re.compile("^\{\{(?:.*?)\}\}|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*\#\|]+?)(?:[ ]*)(?=\||\*|\#)|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*\#\|]+?)(?:[ ]*)\{\{(?:.*?)\}\}$")
        
        #Pattern for getting entries from a "flowlist"
        self.patternFlowlist = re.compile("^(?:\{\{(?:.*?))(?=\|)|\|(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)list_style(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\||\})|(?:\*|\#|\|)(?:[ ]*)([^\*\#\|]+?)(?:[ ]*)(?=(?:\||\*|\#))|(?:\||\*|\#)(?:[ ]*)([^\*\#\}]*?)(?:[ ]*)\}\}$")

        #Pattern for getting entries from a "hlist"
        self.patternHlist = re.compile("^\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)list_style(?:[ ]*)=(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?:\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\|)|(?:\||\*|\#)*(?:[ ]*)([^\|\*\#]+?)(?:[ ]*)(?=(?:\||\#|\*))|(?:\||\*|\#)*(?:[ ]*)([^\|\*\#]+?)(?:[ ]*)\}\}$")
           
        #Pattern for getting entries from an "unbulleted list"
        self.patternUnbulletedList = re.compile("^\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\||\})|(?:\|*)(?:[ ]*)list_style(?:[ ]*)=(?:.*?)(?=\||\})|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\||\})|(?:\|*)(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?:\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\||\})|(?:\||\*|\#)*(?:[ ]*)([^\|\*\#]+?)(?:[ ]*)(?=(?:\||\#|\*))|(?:\||\*|\#)(?:[ ]*)([^\|\*\#]+?)(?:[ ]*)\}\}$")

        #Pattern for getting entries from a "pagelist"
        self.patternPagelist = re.compile("^\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)list_style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)nspace(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)delim(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:(?:\||\*|\#)+)(?:[ ]*)(.*?)(?:[ ]*)(?=\||\*|\#)|(?:(?:\||\*|\#)+)(?:[ ]*)(.*?)(?:[ ]*)\}\}$")

        #Pattern for getting entries from an "ordered list"
        self.patternOrderedList = re.compile("^\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)list_style_type(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_value(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)start(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:(?:\||\*|\#)+)(?:[ ]*)(.*?)(?:[ ]*)(?=\|)|(?:(?:\||\*|\#)+)(?:[ ]*)(.*?)(?:[ ]*)\}\}$")

        #Pattern for getting entries from a "toolbar"
        self.patternToolbar = re.compile("^\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)separator(?:[ ]*)=(?:.*?)(?=\}\}|\|)|\|(?:[ ]*)(.*?)(?:[ ]*)(?=\|)|\|(?:[ ]*)([^\|]*?)(?:[ ]*)\}\}$")
        
        if verbose:
			print "AttributeValueParser has compiled all regex patterns"
    
                      
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
        if verbose:
			print "\nNew parse initiated."
			
        #Could be an image: ignore these before trying to parse it
        if any([value.endswith(fileExt) for fileExt in (".svg")]):
            if verbose:
                print "File extension found - attribute value", value, "was purged from records."
            return ""
        
        #Replace all <br /> and similar
        if verbose:
		    print "Entering removal of line breaks and nbsps."
		    print "    Value before was: '%s'" % str(value)
        value = self.patternBr.sub(r" ", value)
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
        
        #Replace all Wiki article links in the string.
        #    Step 1: Stuff of the form [[blabla|derpderp]] should become derpderp
        if verbose:
		    print "Entering link conversion of type 1 ([[a|b]])."
		    print "    Value before was: '%s'" % str(value)
        value = self.patternPipeLink.sub(r"\g<1>", value)
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
                
        #    Step 2: Stuff of the form [[derpderp]] should become derpderp
        if verbose:
            print "Entering link conversion of type 2 ([[a]])."
            print "    Value before was: '%s'" % str(value)
        
        value = self.patternLink.sub(r"\g<1>", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #    Removal of the "Longitem" environment
        if verbose:
            print "Entering removal of 'Longitem' and 'nowrap' environments."
            print "    Value before was: '%s'" % str(value)
        value = self.patternLongitem.sub(r"\g<1>", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
        
        #Now that we're done with that, we want to check if the attribute value is a list.
        #TODO: "plain list" on wikipedia might redirect to "plainlist". Fix this?
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
                returnList = filter(None, list(itertools.chain.from_iterable(self.patternBulletedList.findall(value))))
                
            elif listType == "flatlist":
                if verbose:
                    print '    "flatlist" detected.'
                #Note: We do NOT need to have a subcase for endflatlist environment, since that is initiated by {{startflatlist}}
                returnList = filter(None, list(itertools.chain.from_iterable(self.patternFlatlist.findall(value))))
                
            elif listType == "startflatlist":
                if verbose:
                    print '    "startflatlist" detected.'
                
                #Returns a list of tuples with all matches, where each group corresponds to one tuple.
                returnList = filter(None, list(itertools.chain.from_iterable(self.patternStartflatlist.findall(value))))
                
            elif listType == "plainlist":
                if verbose:
                    print '    some type of plainlist detected...'
                #A subcase for endplainlist environment:
                if value.endswith("{{endplainlist}}"):
                    if verbose:
                        print '    "endplainlist" detected.'
                    returnList = filter(None, list(itertools.chain.from_iterable(self.patternEndplainlist.findall(value))))
                else:
                    if verbose:
                        print '    "plainlist" detected.'
                returnList = filter(None, list(itertools.chain.from_iterable(self.patternPlainlist.findall(value))))
            
            elif listType == "flowlist":
                if verbose:
                    print '    some type of flowlist detected...'
                #A subcase for endflowlist environment:
                if value.endswith("{{endflowlist}}"):
                    if verbose:
                            print '    "endflowlist" detected.'
                    returnList = filter(None, list(itertools.chain.from_iterable(self.patternEndflowlist.findall(value))))
                else:
                    if verbose:
                            print '    "flowlist" detected.'
                    returnList = filter(None, list(itertools.chain.from_iterable(self.patternFlowlist.findall(value))))
                
            elif listType == "hlist":
                if verbose:
                    print '    "hlist" detected.'

                #Returns a list of tuples with all matches, where each group corresponds to one tuple.
                returnList = filter(None, list(itertools.chain.from_iterable(self.patternHlist.findall(value))))
                
            elif listType == "unbulleted list":
                if verbose:
                    print '    "unbulleted list" detected.'

                #Returns a list of tuples with all matches, where each group corresponds to one tuple.
                returnList = filter(None, list(itertools.chain.from_iterable(self.patternUnbulletedList.findall(value))))
                
            elif listType == "pagelist":
                if verbose:
                    print '    "pagelist" detected.'

                #Returns a list of tuples with all matches, where each group corresponds to one tuple.
                returnList = filter(None, list(itertools.chain.from_iterable(self.patternPagelist.findall(value))))
                
            elif listType == "ordered list":
                if verbose:
                    print '    "ordered list" detected.'

                #Returns a list of tuples with all matches, where each group corresponds to one tuple.
                returnList = filter(None, list(itertools.chain.from_iterable(self.patternOrderedList.findall(value))))
                
            elif listType == "toolbar":
                if verbose:
                    print '    "toolbar" detected.'

                #Returns a list of tuples with all matches, where each group corresponds to one tuple.
                returnList = filter(None, list(itertools.chain.from_iterable(self.patternToolbar.findall(value))))
            else:
				if verbose:
					print '    list of unknown type found.'
                    
				returnList = ""
                
            if verbose:
				print "Returning: %s" % str(returnList)
            return returnList
                
        else:
            #No list was found...
            if verbose:
                    print 'No list was found.'
                    print "Returning '%s'" % str(value)
            return value
        
        
def test(verbose=False):
    testValues = [
		#Tested and working:
        ('',''),
        ('germany','germany'),
        #Links:
        ('[[germany]]','germany'),
        ('[[confusingLink|germany]]','germany'),
        ('[[confusingLink|germany]] ister','germany ister'),
        #Multiple links:
        ('[[You should not see this|   Aber ]] [[confusingLink | Germany  ]] ist [[ geil    ]], [[da]]','Aber Germany ist geil, da'),
        #Longitem environment:
        ('{{longitem|virtually all subsequent [[western philosophy]], [[christian philosophy]] and pre-[[age of enlightenment|enlightenment]] science; also much [[islamic philosophy|islamic]] and [[jewish philosophy]] (see [[list of writers influenced by aristotle]])}}', 'virtually all subsequent western philosophy, christian philosophy and pre-enlightenment science; also much islamic and jewish philosophy (see list of writers influenced by aristotle)'),
        #Lists:
        ('{{bulleted list |class=sdfsdf|list_style=adfsdf|style=asdfsdf|item_style=sdfsdf |item2_style=sdfsdf| We only need this |information }}', ['We only need this', 'information']),
        ('{{flatlist|     class   =    asdfasd|style=      asdfsdfs|        indent   =asdfsdfsd|* [[cat]]* [[dog]]* [[horse]]* [[cow]]* [[sheep]]* [[pig]]}}', ['cat', 'dog', 'horse', 'cow', 'sheep', 'pig']),
		('{{startflatlist}}* [[All]]* [[your]]* [[base]]* [[are]]* [[belong]]* [[to]]* [[us]]{{endflatlist}}', ['All','your','base','are','belong','to','us']),
		#('{{plainlist}}* [[These   ]]* [[not visible | wonky   ]]* [[lists]]* are   * [[hard]]* [[to]]* [[you cant see me|parse]]{{endplainlist}}',['These','wonky','lists','are','hard','to','parse']),
		('{{plainlist|class=sdfsdf|style=border:solid 1px silver; background:lightyellow|indent=2|* [[congo]]* [[niger]]* [[zululand]]}}', ['congo', 'niger', 'zululand']),
		('{{flowlist}}*   [[Mao Zedong]]*    [[Ho Chi Minh]]    * [[Lars Ohly]]     {{endflowlist}}', ['Mao Zedong','Ho Chi Minh','Lars Ohly']),
		('{{flowlist |class  =asdfasdf |style  =asdas |* [[platypus]]   * [[iguana]]  *  [[zorse]]   }}',['platypus','iguana','zorse']),
		('{{hlist|gondwanaland|   mu|  leng  |class     = class|style     = style|list_style  = style for ul tag|item_style  = style for all li tags|item1_style = style for first li tag |item2_style = style for second li tag |   atlantis   |indent    = indent for the list}}', ['gondwanaland', 'mu', 'leng', 'atlantis']),
		('{{unbulleted list|snorlax   |     pikachu|class     = class|style     = style|list_style  = style for ul tag|item_style  = style for all li tags|item1_style = style for first li tag |item2_style = style for second li tag |  charizard }}', ['snorlax', 'pikachu', 'charizard']),
		('{{pagelist|nspace= |delim=''|sean connery   |    roger moore|   george lazenby   }}', ['sean connery', 'roger moore', 'george lazenby']),
		('{{ordered list |item1_value=value1 |item2_value=value2|start=start|   alan turing |claude shannon    |item1_style=CSS1 |item2_style=CSS2 }}', ['alan turing', 'claude shannon']),
		('{{toolbar|separator=comma |bethany    |     ambrose}}', ['bethany', 'ambrose']),
		
		#Stuff from real Wikipedia (starting with article about aristotle):
		('{{unbulleted list |[[peripatetic school]] |[[aristotelianism]]}}', ['peripatetic school', 'aristotelianism']),
		('{{unbulleted list |[[golden mean (philosophy)|golden mean]] |[[aristotelian logic]] |[[syllogism]] |[[hexis]] |[[hylomorphism]] |[[on the soul|theory of the soul]]}}', ['golden mean', 'aristotelian logic', 'syllogism', 'hexis', 'hylomorphism', 'theory of the soul']),
		('{{hlist |[[parmenides]] |[[socrates]] |[[plato]] |[[heraclitus]] |[[democritus]]}}', ['parmenides', 'socrates', 'plato', 'heraclitus', 'democritus']),
		#NESTED LISTS DANGER WILL ROBINSON DANGER
		#('{{hlist|[[biology]]|[[zoology]]}} {{hlist|[[physics]]|[[metaphysics]]}}', ['biology', 'zoology', 'physics', 'metaphysics']),
    ]

    attributeValueParser = AttributeValueParser()
    
    print "Testing",
    print "attribute_value_parser.AttributeValueParser.parseAttributeValue()"
    
    for inValue, outValue in testValues:
        parsedValue = attributeValueParser.parseAttributeValue(inValue, verbose)
        if verbose: print "%s -> %s" % (inValue, parsedValue)
        assert(parsedValue == outValue)
        
    print "Successfully tested",
    print "attribute_value_parser.AttributeValueParser.parseAttributeValue()"

if __name__ == "__main__":
    test(verbose=True)
