import re
import itertools
from datetime import date
import copy
from termcolor import colored

class AttributeValueParser:
    def __init__(self, verbose=False):
        """Initializes all regex patterns and dictionaries needed for parsing.
        
        Regex patterns are grouped by functionality for easier merging, if you
        should wish to do so later.
        
        Arguments:
        If verbose is True, current operations will be printed.
        """
        
        #Dictionary for parsing date environments
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
        
        ########################################################################
        #LIST NAME REGEX PATTERNS
        #(For identifying list environments)
        ########################################################################
        
        self.patternBulletedListName = re.compile("(?i)bulleted[ ]*list|blist")
        self.patternFlatlistName = re.compile("(?i)flat[ ]*list") #flist?
        self.patternStartflatlistName = re.compile("(?i)start[ ]*flat[ ]*list|sflist")
        self.patternPlainlistName = re.compile("(?i)(?:start)*plain[ ]*list") #plist?
        self.patternFlowlistName = re.compile("(?i)flow[ ]*list") #flist?
        self.patternHlistName = re.compile("(?i)hlist")
        self.patternUnbulletedListName = re.compile("(?i)unbulleted[ ]*list|ublist")
        self.patternPagelistName = re.compile("(?i)page[ ]*list") #plist?
        self.patternOrderedListName = re.compile("(?i)ordered[ ]*list|olist")
        self.patternToolbarName = re.compile("(?i)tool[ ]*bar|toolbar")
        
        ########################################################################
        #LIST ENVIRONMENT REGEX PATTERNS
        #(for getting the elements from a Wiki markup list)
        ########################################################################
        
        #TODO: Do lists starting with a {{tag}} have list attributes similar to
        #other lists? In which format?
        
        #Pattern for getting entries from a "bulleted list"
        self.patternBulletedList = re.compile("^(?i)(?:\{\{(?:.*?))(?=\|)|\|(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)list_style(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)(.*?)(?:[ ]*)(?=\|)|\|(?:[ ]*)([^\|]*?)(?:[ ]*)\}\}$")
        #Pattern for getting entries from a "flatlist"
        self.patternFlatlist= re.compile("^(?i)(?:\{\{(?:.*?))(?=\|)|\|(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\||\})|(?:\|*)(?:[ ]*)list_style(?:[ ]*)=(?:.*?)(?=\||\})|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\||\})|(?:\|*)(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?=\||\})|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\||\})|(?:\*|\#)(?:[ ]*)([^\*\#]+)(?:[ ]*)(?=(?:\||\*|\#))|(?:\||\*|\#)(?:[ ]*)([^\*\#\}]+?)(?:[ ]*)\}\}$")
        #Pattern for getting entries from a "startflatlist"
        self.patternStartflatlist = re.compile(r"^(?i)\{\{(?:.*?)\}\}|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*]+)(?:[ ]*)(?=\*)|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*]+?)(?:[ ]*)\{\{(?:.*?)\}\}$")
        #Pattern for getting entries from an "endplainlist"
        self.patternEndplainlist  = re.compile(r"^(?i)(?:\{\{(?:.*?))(?=\})|(?:\||\*|\#)(?:[ ]*)([^\*\#]+?)(?:[ ]*)(?=(?:\||\*|\#))|(?:\||\*|\#)(?:[ ]*)([^\*\#\}]*?)(?:[ ]*)\{\{endplainlist\}\}$")
        #Pattern for getting entries from a "plainlist"
        self.patternPlainlist = re.compile("^(?i)(?:\{\{(?:.*?))(?=\|)|\|(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)list_style(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\||\})|(?:\*|\#)(?:[ ]*)([^\*\#]+)(?:[ ]*)(?=(?:\||\*|\#))|(?:\||\*|\#)(?:[ ]*)([^\*\#\}]*?)(?:[ ]*)\}\}$")
        #Pattern for getting entries from an "endflowlist"
        self.patternEndflowlist = re.compile("^(?i)\{\{(?:.*?)\}\}|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*\#\|]+?)(?:[ ]*)(?=\||\*|\#)|(?:(?:\||\*|\#)+)(?:[ ]*)([^\*\#\|]+?)(?:[ ]*)\{\{(?:.*?)\}\}$")
        #Pattern for getting entries from a "flowlist"
        self.patternFlowlist = re.compile("^(?i)(?:\{\{(?:.*?))(?=\|)|\|(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)list_style(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?=\||\})|\|(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\||\})|(?:\*|\#|\|)(?:[ ]*)([^\*\#\|]+?)(?:[ ]*)(?=(?:\||\*|\#))|(?:\||\*|\#)(?:[ ]*)([^\*\#\}]*?)(?:[ ]*)\}\}$")
        #Pattern for getting entries from a "hlist"
        self.patternHlist = re.compile("^(?i)\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)class(?:[ ]*)=*(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)list_style(?:[ ]*)=*(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?:\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\|)|(?:\||\*|\#)*(?:[ ]*)([^\|\*\#]+?)(?:[ ]*)(?=(?:\||\#|\*))|(?:\||\*|\#)*(?:[ ]*)([^\|\*\#]+?)(?:[ ]*)\}\}$")
        #Pattern for getting entries from an "unbulleted list"
        self.patternUnbulletedList = re.compile("^(?i)\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)class(?:[ ]*)=*(?:.*?)(?=\||\})|(?:\|*)(?:[ ]*)list_style(?:[ ]*)=*(?:.*?)(?=\||\})|(?:\|*)(?:[ ]*)style(?:[ ]*)=*(?:.*?)(?=\||\})|(?:\|*)(?:[ ]*)indent(?:[ ]*)=*(?:.*?)(?:\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=*(?:.*?)(?=\||\})|(?:\||\*|\#)*(?:[ ]*)([^\|\*\#]+?)(?:[ ]*)(?=(?:\||\#|\*))|(?:\||\*|\#)(?:[ ]*)([^\|\*\#]+?)(?:[ ]*)\}\}$")
        #Pattern for getting entries from a "pagelist"
        self.patternPagelist = re.compile("^(?i)\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)list_style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)indent(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)nspace(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)delim(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:(?:\||\*|\#)+)(?:[ ]*)(.*?)(?:[ ]*)(?=\||\*|\#)|(?:(?:\||\*|\#)+)(?:[ ]*)(.*?)(?:[ ]*)\}\}$")
        #Pattern for getting entries from an "ordered list"
        self.patternOrderedList = re.compile("^(?i)\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)list_style_type(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)item(?:\d*)_value(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)start(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:(?:\||\*|\#)+)(?:[ ]*)(.*?)(?:[ ]*)(?=\|)|(?:(?:\||\*|\#)+)(?:[ ]*)(.*?)(?:[ ]*)\}\}$")
        #Pattern for getting entries from a "toolbar"
        self.patternToolbar = re.compile("^(?i)\{\{(?:.*?)(?=\|)|(?:\|*)(?:[ ]*)class(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)style(?:[ ]*)=(?:.*?)(?=\}\}|\|)|(?:\|*)(?:[ ]*)separator(?:[ ]*)=(?:.*?)(?=\}\}|\|)|\|(?:[ ]*)(.*?)(?:[ ]*)(?=\|)|\|(?:[ ]*)([^\|]*?)(?:[ ]*)\}\}$")

        ########################################################################
        #MISC REGEX PATTERNS
        #(For identifying/deleting/replacing/extracting content from 
        #   various miscellaneous environments)
        ########################################################################
        
        #Pattern for creating dot-separated lists
        self.patternDot = re.compile(u"(?i)\{\{\u00b7\}\}")
        #TODO: Pattern for replacing unicode hyphens (Why do this though???)
        self.patternHyphen = re.compile(u"\\u2013")

        #########################################
        ##REGEX PATTERNS FOR REMOVING WIKI MARKUP

        #Pattern for removing cref and contents
        self.patternCref = re.compile(r"(?i)\{\{cref[^\}]*?(?:\}\}\}\}\}|\}\}(?!\}))")
        #Pattern for removing comments
        self.patternComment = re.compile(r"<!--(?:.*?)-->")
        #Pattern for removing thinsp tag
        self.patternThinsp = re.compile(r"(?i)\{\{thinsp\}\}")
        #Pattern for removing sup environment
        self.patternSup = re.compile(r"(?i)\{\{sup\|(?:.*?)\}\}")
        #Pattern for removing references
        self.patternReference = re.compile(r"(?i)<(?:span|ref|ref group(?:[^\>])*|ref name(?:[^\>])*)>(?:.*?)<\/(?:ref|span)>|<ref(?:.*?)\/>")
        #Pattern for removing references of the type "(see: foobar)"
        self.patternSeeRef = re.compile(r"(?i)(?: \- |[ ])*\(see[ |\: ](?:.*?)\)")
        #Pattern for removing <small> and </small> tags
        self.patternSmall = re.compile(r"(?i)\<[\/]*small\>")
        #Pattern for removing {{*}}, and ndash, mdash andspaced ndash
        self.patternCBDot = re.compile("(?i)\{\{(?:\*|ndash|mdash|spaced ndash)\}\}")
        #Pattern for removing sfn, refn, cite journal, sfnp, native phrase/name and pad
        self.patternSfn = re.compile(r"(?i)\{\{(?:native(.*?)|sfn|refn|cite journal|citation needed|dn|disambiguation needed|pad)(?:.*?)\}\}")
        #Pattern for removing list sub-titles encased as '''title'''
        self.patternTitle = re.compile("'''(.*?)'''")
        #Pattern for removing Wiki markup picture links
        self.patternWikiPic = re.compile(r"(?i)\[\[file\:(.*?)\]\]")
        
        ##########################################
        ##REGEX PATTERNS FOR REPLACING WIKI MARKUP
        
        #Pattern for replacing nbsp with whitespaces
        self.patternNbsp = re.compile(r"(?i)(?:(\&amp;)*(\&)*nbsp;)|\{\{dot\}\}|\{\{int\:dot\-separator\}\}|\{\{nbsp\}\}")
        #Pattern for replacing &amp;ndash; with "-"
        self.patternNdash = re.compile(r"(?i)\&amp\;ndash\;")
        #Pattern for replacing &quot; with a '
        self.patternQuote = re.compile(r"(?i)\&quot;")
        #Pattern for replacing <br /> with " "
        #or split string with it as separator
        self.patternBr = re.compile("(?i)\<br[ ]*(?:[\/]*)[ ]*\>")
        
        #######################################
        ##REGEX PATTERNS FOR EXTRACTING CONTENT
        
        #Pattern for getting b from [[a|b]]
        self.patternPipeLink = re.compile(r"\[\[(?:[ ]*)(?:[^\]]*?)(?:[ ]*)\|(?:[ ]*)(.*?)(?:[ ]*)\]\]")
        #Pattern for getting a from [[a]]
        self.patternLink = re.compile(r'\[\[(?:[ ]*)(.*?)(?:[ ]*)\]\]')
        #Pattern for getting (a) from ''(a)'' or (a)
        self.patternDoubleQuotes = re.compile("^(?:\'\'(?=\())*(.*?)(?:(?<=\))\'\')*$")
        
        #Pattern for extracting contents from the "Longitem", "bigger",
        #   "nowrap", "flagicon", "flag" and "flagcountry" environments
        self.patternLongitem = re.compile(r'(?i)\{\{(?:[ ]*)(?:smaller|longitem|nowrap|bigger|flagicon|flag|flagcountry)(?:[ ]*)\|(?:(?:(?:[ ]*)(?:style|padding|line-height)(?:[^\|]+?)\|)*)(?:[ ]*)(.*?)(?:[ ]*)\}\}')
        #Pattern for extracting contents of the "small" environment
        #and replacing a <br /> directly preceding it, if there is one.
        self.patternSmallEnv = re.compile("(?i)(?:<br(?:[ ]*)(?:[\/]*)>)*\{\{(?:[ ]*)small(?:[ ]*)\|(?:[\']*)(.*?)(?:[\']*)\}\}")
        
        #Gets death date and age out of a "death date and age" environment
        self.patternDda = re.compile('(?i)\{\{(?:birth date and age|bda)(?:[ ]*)(?=\|)(?:(?:\|(?:[ ]*)(?:df|mf)(?:[ ]*)=*(?:[^\|\}]*?)(?=\||\}))*\|(?:[ ]*)(\d+)(?:[ ]*)\|(?:[ ]*)(\d+)(?:[ ]*)\|(?:[ ]*)(\d+)(?:[ ]*)(?:\|(?:[ ]*)(?:df|mf)(?:[ ]*)=(?:.*?)(?=\||\}))*\}\})')
        #Gets death date and age out of a "death year and age" environment
        self.patternDya = re.compile('(?i)\{\{(?:death year and age|dya)(?:[ ]*)(?=\|)(?:(?:\|(?:[ ]*)(?:df|mf)(?:[ ]*)=*(?:[^\|\}]*?)(?=\||\}))*\|(?:[ ]*)(\d+)(?:[ ]*)\|(?:[ ]*)(\d+)(?:[ ]*)(?:\|(?:[ ]*)(?:\d+)(?:[ ]*))*(?:\|(?:[ ]*)(?:df|mf)(?:[ ]*)=(?:.*?)(?=\||\}))*\}\})')
        #Gets date of birth out of a "birth date and age" environment (and NOT from a "birth date" environment)
        self.patternBda = re.compile('(?i)\{\{(?:birth date and age|bda)(?:[ ]*)(?=\|)(?:(?:\|(?:[ ]*)(?:df|mf)(?:[ ]*)=*(?:[^\|\}]*?)(?=\||\}))*\|(?:[ ]*)(\d+)(?:[ ]*)\|(?:[ ]*)(\d+)(?:[ ]*)\|(?:[ ]*)(\d+)(?:[ ]*)(?:\|(?:[ ]*)(?:df|mf)(?:[ ]*)=(?:.*?)(?=\||\}))*\}\})')
        #Gets date of birth out of a "birth date" environment
        self.patternDob = re.compile('(?i)\{\{(?:birth date|dob)(?:[ ]*)(?=\|)(?:(?:\|(?:[ ]*)(?:df|mf)(?:[ ]*)=*(?:[^\|\}]*?)(?=\||\}))*\|(?:[ ]*)(\d+)(?:[ ]*)\|(?:[ ]*)(\d+)(?:[ ]*)\|(?:[ ]*)(\d+)(?:[ ]*)(?:\|(?:[ ]*)(?:df|mf)(?:[ ]*)=(?:.*?)(?=\||\}))*\}\})')
        
        #Pattern for extracting approximate dates from the circa environment
        self.patternCirca = re.compile("(?i)\{\{(?:c\.|circa)[ ]*(?:\}\})*|(?:\|(\d+?)\}\})|\|(\d+?)(?=\|)")
        #Gets name and dates of marriage from a "marriage" environment as the three first capture groups
        self.patternMarriage = re.compile('^(?i)(?:\{\{marriage(?:.*?))(?=\|)|\|(?:[ ]*)\(\)(?:\=)*small(?:er)*(?:[ ]*)(?=\||\})|(?:\|*)(?:[ ]*)end(?:[ ]*)=*(?:.*?)(?=\||\})|(?:\||\*|\#)(?:[ ]*)(.+?)(?:[ ]*)(?=(?:\||\*|\#))|(?:\||\*|\#)(?:[ ]*)(.*?)(?:[ ]*)\}\}$')
        #self.patternMarriage = re.compile('(?i)\{\{(?:marriage)(?:[ ]*)(?=\|)(?:\|(?:(?:[ ]*)\((?:[ ]*)\)(?:[ ]*)\=*(?:[ ]*)small(?:er)*[ ]*)(?=\|)|\|(?:[ ]*)end(?:[ ]*)\=*(?:.*?)(?=\|)|\|(.+?)(?=\|))(?:\|(?:(?:[ ]*)\((?:[ ]*)\)(?:[ ]*)\=*(?:[ ]*)small(?:er)*[ ]*)|\|(?:[ ]*)end(?:[ ]*)\=*(?:.*?)(?=\|)|\|(.+?)(?=\|))(?:\|(?:(?:[ ]*)\((?:[ ]*)\)(?:[ ]*)\=*(?:[ ]*)small(?:er)*[ ]*)(?=\|)|\|(?:[ ]*)end(?:[ ]*)\=*(?:.*?)(?=\|)|\|(.+?)(?=\||\}))(?:\|(?:(?:[ ]*)\((?:[ ]*)\)(?:[ ]*)\=*(?:[ ]*)small(?:er)*[ ]*)(?=\|)|\|(?:[ ]*)end(?:[ ]*)\=*(?:.*?)(?=\||\})|\|(.+?)(?=\||\}))*(?:\|(?:(?:[ ]*)\((?:[ ]*)\)(?:[ ]*)\=*(?:[ ]*)small(?:er)*[ ]*)(?=\|)|\|(?:[ ]*)end(?:[ ]*)\=*(?:.*?)(?=\||\})|\|(.+?)(?=\||\}))*\}\}')
        
        #Pattern for extracting list name from {{list name| or {{list name}}
        #Match starts at start of list and ends at end.
        self.patternList = re.compile(r'\{\{(?:[ ]*)([^|]+?)(?:[ ]*)(?=\||\})(?:.*?)\}\}')
        
        #############################################
        ##REGEX PATTERNS FOR CLEANING UP FINAL RESULT
        
        #Pattern for removing }} from end of string
        #(used for cleanup)
        self.patternCurlyBrackets = re.compile(r"\}\}$")
        #Pattern for removing string if it starts with #
        #(used for cleanup)
        self.patternStartsWithSquare = re.compile(r"^\#")
        #Pattern for removing everything on the right of the first pipe
        #(used for cleanup)
        self.patternRightOfPipe = re.compile(r"\|(?:.*)")
        #Pattern for removing whitespaces from ends of strings
        #and also trailing commas.
        #(used for cleanup)
        self.patternWhitespaces = re.compile("^[ ]*(.*?)(?: )*$")
        
        ################################################
        ##REGEX PATTERNS FOR IDENTIFYING SPECIAL STRINGS
        
        #Pattern for checking if string is enclosed by parantheses
        #(possibly also by double quotation marks)
        self.patternEnclosedByParentheses = re.compile("^(\'\')*\((?:[^\)\(]*)\)(\'\')*$")
        self.patternEndsWithComma = re.compile("(?:.*)\,$")
        #Identifies a "marriage" environment
        self.patternIdentifyMarriage = re.compile('(?i)(\{\{marriage(?:.*?)\}\})')
        #Identifies a "circa" environment
        self.patternIdentifyCirca = re.compile('(?i)(\{\{(?:circa|c\.)(?:.*?)\}\})')
        #Identifies a "hlist" environment
        self.patternIdentifyHlist = re.compile('(?i)\{\{hlist(?:.*?)\}\}')
        #Identifies a list with a match
        self.patternListNoCatchGroups = re.compile(r'\{\{(?:[\w ]+?)(?:\|class(?:\=*)[^\}]*)*(?:(?=\|)(?:.*?)\}\}|\}\}(?:.*)(?:\{\{end(?:[^\}]*)\}\})*)')

        if verbose:
            print "AttributeValueParser has compiled all regex patterns"
            
            
    def concatenateParenthesesEnclosedEntries(self, aList, verbose=False):
        """Takes a list which should be maximally parsed already, and
        concatenates entries enclosed by parentheses to the previous ones.
        Also, remove '', wherever they occur.
        
        Arguments:
        If verbose is True, current operations will be printed.
        A list of strings.
        
        Return value:
        A list which has been cleaned to specifications.
        """
        #Clean list entries as needed
        if aList != "":
            assert(isinstance(aList, list))
            if verbose:
                print '    Removing whitespaces on both ends...'  
            for i, string in enumerate(aList):
                match = self.patternWhitespaces.match(string)
                if match:
                    if verbose:
                        print "        " + string + ' being fixed to ' + match.group(1)
                    aList[i] = match.group(1)
                else:
                    if verbose:
                        print colored("WARNING: Fixing of list entries has failed.", "magenta")
                    
            #Try to concatenate the next element to all elements ending with a comma
            if len(aList) > 1:
                newList = [aList[0]]
                if verbose:
                    print '    Concatenating subceding entries to entries ending with commas...'
                for i, string in enumerate(aList[1:]):
                    if self.patternEndsWithComma.match(aList[i]):
                        newList[-1] += " " + string
                        if verbose:
                            print "        Appending " + string + " to previous. Result is: " + newList[i-1]
                    else:
                        newList.append(string)
                aList = copy.deepcopy(newList)
                 
                #Try to concatenate all elements enclosed in parantheses to the previous element
                newList = [aList[0]]
                if verbose:
                    print '    Concatenating entries in parentheses to previous entries...'
                for i, string in enumerate(aList[1:]):
                    if self.patternEnclosedByParentheses.match(string):
                        newList[-1] += " " + self.patternDoubleQuotes.match(string).group(1)
                        if verbose:
                            print "        Appending " + self.patternDoubleQuotes.match(string).group(1) + " to previous. Result is: " + newList[-1]
                    else:
                        newList.append(string)
                aList = newList
        return aList
      
      
    def initialParsing(self, value, verbose=False):
        """Does the initial part of the parsing, which should be done for all
        inputs. Please note that the order you parse things in might have
        and impact on the end results.
        
        Arguments: a string to be parsed.
        
        Return value: a parsed string.
        """
        #The whole entry could be an image: ignore these before trying to parse
        #TODO: Might better be contains, not endswith, and a regex for filenames
        if any([value.endswith(fileExt) for fileExt in (".svg",)]):
            if verbose:
                print "File extension found - attribute value", value, "was purged from records."
            return ""
            
        #Replaces &lt; and &gt; with actual < and > signs
        value = value.replace("&lt;","<").replace("&gt;",">")
        
        #Removes the {{*}} stuff
        if verbose:
            print colored("Entering removal of {{*}}.", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternCBDot.sub(r"", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Removes the titles encased as '''title'''
        if verbose:
            print colored("Entering removal of encased titles.", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternTitle.sub(r"", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
        
        #Remove all "cref" environments
        if verbose:
            print colored("Entering removal of cref environment and contents.", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternCref.sub(r"", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Remove all "sfn" environments
        if verbose:
            print colored("Entering removal of sfn environment and contents.", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternSfn.sub(r"", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Remove all "small" environments (Ex: {{small|(April 21, 1832 - July 10, 1832)}})
        #Plus, if these are preceeded immediately by a <br />, this means that
        #we should remove that break before creating a list out of
        #break-separated values.
        if verbose:
            print colored("Entering removal of 'small' environment, checking for preceding br-tags and replacing them with whitespace.", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternSmallEnv.sub(r" \g<1>", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Removes all ndashes
        if verbose:
            print colored("Entering removal of ndash.", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternNdash.sub(r"-", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
        
        #Removes all nbsps
        if verbose:
            print colored("Entering removal of nbsps.", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternNbsp.sub(r" ", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Removes the thinsp environment
        if verbose:
            print colored("Entering removal of thinsp.", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternThinsp.sub(r"", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Removes the sup environment
        if verbose:
            print colored("Entering removal of sup.", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternSup.sub(r"", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Removes all quot
        if verbose:
            print colored("Entering removal of quot.", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternQuote.sub(r"'", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #TODO: Replaces all unicode hyphens
        if verbose:
            print colored("Entering removal of hyphens.", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternHyphen.sub(r"-", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Replaces some birthdate environments (Ex: {{birth date|1809|2|12}})
        #with plain text describing the same thing.
        #If the person in question is living, you get their age as well.
        if verbose:
            print colored("Entering parsing of birthdate environment.", "blue")
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
            match = self.patternDya.match(value)
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
                value = self.patternDya.sub(dateString, value)    
        
        if verbose:
            print "    Value after became: '%s'" % str(value)
                    
        #Remove all <small> tags
        if verbose:
            print colored("Entering removal of <small> tags.", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternSmall.sub(r"", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Remove all comments
        if verbose:
            print colored("Entering removal of comments.", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternComment.sub(r"", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Remove all references
        if verbose:
            print colored("Entering removal of references.", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternReference.sub(r"", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
        
        #Remove all references of the type "(see: foobar)"
        if verbose:
            print colored("Entering removal of references of type '(see: foo)'.", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternSeeRef.sub(r"", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Remove all Wiki markup picture links
        if verbose:
            print colored("Entering removal of Wiki markup pictures of format [[file: picture|text]].", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternWikiPic.sub(r"", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
        
        #Replace all Wiki markup article links in the string.
        #    Step 1: Stuff of the form [[link|example]] should become example
        if verbose:
            print colored("Entering link conversion of type 1 ([[link|example]]).", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternPipeLink.sub(r"\g<1>", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
                
        #    Step 2: Stuff of the form [[example]] should become example
        if verbose:
            print colored("Entering link conversion of type 2 ([[example]]).", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternLink.sub(r"\g<1>", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #Replaces the circa environment with text describing the approximate date.
        if verbose:
            print colored("Entering replacement of circa environment.", "blue")
            print "    Value before was: '%s'" % str(value)
        circaEnvironments = self.patternIdentifyCirca.findall(value)
        for i in range(len(circaEnvironments)):
            match = filter(None, list(itertools.chain.from_iterable(self.patternCirca.findall(circaEnvironments[i]))))
            if len(match) == 1:
                replacementValue = "c. " + match[0]
            elif len(match) == 2:
                replacementValue += "-" + match[1]
            else:
                print colored("WARNING: Illegal circa statement detected!", "magenta")
                for i in range(len(circaEnvironments)):
                    print "    More specifically: " + circaEnvironments[i]
            value = self.patternIdentifyCirca.sub(replacementValue, value, 1)
            
        #Replaces the marriage environment with text describing the marriage in
        #natural language.
        if verbose:
            print colored("Entering replacement of marriage environment.", "blue")
            print "    Value before was: '%s'" % str(value)
        marriageEnvironments = self.patternIdentifyMarriage.findall(value)
        for i in range(len(marriageEnvironments)):
            match = filter(None, list(itertools.chain.from_iterable(self.patternMarriage.findall(marriageEnvironments[i]))))
            replacementValue = match[0] + " "
            if len(match) == 2:
                replacementValue += "(m. " + match[1] + ")"
            elif len(match) == 3:
                replacementValue += "(m. " + match[1] + "-" + match[2] + ")"
            else:
                print colored("WARNING: Illegal marriage detected!", "magenta")
            value = self.patternIdentifyMarriage.sub(replacementValue, value, 1)

        if verbose:
            print "    Value after became: '%s'" % str(value)
            
        #    Removal of the "Longitem" environment
        if verbose:
            print colored("Entering removal of 'Longitem' and 'nowrap' environments.", "blue")
            print "    Value before was: '%s'" % str(value)
        value = self.patternLongitem.sub(r"\g<1>", value)
        if verbose:
            print "    Value after became: '%s'" % str(value)
        
        #Replace nested hlists in start-tag end-tag lists
        if value.endswith("{{endplainlist}}") or value.endswith("{{endflowlist}}") or value.endswith("{{endflatlist}}"):
            #1. Find out what the list is delimited by (#, | or *)
            hlistEnvironments = self.patternIdentifyHlist.findall(value)
            if len(hlistEnvironments) > 0:
                if "#" in value:
                    #Sub all groups in match into #- separated string
                    for i in range(len(hlistEnvironments)):
                        match = filter(None, list(itertools.chain.from_iterable(self.patternHlist.findall(hlistEnvironments[i]))))
                        if len(match) > 0:
                            replacementValue = " # ".join(match)
                        else:
                            print colored("WARNING: Empty hlist statement detected!", "magenta")
                            replacementValue = ""
                        value = self.patternIdentifyHlist.sub(replacementValue, value, 1)
                elif "*" in value:
                    #Sub all groups in match into *- separated string
                    for i in range(len(hlistEnvironments)):
                        match = filter(None, list(itertools.chain.from_iterable(self.patternHlist.findall(hlistEnvironments[i]))))
                        if len(match) > 0:
                            replacementValue = " * ".join(match)
                        else:
                            print colored("WARNING: Empty hlist statement detected!", "magenta")
                            replacementValue = ""
                        value = self.patternIdentifyHlist.sub(replacementValue, value, 1)
                else: #List must be |-separated then...
                    #Sub all groups in match into |- separated string
                    for i in range(len(hlistEnvironments)):
                        match = filter(None, list(itertools.chain.from_iterable(self.patternHlist.findall(hlistEnvironments[i]))))
                        if len(match) > 0:
                            replacementValue = " | ".join(match)
                        else:
                            print colored("WARNING: Empty hlist statement detected!", "magenta")
                            replacementValue = ""
                        value = self.patternIdentifyHlist.sub(replacementValue, value, 1)
            
        return value
    
    def parseList(self, value, listType, verbose=False):
        """Parses a list from a string - this is presumed to be a string
        containing onyl one list. If you do not clean the string thoroughly
        before feeding them to this function, you might encounter strange
        behaviour.
        
        Arguments: A string with a list in Wiki markup to be parsed to a
        list of strings.
        
        Return value: A list of strings.
        """
        
        #Since we are in a list, we want to replace the <br />s with
        #whitespaces. TODO: Really?
        if verbose:
            print "    Entering removal of <br />s, since we have discovered a list."
            print "        Value before was: '%s'" % str(value)
        value = self.patternBr.sub(r" ", value)
        
        if verbose:
            print "        Value after became: '%s'" % str(value)
        
        #Now that we have obtained the list type, we want to do different things depending on which list type it is.
        if self.patternBulletedListName.match(listType):
            if verbose:
                print '    "bulleted list" detected.'

            #Returns a list of tuples with all matches, where each group corresponds to one tuple.
            returnList = filter(None, list(itertools.chain.from_iterable(self.patternBulletedList.findall(value))))
            
        elif self.patternFlatlistName.match(listType):
            if verbose:
                print '    "flatlist" detected.'
            #Note: We do NOT need to have a subcase for endflatlist environment, since that is initiated by {{startflatlist}}
            returnList = filter(None, list(itertools.chain.from_iterable(self.patternFlatlist.findall(value))))
            
        elif self.patternStartflatlistName.match(listType):
            if verbose:
                print '    "startflatlist" detected.'
            
            #Returns a list of tuples with all matches, where each group corresponds to one tuple.
            returnList = filter(None, list(itertools.chain.from_iterable(self.patternStartflatlist.findall(value))))
            
        elif self.patternPlainlistName.match(listType):
            if verbose:
                print '    some type of plainlist detected...'
            #A subcase for endplainlist/startplainlist environment:
            if value.endswith("{{endplainlist}}"):
                if verbose:
                    print '    "endplainlist" detected.'
                returnList = filter(None, list(itertools.chain.from_iterable(self.patternEndplainlist.findall(value))))
            else:
                if verbose:
                    print '    "plainlist" detected.'
                returnList = filter(None, list(itertools.chain.from_iterable(self.patternPlainlist.findall(value))))
        
        elif self.patternFlowlistName.match(listType):
            if verbose:
                print '    some type of flowlist detected...'
            #A subcase for endflowlist environment:
            if value.endswith("{{endflowlist}}"):
                if verbose:
                    print '    "endflowlist" detected'
                returnList = filter(None, list(itertools.chain.from_iterable(self.patternEndflowlist.findall(value))))
            else:
                if verbose:
                        print '    "flowlist" detected.'
                returnList = filter(None, list(itertools.chain.from_iterable(self.patternFlowlist.findall(value))))
            
        elif self.patternUnbulletedListName.match(listType):
            if verbose:
                print '    "unbulleted list" detected.'

            #Returns a list of tuples with all matches, where each group corresponds to one tuple.
            returnList = filter(None, list(itertools.chain.from_iterable(self.patternUnbulletedList.findall(value))))
            
        elif self.patternPagelistName.match(listType):
            if verbose:
                print '    "pagelist" detected.'

            #Returns a list of tuples with all matches, where each group corresponds to one tuple.
            returnList = filter(None, list(itertools.chain.from_iterable(self.patternPagelist.findall(value))))
            
        elif self.patternOrderedListName.match(listType):
            if verbose:
                print '    "ordered list" detected.'

            #Returns a list of tuples with all matches, where each group corresponds to one tuple.
            returnList = filter(None, list(itertools.chain.from_iterable(self.patternOrderedList.findall(value))))
            
        elif self.patternToolbarName.match(listType):
            if verbose:
                print '    "toolbar" detected.'

            #Returns a list of tuples with all matches, where each group corresponds to one tuple.
            returnList = filter(None, list(itertools.chain.from_iterable(self.patternToolbar.findall(value))))
                  
        elif self.patternHlistName.match(listType):
            if verbose:
                print '    "hlist" detected.'

            #Returns a list of tuples with all matches, where each group corresponds to one tuple.
            returnList = filter(None, list(itertools.chain.from_iterable(self.patternHlist.findall(value))))
        else:
            if verbose:
                print colored("WARNING: List of unknown type found!", "magenta")  
            returnList = ""
            
        returnList = self.concatenateParenthesesEnclosedEntries(returnList, verbose)
  
        return returnList
        
        
    def parseAttributeValue(self, value, verbose=False, logFileName=None):
        """Takes an attribute value as a string in un-edited Wiki markup format 
        and parses it into either a string value or a tuple of string values.
        
        Arguments:
        If verbose is True, current operations will be printed
        If logFileName is a string, anything happenening (including errors)
            will be logged to the filename logFileName.
        
        Return value:
        If no value was found, "" is returned.
        If the value is not considered to be relevant text, ""  is returned.
        
        Examples:
        value = "{{br separated values|entry1|entry2}}"
        parseAttributeValue(value) == (entry1, entry2)

        value = "Germany"
        parseAttributeValue(value) == "Germany"

        value = "Barack Obama signature.svg"
        parseAttributeValue(value) == ""
        """
        
        if verbose:
            print "\nPARSE OF ATTRIBUTE VALUE INITIATED"
        
        #Do initial parsing
        value = self.initialParsing(value, verbose)
        
        #Now that we're done with that, we want to check if the attribute value
        #is a list.
        if verbose:
            print colored("Entering check for attribute value being a list...", "blue")
        match = self.patternList.match(value) #We can actually use match since we are only explicitly looking for matches at the beginning.
        
        if match:
            if verbose:
                print "List detected."
            #TODO: Get all list types here. Loop through them all and merge them
            #to one long list, then return.
            resultList = []
            subStrings = self.patternListNoCatchGroups.findall(value)
            #TEST: Lots of prints here:
            #print "Number of substrings in " + str(value.encode("utf-8")) + " is " + str(len(subStrings))
            #for string in subStrings:
            #    print "Value is: " + value
            #    print "String is: " + string
            for i, listType in enumerate(self.patternList.findall(value)):
                #print "List type is: " + listType
                if i == len(subStrings):
                    print colored("WARNING: Degenerate list environment found!", "magenta")
                    return resultList
                if listType not in ["endflatlist", "endplainlist", "endflowlist"]:
                    resultList.extend(self.parseList(subStrings[i], listType, verbose))
            #print "Entire string was parsed..."    
            if verbose:
                print "Returning: %s" % str(resultList) 
            return resultList    
        else:
            #No list was found... Check if the attribute value is
            #<br />-separated or dot ({{.}})-separated. If that is the case, split it using that as a
            #separator. Otherwise, return the value as it is.
            
            #Remove everything on the right of first pipe, to compensate for bad Wikipedia formatting
            if verbose:
                print colored("Entering removal of right-of-pipe elements.", "blue")
                print "    Value before was: '%s'" % str(value)
            value = self.patternRightOfPipe.sub(r"", value)
            if verbose:
                print "    Value after became: '%s'" % str(value)

            #Delete the entry if it starts with a #
            if verbose:
                print colored("Entering removal of #-prepended entries", "blue")
                print "    Value before was: '%s'" % str(value)
            value = self.patternStartsWithSquare.sub(r"", value)
            if verbose:
                print "    Value after became: '%s'" % str(value)
            
            #Remove eventual curly brackets at end
            if verbose:
                print colored("Entering removal of curly brackets.", "blue")
                print "    Value before was: '%s'" % str(value)
            value = self.patternCurlyBrackets.sub(r"", value)
            if verbose:
                print "    Value after became: '%s'" % str(value)

            if "<br />" in value or "<br/>" in value or "<br>" in value:
                if verbose:
                    print 'Attribute value is a list separated by <br />.'
                value = filter(None, self.patternBr.split(value))
                value = self.concatenateParenthesesEnclosedEntries(value, verbose)
                if verbose:
                    print "Returning '%s'" % str(value)
            else:
                #Checking for dot-separated lists
                if verbose:
                    print colored("Entering check for lists separated by dots.", "blue")
                    print "    Value before was: '%s'" % str(value)
                match = self.patternDot.search(value)
                if match:
                    value = filter(None, self.patternDot.split(value))
                    value = self.concatenateParenthesesEnclosedEntries(value, verbose)
                if verbose:
                    print "    Value after became: '%s'" % str(value)
                else:
                    if verbose:
                        print 'No list was found in attribute value.'
                        print "Returning '%s'" % str(value)
            return value
        
        
def test(verbose=False):
    """Tests the functionality of attribute_value_paser. Will crash with an
    AssertionError if something is not working correctly.
    
    Arguments:
    If verbose is True, current operations will be printed.
    """
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
        ('{{plainlist}}* [[These   ]]* [[not visible | wonky   ]]* [[lists]]* are   * [[hard]]* [[to]]* [[you cant see me|parse]] {{endplainlist}}',['These','wonky','lists','are','hard','to','parse']),
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
        ('[[Milan|Mediolanum]],<br />[[Italy (Roman Empire)|Italia annonaria]], [[Roman Empire]]<br />''[[Italy|(present-day Italy)]]''', ['Mediolanum, Italia annonaria, Roman Empire (present-day Italy)']),
        #Nested and/or multiple lists
        ('{{hlist|[[biology]]|[[zoology]]}} {{hlist|[[physics]]|[[metaphysics]]}}', ['biology', 'zoology', 'physics', 'metaphysics']),
        ('{{startplainlist|classnowrap}}* {{hlist |Medicine |Aromatherapy}}* Philosophy and logic* ''Kalam'' (Islamic theology)* {{hlist |Science |Poetry}}{{endplainlist}}', ['Medicine', 'Aromatherapy', 'Philosophy and logic', 'Kalam (Islamic theology)', 'Science', 'Poetry']),
        #Misc.
        ('{{c.|980}} [[Common Era|CE]]','c. 980 CE')
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
