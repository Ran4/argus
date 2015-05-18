import re
import itertools
from datetime import date

from termcolor import colored

class AttributeValueParser:
    def __init__(self, verbose=False):
        
        #For parsing date environments
        self.months = {1 : "January",
            2 : "February",
            3 : "March",
            4 : "April",
            5 : "May",
            6 : "June",
            7 : "July",
            8 : "August",
            9 : "September",
            10 : "October",
            11 : "November",
            12 : "December",
        }
        
        #Pattern for removing <small> and </small>
        self.patternSmall = re.compile(r"\<[\/]*small\>")
        
        #Pattern for creating dot-separated lists
        self.patternDot = re.compile(u"\{\{\xB7\}\}")
        
        #Pattern for tidying up list entries
        self.patternFixListEntries = re.compile("^[ ]*(.*?)[\, ]*$")
        
        #Pattern for removing {{*}}
        self.patternCBDot = re.compile("\{\{(?:\*|ndash|mdash|spaced ndash)\}\}")
        
        #Pattern for removing titles encased as '''title'''
        self.patternTitle = re.compile("'''(.*?)'''")
        
        #Pattern for checking if string is enclosed by parantheses
        self.patternEnclosedByParentheses = re.compile("^\((?:[^\)\(]*)\)$")
        
        #Pattern for removing cref and contents
        self.patternCref = re.compile(r"\{\{cref[^\}]*?(?:\}\}\}\}\}|\}\}(?!\}))")
        
        #Pattern for removing sfn, refn, cite journal and sfnp
        #Also flagicon, pad, 
        self.patternSfn = re.compile(r"\{\{(?:sfn|refn|cite journal|citation needed|flagicon|pad)(?:.*?)\}\}")
        
        #Pattern for removing the "small" environment and replacing a <br />
        #directly before it, if there is one.
        self.patternSmallEnv = re.compile("(?:<br(?:[ ]*)(?:[\/]*)>)*\{\{(?:[ ]*)small(?:[ ]*)\|(?:[\']*)(.*?)(?:[\']*)\}\}")
        
        #Pattern for removing comments
        self.patternComment = re.compile(r"<!--(?:.*?)-->")
        
        #Pattern for removing thinsp environment
        self.patternThinsp = re.compile(r"\{\{thinsp\}\}|\{\{dot\}\}")
        
        #Pattern for removing sup environment
        self.patternSup = re.compile(r"\{\{sup\|(?:.*?)\}\}")
        
        #Pattern for removing references
        self.patternReference = re.compile(r"<(?:span|ref|ref group(?:[^\>])*|ref name(?:[^\>])*)>(?:.*?)<\/(?:ref|span)>|<ref(?:.*?)\/>")
        
        #Pattern for removing references of the type "(see: foobar)"
        self.patternSeeRef = re.compile(r"(?: \- |[ ])*\(see[ |\: ](?:.*?)\)")
        
        #Pattern for replacing nbsp with whitespaces
        self.patternNbsp = re.compile(r"(\&amp;)*(\&)*nbsp;")
        
        #Pattern for replacing &amp;ndash; with "-"
        self.patternNdash = re.compile(r"\&amp\;ndash\;")
        
        #Pattern for replacing &quot;
        self.patternQuote = re.compile(r"\&quot;")
        
        #Pattern for seeing if string ends with }}
        self.patternCurlyBrackets = re.compile(r"\}\}$")
        
        #Pattern for seeing if string starts with #
        self.patternStartsWithSquare = re.compile(r"^\#")
        
        #Pattern for getting everything on the right of the first pipe
        self.patternRightOfPipe = re.compile(r"\|(?:.*)")
        
        #Pattern for replacing <br />
        self.patternBr = re.compile("\<br[ ]*(?:[\/]*)[ ]*\>")
        
        #Pattern for replacing unicode hyphens
        self.patternHyphen = re.compile(u"\\u2013")
        
        #Pattern for getting b from [[a|b]]
        self.patternPipeLink = re.compile(r"\[\[(?:[ ]*)(?:[^\]]*?)(?:[ ]*)\|(?:[ ]*)(.*?)(?:[ ]*)\]\]")
        
        #Pattern for removing wikipedia pictures
        self.patternWikiPic = re.compile(r"\[\[file\:(.*?)\]\]")
        
        #Pattern for getting a from [[a]]
        self.patternLink = re.compile(r'\[\[(?:[ ]*)(.*?)(?:[ ]*)\]\]')
        
        #Pattern for removing the "Longitem", "bigger" or "nowrap" environments
        self.patternLongitem = re.compile(r'\{\{(?:[ ]*)(?:smaller|longitem|nowrap|bigger)(?:[ ]*)\|(?:(?:(?:[ ]*)(?:style|padding|line-height)(?:[^\|]+?)\|)*)(?:[ ]*)(.*?)(?:[ ]*)\}\}')
        
        #Gets death date and age out of a "death date and age" environment
        self.patternDda = re.compile('\{\{(?:birth date and age|bda)(?:[ ]*)(?=\|)(?:(?:\|(?:[ ]*)(?:df|mf)(?:[ ]*)=*(?:[^\|\}]*?)(?=\||\}))*\|(?:[ ]*)(\d+)(?:[ ]*)\|(?:[ ]*)(\d+)(?:[ ]*)\|(?:[ ]*)(\d+)(?:[ ]*)(?:\|(?:[ ]*)(?:df|mf)(?:[ ]*)=(?:.*?)(?=\||\}))*\}\})')
        
        #Gets date of birth out of a "birth date and age" environment (and NOT from a "birth date" environment)
        self.patternBda = re.compile('\{\{(?:birth date and age|bda)(?:[ ]*)(?=\|)(?:(?:\|(?:[ ]*)(?:df|mf)(?:[ ]*)=*(?:[^\|\}]*?)(?=\||\}))*\|(?:[ ]*)(\d+)(?:[ ]*)\|(?:[ ]*)(\d+)(?:[ ]*)\|(?:[ ]*)(\d+)(?:[ ]*)(?:\|(?:[ ]*)(?:df|mf)(?:[ ]*)=(?:.*?)(?=\||\}))*\}\})')
        
        #Gets date of birth out of a "birth date" environment
        self.patternDob = re.compile('\{\{(?:birth date|dob)(?:[ ]*)(?=\|)(?:(?:\|(?:[ ]*)(?:df|mf)(?:[ ]*)=*(?:[^\|\}]*?)(?=\||\}))*\|(?:[ ]*)(\d+)(?:[ ]*)\|(?:[ ]*)(\d+)(?:[ ]*)\|(?:[ ]*)(\d+)(?:[ ]*)(?:\|(?:[ ]*)(?:df|mf)(?:[ ]*)=(?:.*?)(?=\||\}))*\}\})')
        
        #Pattern for getting list name from {{list name| or {{list name}}
        self.patternList = re.compile(r'\{\{([^|]+?)(?:[ ]*)(?:\||\})')
        
        #TODO: Do lists starting with a {{tag}} have list attributes similar to
        #other lists? In which format?
        
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
        self.patternHlist = re.compile("^\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)class(?:[ ]*)=*(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)list_style(?:[ ]*)=*(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?:\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\|)|(?:\||\*|\#)*(?:[ ]*)([^\|\*\#]+?)(?:[ ]*)(?=(?:\||\#|\*))|(?:\||\*|\#)*(?:[ ]*)([^\|\*\#]+?)(?:[ ]*)\}\}$")
           
        #Pattern for getting entries from an "unbulleted list"
        self.patternUnbulletedList = re.compile("^\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)class(?:[ ]*)=*(?:.*?)(?=\||\})|(?:\|*)(?:[ ]*)list_style(?:[ ]*)=*(?:.*?)(?=\||\})|(?:\|*)(?:[ ]*)style(?:[ ]*)=*(?:.*?)(?=\||\})|(?:\|*)(?:[ ]*)indent(?:[ ]*)=*(?:.*?)(?:\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=*(?:.*?)(?=\||\})|(?:\||\*|\#)*(?:[ ]*)([^\|\*\#]+?)(?:[ ]*)(?=(?:\||\#|\*))|(?:\||\*|\#)(?:[ ]*)([^\|\*\#]+?)(?:[ ]*)\}\}$")

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
            
        #TODO: Remove all linked images (Ex: [[File:Andrei Tarkovsky.jpg|240px]])
            
        #The whole entry could be an image: ignore these before trying to parse
        #TODO: Might better be contains, not endswith???
        if any([value.endswith(fileExt) for fileExt in (".svg",)]):
            if verbose:
                print "File extension found - attribute value", value, "was purged from records."
            return ""
            
        #Replaces these with real < and > signs
        value = value.replace("&lt;","<").replace("&gt;",">")
        
        #TODO: death date and age environment (Ex: {{death date and age|1865|4|15|1809|2|12}})
        #        Output should be in format: 29 December 1986 (aged 54)
        #TODO: convert environment (Ex: {{convert|550|ft|m|0}})
        
        #Removes the {{*}} stuff
        if verbose:
            print "Entering removal of {{*}}."
            print "    Value before was: '%s'" % str(value)
        value = self.patternCBDot.sub(r"", value)
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Removes the titles encased as '''title'''
        if verbose:
            print "Entering removal of encased titles."
            print "    Value before was: '%s'" % str(value)
        value = self.patternTitle.sub(r"", value)
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
        
        #Remove all "cref" environments
        if verbose:
            print "Entering removal of cref environment and contents."
            print "    Value before was: '%s'" % str(value)
        value = self.patternCref.sub(r"", value)
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Remove all "sfn" environments
        if verbose:
            print "Entering removal of sfn environment and contents."
            print "    Value before was: '%s'" % str(value)
        value = self.patternSfn.sub(r"", value)
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Remove all "small" environments (Ex: {{small|(April 21, 1832 - July 10, 1832)}})
        #Plus, if these are preceeded by a <br />, this means that we should
        #remove that break before creating a list out of break-separated values.
        if verbose:
            print "Entering removal of 'small' environment, checking for preceding br-tags and replacing them with whitespace."
            print "    Value before was: '%s'" % str(value)
        value = self.patternSmallEnv.sub(r" \g<1>", value)
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Removes all ndashes
        if verbose:
            print "Entering removal of ndash."
            print "    Value before was: '%s'" % str(value)
        value = self.patternNdash.sub(r"-", value)
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
        
        #Removes all nbsps
        if verbose:
            print "Entering removal of nbsps."
            print "    Value before was: '%s'" % str(value)
        value = self.patternNbsp.sub(r" ", value)
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Removes the thinsp environment
        if verbose:
            print "Entering removal of thinsp."
            print "    Value before was: '%s'" % str(value)
        value = self.patternThinsp.sub(r"", value)
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Removes the sup environment
        if verbose:
            print "Entering removal of sup."
            print "    Value before was: '%s'" % str(value)
        value = self.patternSup.sub(r"", value)
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Removes all quot
        if verbose:
            print "Entering removal of quot."
            print "    Value before was: '%s'" % str(value)
        value = self.patternQuote.sub(r"'", value)
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Replaces all unicode hyphens
        if verbose:
            print "Entering removal of hyphens."
            print "    Value before was: '%s'" % str(value)
        value = self.patternHyphen.sub(r"-", value)
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Replaces some birthdate environments (Ex: {{birth date|1809|2|12}})
        #TODO: Handle more environments: http://en.wikipedia.org/wiki/Template:Birth_date
        #with plain text describing the same thing.
        #If the person in question is living, you get their age as well.
        if verbose:
            print "Entering parsing of birthdate environment."
            print "    Value before was: '%s'" % str(value)
        match = self.patternBda.match(value)
        if match:
            if verbose:
                print "        'Birthdate and age' environment detected."
            #Calculate the person's age in years
            today = date.today()
            ageInYears = today.year - int(match.group(1)) - ((today.month, today.day) < (int(match.group(2)), int(match.group(3))))
            #Replace match with a descriptive string
            #value = self.patternBda.sub(match.group(3) + " " + self.months[int(match.group(2))] + " " + match.group(1) + "(age " + str(ageInYears) + ")", value) #Note: we assume that second group is a digit
            try:
                dateAndAgeString = "%s %s %s (age %s)" % (match.group(3), self.months[int(match.group(2))], match.group(1), str(ageInYears))
            except:
                try:
                    dateAndAgeString = "%s %s %s (age %s)" % (match.group(2), self.months[int(match.group(3))], match.group(1), str(ageInYears))
                except:
                    #We define dateAndAgeString as an empty string if we have not defined it previously, so that we won't crash on subbing
                    dateAndAgeString = ""
                    print colored("        WARNING: Invalid date and age format when parsing attribute value '%s'" % value, "magenta")
            value = self.patternBda.sub(dateAndAgeString, value) 
        else:
            match = self.patternDob.match(value)
            if match:
                if verbose:
                    print "        'Date of birth' environment detected."
                try:
                    dateString = "%s %s %s" % (match.group(3), self.months[int(match.group(2))], match.group(1))
                except:
                    try:
                        dateString = "%s %s %s" % (match.group(2), self.months[int(match.group(3))], match.group(1))
                    except:
                        #We define dateString as an empty string if we have not defined it previously, so that we won't crash on subbing
                        dateString = ""
                        print colored("        WARNING: Invalid date format when parsing attribute value '%s'" % value, "magenta")
                value = self.patternDob.sub(dateString, value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Replaces some death date environments (death date and age)
        match = self.patternDda.match(value)
        if match:
            if verbose:
                print "        'Death date and age' environment detected."
            try:
                ageInYears = int(match.group(1)) - int(match.group(4)) - ((int(match.group(2)), int(match.group(3))) < (int(match.group(5)), int(match.group(6))))
                dateString = "%s %s %s (age %s)" % (match.group(3), self.months[int(match.group(2))], match.group(1), str(ageInYears))
            except:
                try:
                    ageInYears = int(match.group(1)) - int(match.group(4)) - (int(match.group(2)) < int(match.group(5)))
                    dateString = "%s %s %s (age %s)" % (match.group(3), self.months[int(match.group(2))], match.group(1), str(ageInYears))
                except:
                    try:
                        ageInYears = int(match.group(1)) - int(match.group(4))
                        dateString = "%s %s %s (age %s)" % (match.group(3), self.months[int(match.group(2))], match.group(1), str(ageInYears))
                    except:
                        #We define dateString as an empty string if we have not defined it previously, so that we won't crash on subbing
                        dateString = ""
                        print colored("        WARNING: Invalid date format when parsing attribute value '%s'" % value, "magenta")
            value = self.patternDda.sub(dateString, value)
        else:
            #Try if we can find a match for year of death environment (mutually exclusive to the former)
            match = self.patternDoy.match(value)
            if match:
                if verbose:
                    print "        'Death year and age' environment detected."
                try:
                    ageInYears = int(match.group(1)) - int(match.group(2))
                    dateString = "%s (age %s)" % (match.group(1), str(ageInYears))
                except:
                    try:
                        ageInYears = int(match.group(1)) - int(match.group(2))
                        dateString = "%s (age %s)" % (match.group(1), str(ageInYears))
                    except:
                        #We define dateString as an empty string if we have not defined it previously, so that we won't crash on subbing
                        dateString = ""
                        print colored("        WARNING: Invalid date format when parsing attribute value '%s'" % value, "magenta")
                value = self.patternDoy.sub(dateString, value)    
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
                    
        #Remove all <small> tags
        if verbose:
            print "Entering removal of <small> tags."
            print "    Value before was: '%s'" % str(value)
        value = self.patternSmall.sub(r"", value)
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Remove all comments
        if verbose:
            print "Entering removal of comments."
            print "    Value before was: '%s'" % str(value)
        value = self.patternComment.sub(r"", value)
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Remove all references
        if verbose:
            print "Entering removal of references."
            print "    Value before was: '%s'" % str(value)
        value = self.patternReference.sub(r"", value)
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
        
        #Remove all references of the type "(see: foobar)"
        if verbose:
            print "Entering removal of references of type '(see: foo)'."
            print "    Value before was: '%s'" % str(value)
        value = self.patternSeeRef.sub(r"", value)
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Remove all Wiki pictures
        if verbose:
            print "Entering removal of Wikipedia pictures of format [[file: asdasd|asdasdasd]]."
            print "    Value before was: '%s'" % str(value)
        value = self.patternWikiPic.sub(r"", value)
        
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
        
        #Now that we're done with that, we want to check if the attribute value
        #is a list.
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
                
            #Since we are in a list, we want to replace the <br />s with
            #whitespaces.
            if verbose:
                print "    Entering removal of <br />s, since we have discovered a list."
                print "        Value before was: '%s'" % str(value)
            value = self.patternBr.sub(r" ", value)
            
            if verbose:
                print "        Value after became: '%s'" % str(value)
            
            #Now that we have obtained the list type, we want to do different things depending on which list type it is.
            if listType == "bulleted list":
                if verbose:
                    print '    "bulleted list" detected.'

                #Returns a list of tuples with all matches, where each group corresponds to one tuple.
                returnList = filter(None, list(itertools.chain.from_iterable(self.patternBulletedList.findall(value))))
                
            elif listType == "flatlist" or listType == "flat list":
                if verbose:
                    print '    "flatlist" detected.'
                #Note: We do NOT need to have a subcase for endflatlist environment, since that is initiated by {{startflatlist}}
                returnList = filter(None, list(itertools.chain.from_iterable(self.patternFlatlist.findall(value))))
                
            elif listType == "startflatlist":
                if verbose:
                    print '    "startflatlist" detected.'
                
                #Returns a list of tuples with all matches, where each group corresponds to one tuple.
                returnList = filter(None, list(itertools.chain.from_iterable(self.patternStartflatlist.findall(value))))
                
            elif listType == "plainlist" or listType == "plain list":
                if verbose:
                    print '    some type of plainlist detected...'
                #A subcase for endplainlist environment:
                #TODO: There can occur a third case: a plainlist environment which does not close (See: article with Abraham Lincoln)
                if value.endswith("{{endplainlist}}"):
                    if verbose:
                        print '    "endplainlist" detected.'
                    returnList = filter(None, list(itertools.chain.from_iterable(self.patternEndplainlist.findall(value))))
                else:
                    if verbose:
                        print '    "plainlist" detected.'
                returnList = filter(None, list(itertools.chain.from_iterable(self.patternPlainlist.findall(value))))
            
            elif listType == "flowlist" or listType == "flow list":
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
                
            elif listType == "unbulleted list" or listType == "ublist":
                if verbose:
                    print '    "unbulleted list" detected.'

                #Returns a list of tuples with all matches, where each group corresponds to one tuple.
                returnList = filter(None, list(itertools.chain.from_iterable(self.patternUnbulletedList.findall(value))))
                
            elif listType == "pagelist" or listType == "page list":
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
                    print colored("WARNING: List of unknown type found!", "magenta")  
                returnList = ""
                
            #Fix list entries as needed
            if returnList != "":
                assert(isinstance(returnList, list))
                if verbose:
                    print '    Fixing list entries...'  
                for string in returnList:
                    match = self.patternFixListEntries.match(string)
                    if match:
                        string = match.group(1)
                    else:
                        if verbose:
                            print colored("WARNING: Fixing of list entries has failed.", "magenta")
                
                #Try to concatenate all elements enclosed in parantheses to the previous element
                newReturnList = [returnList[0]]
                for i, element in enumerate(returnList[1:]):
                    if self.patternEnclosedByParentheses.match(element):
                        newReturnList[-1] += element
                    else:
                        newReturnList.append(element)
                returnList = newReturnList
            if verbose:
                print "Returning: %s" % str(returnList)   
            return returnList
                
        else:
            #No list was found... Check if the attribute value is
            #<br />-separated or dot ({{.}})-separated. If that is the case, split it using that as a
            #separator. Otherwise, return the value as it is.
            
            
            #Remove everything on the right of first pipe, to compensate for bad Wikipedia formatting
            if verbose:
                print "Entering removal of right-of-pipe elements."
                print "    Value before was: '%s'" % str(value)
            value = self.patternRightOfPipe.sub(r"", value)
            if verbose:
                print "    Value after became: '%s'" % str(value)

            #Delete the entry if it starts with a #
            if verbose:
                print "Entering removal of #-prepended entries"
                print "    Value before was: '%s'" % str(value)
            value = self.patternStartsWithSquare.sub(r"", value)
            if verbose:
                print "    Value after became: '%s'" % str(value)
            
            #Remove eventual curly brackets at end
            if verbose:
                print "Entering removal of curly brackets."
                print "    Value before was: '%s'" % str(value)
            value = self.patternCurlyBrackets.sub(r"", value)
            if verbose:
                print "    Value after became: '%s'" % str(value)

            if "<br />" in value or "<br/>" in value or "<br>" in value:
                if verbose:
                    print 'Attribute value is a list separated by <br />.'
                    print "Returning '%s'" % str(value)
                value = filter(None, self.patternBr.split(value))
            else:
                #Checking for dot-separated lists
                if verbose:
                    print "Entering check for lists separated by dots."
                    print "    Value before was: '%s'" % str(value)
                match = self.patternDot.match(value)
                if match:
                    value = filter(None, self.patternDot.split(value))
                if verbose:
                    print "    Value after became: '%s'" % str(value)
                else:
                    if verbose:
                        print 'No list was found in attribute value.'
                        print "Returning '%s'" % str(value)
            return value
        
        
def test(verbose=False):
    
    def asserter(inValue, outValue):
        if (isinstance(inValue, str) or isinstance(inValue, unicode)) \
                and (isinstance(outValue, str), isinstance(outValue, unicode)):
            if len(inValue) != len(outValue):
                print colored("WARNING: Mismatching length!", "magenta")
            else:
                for i in range(len(inValue)):
                    if inValue[i] != outValue[i]:
                        print colored("WARNING: Mismatching character '%s' != '%s' at position %s" % \
                            (inValue[i], outValue[i], i),
                            "magenta")
        #else: #TODO: add per-character check for lists too...
        #    print colored("lolwhat, types=%s, %s" % (type(inValue), type(outValue)), "yellow")
                            
        assert(inValue == outValue)
    
    testValues = [
        #Trivial:
        ('',''),
        ('germany','germany'),
        #Links:
        ('[[germany]]','germany'),
        ('michael bloomberg','michael bloomberg'),
        ('[[confusingLink|germany]]','germany'),
        ('[[confusingLink|germany]] sister','germany sister'),
        #Multiple links:
        ('[[You should not see this|   Aber ]] [[confusingLink | Germany  ]] ist [[ geil    ]], [[da]]','Aber Germany ist geil, da'),
        #Longitem environment:
        ('{{longitem|virtually all subsequent [[western philosophy]], [[christian philosophy]] and pre-[[age of enlightenment|enlightenment]] science; also much [[islamic philosophy|islamic]] and [[jewish philosophy]] (see [[list of writers influenced by aristotle]])}}', 'virtually all subsequent western philosophy, christian philosophy and pre-enlightenment science; also much islamic and jewish philosophy'),
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
        #NESTED AND/OR MULTIPLE LISTS: DANGER WILL ROBINSON DANGER
        #('{{hlist|[[biology]]|[[zoology]]}} {{hlist|[[physics]]|[[metaphysics]]}}', ['biology', 'zoology', 'physics', 'metaphysics']),
    ]

    attributeValueParser = AttributeValueParser()
    
    print "Testing",
    print "attribute_value_parser.AttributeValueParser.parseAttributeValue()"
    
    for inValue, outValue in testValues:
        parsedValue = attributeValueParser.parseAttributeValue(inValue, verbose)
        if verbose: print "%s -> %s" % (inValue, parsedValue)
        asserter(parsedValue, outValue)
        
    if verbose:
        print colored("Successfully tested attribute_value_parser.AttributeValueParser.parseAttributeValue()", "green")
    else:
        print "Successfully tested attribute_value_parser.AttributeValueParser.parseAttributeValue()"

if __name__ == "__main__":
    test(verbose=True)
