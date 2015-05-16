import sys
import time
from pprint import pprint as pp
from collections import Counter
import json

import logger
from logger import writeToFile

global atLine

class InfoBox(object):
    """Helpful object which stores all the information in an InfoBox
    args:
    articleTitle - string
    infoBoxType - the 'type' of infobox. E.g. "{{Infobox militaryperson"
        has infoboxType="militaryperson"
    infoBoxStringList - a list of strings, each being a line in the InfoBox
    countInArticle - the n'th InfoBox found in an article
    """
    def __init__(self, articleTitle, infoBoxType, infoBoxStringList,
            countInArticle):
        self.articleTitle = articleTitle
        self.infoBoxType = infoBoxType
        self.infoBoxStringList = infoBoxStringList
        self.countInArticle = countInArticle
        
        self.isInArticleWithPersonBox = False
        
        """
        if "lincoln" in articleTitle.lower() and "abraham" in articleTitle.lower():
            print "in InfoBox.__init__ of title=%s" % articleTitle
            print "infoBoxStringList:", self.infoBoxStringList
            
            print "JSON:"
            print self.getJSON()
            print "\n"*2
        """    
        
        if len(self.infoBoxType) > 30:
            #There might be a problem since the type string is so long!
            self.handleLongInfoBoxType(verbose=False)
    
    def handleLongInfoBoxType(self, verbose=True):
        """If the infoBoxType string is really long, chances are
        that something is wrong. Tries to fix it a little bit.
        """
        if verbose:
            print "There might be a problem with infobox '%s...'" % \
                self.infoBoxType[:30],
            print "(%s characters omitted)'" % (len(self.infoBoxType) - 30)
        
		#If there's a pipe in the infoBoxType, store what can be
                #    found before the pipe
        if "|" in self.infoBoxType:
            self.infoBoxType = self.infoBoxType.split("|")[0].strip()
		#If there's a "<" sign, this means we have discovered a comment.
                #Store what can be found before the comment.
        if "&lt;" in self.infoBoxType:
            self.infoBoxType = self.infoBoxType.split("&lt;")[0].strip()
        
		#TODO: Will this always be displayed if verbose,
                #    even if nothing has been cut off?
        if verbose:
            print "Cutoff after first '|' or '&lt;' gives new infoBoxType: '%s'"%\
                self.infoBoxType
            
    def __str__(self):
        """Returns a representation of the infobox as a string.
        """
        s = "<infobox object. Article'=%s', Type='%s'. %s lines of content>" % \
            (self.articleTitle,
            self.infoBoxType,
            len(self.infoBoxStringList))
            
        return s
        
    def getPropertiesDict(self, verbose=False):
        """Returns a dictionary of properties of the infobox.
        """
        propertiesDict = {}
        for line in self.infoBoxStringList:
            keyValue = self._parseKeyValue(line)
            if keyValue:
                key, value = keyValue
                propertiesDict[key] = value
                
            if verbose:
                print "Parsed attribute: %s -> %s" % (line.strip(), keyValue)
                
        return propertiesDict
        
    def _parseKeyValue(self, line):
        """Gets the key and value from an infobox line,
        as lowercase characters
        Examples:
        '| NAME                  = Lee Aaker ' -> ("name", "lee aaker")
        '|NAME                  = Lee Aaker ' -> ("name", "lee aaker")
        """
        
        if not line.startswith("|") or "=" not in line:
            return None
            
        eqSplit = line.split("=")
        if line[1] == " ": #attribute started with '| '
            key = eqSplit[0][len("| "):].strip().lower()
        else: #attribute started with '|'
            key = eqSplit[0][len("|"):].strip().lower()
        value = "".join(eqSplit[1:]).strip().lower()
        
        return (key, value)
        
    def getJSON(self, indent=None):
        """Gets the attribute key/values plus the wikipedia url,
        isoCode, and if it's the first infobox in an article that has a 
        personbox as a JSON string.
        """
        wikiUrl = 'http://en.wikipedia.org/wiki/' + \
            self.articleTitle.replace(" ", "_")
        isoCode = "en"
        
        d = self.getPropertiesDict()
        d["wikiURL"] = wikiUrl
        d["isoCode"] = isoCode
        if self.isInArticleWithPersonBox and self.countInArticle == 0:
            d["isFirstInArticleWithPersonBox"] = "1"
        else:
            d["isFirstInArticleWithPersonBox"] = "0"
            
        if indent is None:
            return json.dumps(d, indent=4)
        else:
            return json.dumps(d, indent=indent)
    
def getInfoBoxGenerator(f, seekStart=0, requestedNumberOfInfoBoxes=1e99):
    """Generator that takes a file object for the xml of a wikipedia stream,
    and yields a list of infoBoxObject.
    The list returned is all the infoboxes in an article
    
    If requestedNumberOfInfoBoxes is given, only returns up to that many
    article's worth of infoboxes
    """
    record = False
    recordList = []
    pageList = []

    global atLine
    atLine = -1
    
    """
    line 810.000.000 <=> byte 50974096816
    The end of the file is some time after byte 52008028665
    """
    #f.seek(50974096816) #near end, around 17040 infoboxes left
    
    recordInfoBox = False
    recordInfoBoxList = []
    infoBoxList = []
    infoBoxType = ""
    numArticlesFound = 0
    numInfoBoxesFound = 0
    isInArticleWithPersonBox = False
    infoBoxNumber = 0
    while True:
        line = f.readline()
        atLine += 1
        
		#TODO: What is mediawiki??????
        if line == "</mediawiki>":
            print "</mediawiki> found at line %s (tell=%s), filereading stops"\
                % (atLine, f.tell())
            break
            
        if numInfoBoxesFound > requestedNumberOfInfoBoxes:
            print "Found requested number of infoboxes, filereading stops"
            break
        
        if "<page>" in line: #start of an article
            record = True
            
        ####################
        # Handle <page>
        
        if not record:
            continue
            
        recordList.append(line)
        
        if line.startswith("{{Persondata"):
            isInArticleWithPersonBox = True
        
        if line.startswith("{{Infobox"):
            recordInfoBox = True
            infoBoxType = line[len("{{Infobox")+1:-1]
            
        if recordInfoBox: #We are currently inside of an infobox
            recordInfoBoxList.append(line)
            
            #~ print "in recordInfoBox, line: '%s'" % line
			#TODO: Lines must only end in these formats. These might not be separate lines.
            if line == "}}\n" or line == "|}}\n": #Found end of InfoBox
                recordInfoBox = False
                
                page = "".join(recordList)
                title = page[page.find("<title>") + len("<title>"):
                    page.find("</title>")]
                    
                numInfoBoxesFound += 1
                ib = InfoBox(title, infoBoxType, recordInfoBoxList,
                        infoBoxNumber)
                infoBoxList.append(ib)
                
                recordInfoBoxList = []
                infoBoxNumber += 1
            
        # End of handle <page>
        ####################
        
        if "</page>" in line: #end of an article
            record = False
            numArticlesFound += 1
            infoBoxNumber = 0 
            
            page = "".join(recordList)
            title = page[page.find("<title>") + len("<title>"):
                page.find("</title>")]
                
            recordList = []
        
            if isInArticleWithPersonBox:
                for ib in infoBoxList:
                    ib.isInArticleWithPersonBox = isInArticleWithPersonBox
                
            yield infoBoxList
            
            isInArticleWithPersonBox = False
            infoBoxList = []
    
    print "Successfully finished parsing the entire Wikipedia!"
        
def handleInfoBoxes(ibList, outputFileName):
    for ib in ibList:
        #infoBoxTypeCounter[ib.infoBoxType.lower()] += 1
        
        if (ib.isInArticleWithPersonBox and ib.countInArticle == 0) or\
            "person" in ib.infoBoxType:
            writeToFile(ib.getJSON(indent=2)+"\n", outputFileName)
            #print "Got articleInfoBox:"
            #print ib.getJSON()
            #print "\n"*2
        
        
        """
        if "person" in ib.infoBoxType:
            writeToFile("\n".join(ib.getTSVLines()), "output.tsv")
        """
            
        ##debug stuff
        #~ if infoBoxTypeCounter[ib.infoBoxType.lower()] == 1:
            #found new one!
            #~ print ib.infoBoxType
        
        #~ print "".join(ib.infoBoxStringList)
        #~ print "\n"*3

def main():
    if len(sys.argv) > 1:
        filePath = sys.argv[1]
    else:
        fileName = "enwiki-20150304-pages-articles-multistream.xml"
        filePath = "C:\\ovrigt\\ovrigt\\wp\\" + fileName
        
    f = open(filePath)
    
    outputFileName = "ibs_person_raw.json"
    
    with open(logger.defaultFileName, "w") as logFile: #reset file
        logFile.write("")
    with open(outputFileName, "w") as logFile: #reset file
        logFile.write("")
        
    infoBoxTypeCounter = Counter()
    
    #ibGenerator = getInfoBoxGenerator(f)
    ibGenerator = getInfoBoxGenerator(f, requestedNumberOfInfoBoxes=80000)
    
    print "Parsing from file '%s' is started..." % filePath
    writeToFile("[\n", outputFileName)
    print "Output file: '%s'" % outputFileName
    
    ibsGotten = 0
    articlesGotten = 0
    startTime = time.time()    
    while True:
        try:
            ibList = ibGenerator.next()
            
            handleInfoBoxes(ibList, outputFileName)
            
            ibsGotten += len(ibList)
            articlesGotten += 1 
                
            #Continuously write some information about our efforts...
            
            if articlesGotten % 50 == 0:
                dt = time.time() - startTime
                
                #Percent of wikipedia read
                prc = 100.0 * float(atLine) / 810000000
                est = (dt/(prc/100)) #Estimated time remaining in seconds
                left = est - dt
                
                #~ s = "%s infoBoxes generated in %.1f minutes, " % \
                    #~ (ibsGotten, dt/60.0)
                s = "%sk generated infoBoxes. " % (ibsGotten/1000)
                s += "line=%s (%.1fprc,left=%dm), " % (atLine, prc, left/60)
                s += "%.1f ib's/s" % (ibsGotten/dt)
                
                dateStr = time.strftime("%y%m%d_%H:%M.%S ")
                
                writeToFile(dateStr + s + "\n")
                print(s)
            
            
            #just showing some statistics on most common infoBoxTypes after 
            #we've gotten some progress
            """
            if articlesGotten == 105000: #ibsGotten == 285000:
                items = infoBoxTypeCounter.items()
                items.sort(key=lambda x: x[1], reverse=True)
                
                for item in items:
                    if "person" in item[0]:
                    print item[1], item[0]
            """
                
        except StopIteration:
            print "StopIteration reached!"
            dt = time.time() - startTime
            s = "Done generating."
            s += "Generated %s infoboxes, taking %d seconds (=%.1f minutes)" % \
                (ibsGotten, dt, dt/60.0)
            s += " at an average of %.1f articles per second" % \
                (ibsGotten/dt)
                
            writeToFile("]", outputFileName)
                
            writeToFile(s, "log.txt")
            print(s)
            
            
            
            break
            
    

if __name__ == "__main__":
    main()
