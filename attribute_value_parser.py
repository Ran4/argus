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
	#TODO: Should the different patterns for all types of Wikilists be precompiled beforehand? 

    #Could be an image: ignore these before trying to parse it
    if any([value.endswith(fileExt) for fileExt in (".svg")]):
		if verbose:
			print "File extension found - attribute value", value, "was purged from records."
        return ""
        
    #First, replace all Wiki article links in the string.
    #	Step 1: Shit of the form [[blabla|derpderp]] should become derpderp
    if verbose:
			print "Entering link conversion of type 1 ([[a|b]])."
			print "    Value before was:", value
    pattern = re.compile(r"\[\[(?:[^\[]*?)\|(.*?)\]\]")
    value = pattern.sub(r"\g<1>", value)
    if verbose:
			print "    Value after became:", value
			
    #	Step 2: Shit of the form [[derpderp]] should become derpderp
    if verbose:
			print "Entering link conversion of type 2 ([[a]])."
			print "    Value before was:", value
    pattern = re.compile(r'\[\[(.*?)\]\]')
    value = pattern.sub(r"\g<1>", value)
    if verbose:
			print "    Value after became:", value
    
    #Now that we're done with that, we want to check if the attribute value is a list.
    if verbose:
			print "Checking if attribute value is a list..."
    pattern = re.compile(r'\{\{([^|]+?)(?:[ ]*)(?:\||\})')
    match = pattern.match(value) #We can actually use match since we are only explicitly looking for matches at the beginning.
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
			#The regex pattern giving bulleted list entries as groups
			pattern = re.compile("^(?:\{\{(?:.*?))(?=\|)|(?:\|*)class=(?:.*?)\||(?:\|*)list_style=(?:.*?)\||(?:\|*)style=(?:.*?)\||(?:\|*)item(?:\d*)_style=(?:.*?)\||\|(.*?)(?=\|)|\|([^\|]*?)\}\}$")
			
			#Returns a list of tuples with all matches, where each group corresponds to one tuple.
			return pattern.findall(value)
			
		elif listType == "flatlist":
			if verbose:
				print '    "flatlist" detected.'
			#TODO: We do NOT need to have a subcase for endflatlist environment, since that is initiated by {{startflatlist}}
			
			#The regex pattern giving list entries as groups
			pattern = re.compile("^(?:\{\{(?:.*?))\||(?:\|*)(?:[ ]*)class=(?:.*?)\||(?:\|*)(?:[ ]*)list_style=(?:.*?)\||(?:\|*)(?:[ ]*)style=(?:.*?)\||(?:\|*)(?:[ ]*)indent=(?:.*?)\||(?:\|*)(?:[ ]*)item(?:\d*)_style=(?:.*?)\||(?:\*|\#)(?:[ ]*)([^\*\#]+)(?=(?:\||\*|\#))|(?:\||\*|\#)(?:[ ]*)([^\*\#\}]*?)\}\}$")
			
		elif listType == "startflatlist":
			if verbose:
				print '    "startflatlist" detected.'
			#The regex pattern giving list entries as groups
			pattern = re.compile("^\{\{(?:.*?)\}\}|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*]+)(?=\*)|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*]+)\{\{(?:.*?)\}\}$")
			
			#Returns a list of tuples with all matches, where each group corresponds to one tuple.
			return pattern.findall(value)
			
		elif listType == "plainlist":
			if verbose:
				print '    some type of plainlist detected...'
			#A subcase for endplainlist environment:
			if value.endswith("{{endplainlist}}"):
				#The regex pattern giving list entries as groups
				pattern = re.compile("^\{\{(?:.*?)\}\}|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*]+)(?=\*)|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*]+)\{\{(?:.*?)\}\}$")
				
			else:
				#The regex pattern giving list entries as groups
				pattern = re.compile("^(?:\{\{(?:.*?))\||(?:\|*)(?:[ ]*)class=(?:.*?)\||(?:\|*)(?:[ ]*)list_style=(?:.*?)\||(?:\|*)(?:[ ]*)style=(?:.*?)\||(?:\|*)(?:[ ]*)indent=(?:.*?)\||(?:\|*)(?:[ ]*)item(?:\d*)_style=(?:.*?)\||(?:\*|\#)(?:[ ]*)([^\*\#]+)(?=(?:\||\*|\#))|(?:\||\*|\#)(?:[ ]*)([^\*\#\}]*?)\}\}$")
				
			#Returns a list of tuples with all matches, where each group corresponds to one tuple.
			return pattern.findall(value)
		
		elif listType == "flowlist":
			if verbose:
				print '    some type of plainlist detected...'
			#A subcase for endflowlist environment:
			if value.endswith("{{endflowlist}}"):
				#The regex pattern giving list entries as groups
				pattern = re.compile("^\{\{(?:.*?)\}\}|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*]+)(?=\*)|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*]+)\{\{(?:.*?)\}\}$")
			else:
				#The regex pattern giving list entries as groups
				pattern = re.compile("^(?:\{\{(?:.*?))\||(?:\|*)(?:[ ]*)class=(?:.*?)\||(?:\|*)(?:[ ]*)list_style=(?:.*?)\||(?:\|*)(?:[ ]*)style=(?:.*?)\||(?:\|*)(?:[ ]*)indent=(?:.*?)\||(?:\|*)(?:[ ]*)item(?:\d*)_style=(?:.*?)\||(?:\*|\#)(?:[ ]*)([^\*\#]+)(?=(?:\||\*|\#))|(?:\||\*|\#)(?:[ ]*)([^\*\#\}]*?)\}\}$")
			
			#Returns a list of tuples with all matches, where each group corresponds to one tuple.
			return pattern.findall(value)
			
		elif listType == "hlist":
			if verbose:
				print '    "hlist" detected...'
			
			#The regex pattern giving list entries as groups
			pattern = re.compile("^\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)list_style(?:[ ]*)=(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?:\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\|)|(?:\||\*|\#)*(?:[ ]*)([^\|\*\#]+)(?=(?:\||\#|\*))|(?:\||\*|\#)*(?:[ ]*)([^\|\*\#]+)\}\}$")
			
			#Returns a list of tuples with all matches, where each group corresponds to one tuple.
			return pattern.findall(value)
			
		elif listType == "unbulleted list":
				
			#The regex pattern giving list entries as groups
			pattern = re.compile("^\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)list_style(?:[ ]*)=(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?:\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\|)|(?:\||\*|\#)*(?:[ ]*)([^\|\*\#]+)(?=(?:\||\#|\*))|(?:\||\*|\#)*(?:[ ]*)([^\|\*\#]+)\}\}$")
			
			#Returns a list of tuples with all matches, where each group corresponds to one tuple.
			return pattern.findall(value)
			
		elif listType == "pagelist":
				
			#The regex pattern giving list entries as groups
			pattern = re.compile("^\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)list_style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)nspace(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)delim(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:(?:\||\*|\#)+)(?:[ ]*)(.*?)(?=\||\*|\#)|(?:(?:\||\*|\#)+)(?:[ ]*)(.*?)\}\}$")
			
			#Returns a list of tuples with all matches, where each group corresponds to one tuple.
			return pattern.findall(value)
			
		elif listType == "ordered list":
				
			#The regex pattern giving list entries as groups
			pattern = re.compile("^\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)list_style_type(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_value(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)start(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:(?:\||\*|\#)+)(?:[ ]*)(.*?)(?=\|)|(?:(?:\||\*|\#)+)(?:[ ]*)(.*?)\}\}$")
			
			#Returns a list of tuples with all matches, where each group corresponds to one tuple.
			return pattern.findall(value)
			
		elif listType == "toolbar":
				
			#The regex pattern giving list entries as groups
			pattern = re.compile("^\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)class(?:[ ]*)=(?:.*?)(?:\}\}|\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?:\}\}|\|)|(?:\|*)(?:[ ]*)separator(?:[ ]*)=(?:.*?)(?:\}\}|\|)|\|(.*?)(?=\|)|\|([^\|]*?)\}\}$")
			
			#Returns a list of tuples with all matches, where each group corresponds to one tuple.
			return pattern.findall(value)
			
	else:
		#The system has failed
		return ""


#~ def parseInfoBox(ib):
#~     for key, value in attributes:
#~         parsedValue = parseAttributeValue(value)
#~         writeToFile(json.dumps({key: parsedValue}, indent=4), "output.txt")
#~         
#~     """    
#~     example:
#~ 
#~     {{infobox scientist
#~     | residence = germany, switzerland, united states
#~ 
#~     didriksregex("residence") == ("germany", "switzerland", "united states")
#~     """
        
def main():
    pass

if __name__ == "__main__":
    main()
