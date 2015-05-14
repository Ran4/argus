import time
from pprint import pprint as pp
from collections import Counter

global atLine

class InfoBox(object):
    def __init__(self, articleTitle, infoBoxType, infoBoxStringList):
        self.articleTitle = articleTitle
        self.infoBoxType = infoBoxType
        self.infoBoxStringList = infoBoxStringList
        
        if len(self.infoBoxType) > 30:
            #there might be a problem since the type string is so long!
            self.handleLongInfoBoxType(verbose=False)
    
    def handleLongInfoBoxType(self, verbose=True):
        """If the infoBoxType string is really long, chances are
        that something is wrong. Tries to fix it a little bit.
        """
        if verbose:
            print "There might be a problem with infobox '%s...'" % \
                self.infoBoxType[:30],
            print "(%s characters omitted)'" % (len(self.infoBoxType) - 30)
        
        if "|" in self.infoBoxType:
            self.infoBoxType = self.infoBoxType.split("|")[0].strip()
        if "&lt;" in self.infoBoxType:
            self.infoBoxType = self.infoBoxType.split("&lt;")[0].strip()
            
        if verbose:
            print "Cutoff after first '|' or '&lt;' gives new infoBoxType: '%s'"%\
                self.infoBoxType
            
    def __str__(self):
        s = "<infobox object. Article'=%s', Type='%s'. %s lines of content>" % \
            (self.articleTitle,
            self.infoBoxType,
            len(self.infoBoxStringList))
            
        return s
        
    def getPropertiesDict(self):
        """Returns a dictionary of properties of the infobox
        """
        propertiesDict = {}
        for line in self.infoBoxStringList:
            keyValue = _parseKeyValue(line)
            if keyValue:
                propertiesDict[key] = value
                
        return propertiesDict
        
    def _parseKeyValue(self, line):
        """Gets the key and value from an infobox line,
        as lowercase characters
        '| NAME                  = Lee Aaker ' -> ("name", "lee aaker")
        """
        if not line.startswith("| ") or "=" not in line:
            return None
            
        eqSplit = line.split("=")
        key = eqSplit[0][len("| "):].strip().lower()
        value = "".join(eqSplit[1:]).strip().lower()
        
        return (key, value)
        
    def getTSVLines(self):
        wikiUrl = 'http://en.wikipedia.org/wiki/' + \
            self.articleTitle.replace(" ", "_")
        isoCode = "en"
        tsvLines = []
        
        #slow
        #~ for key, value in self.getPropertiesDict():
            #~ tsvLines.append("%s\t%s\t%s\t%s" % (wikiUrl, key, value, isoCode))
        
        #faster
        for key, value in filter(None,
                map(self._parseKeyValue, self.infoBoxStringList)):
            tsvLines.append("%s\t%s\t%s\t%s" % (wikiUrl, key, value, isoCode))
        return tsvLines
        
        #fastest?
        #~ return ["%s\t%s\t%s\t%s" % (wikiUrl, key, value, isoCode) 
            #~ for key, value in filter(
                #~ None, map(self._parseKeyValue, self.infoBoxStringList))]

def getInfoBoxGenerator(f, seekStart=0, requestedNumberOfInfoBoxes=1e99):
    """Generator that takes a file object for the xml of a wikipedia stream,
    and yields an infoBoxObject.
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
    infoBoxType = ""
    numArticlesFound = 0
    numInfoBoxesFound = 0
    while True:
        line = f.readline()
        atLine += 1
        
        if line == "</mediawiki>":
            print "</mediawiki> found at line %s (tell=%s), filereading stops"\
                % (atLine, f.tell())
            break
            
        if numInfoBoxesFound >= requestedNumberOfInfoBoxes:
            print "Found requested number of infoboxes, filereading stops"
            break
        
        if "<page>" in line:
            record = True
        
        if not record:
            continue
            
        recordList.append(line)
        
        if line.startswith("{{Infobox"):
            recordInfoBox = True
            infoBoxType = line[len("{{Infobox")+1:-1]
            
        if recordInfoBox:
            recordInfoBoxList.append(line)
            
            #~ print "in recordInfoBox, line: '%s'" % line
            if line == "}}\n":
                recordInfoBox = False
                
                page = "".join(recordList)
                title = page[page.find("<title>") + len("<title>"):
                    page.find("</title>")]
                    
                numInfoBoxesFound += 1
                yield InfoBox(title, infoBoxType, recordInfoBoxList)
                #yield None
                recordInfoBoxList = []
        
        if "</page>" in line:
            record = False
            numArticlesFound += 1
            
            page = "".join(recordList)
            title = page[page.find("<title>") + len("<title>"):
                page.find("</title>")]
                
            recordList = []
    
    print "Succesfully finished parsing the entire wikipedia!"
        
def uglyLog(s, fileName="log.txt"):
    """Appends a string to a file... yeah.
    """
    try:
        fileName = fileName
        with open(fileName, "a") as logFile:
            logFile.write(s)
    except:
        print "Error saving to logfile"

def main():
    fileName = "enwiki-20150304-pages-articles-multistream.xml"
    filePath = "C:\\ovrigt\\ovrigt\\wp\\" + fileName
    f = open(filePath)
    
    with open("log.txt", "w") as logFile: #reset file
        logFile.write("")
    with open("output.tsv", "w") as logFile: #reset file
        logFile.write("")
        
    infoBoxTypeCounter = Counter()
    
    ibGenerator = getInfoBoxGenerator(f)
    
    print "Parsing is started..."
    
    ibsGotten = 0
    startTime = time.time()
    while True:
        try:
            ib = ibGenerator.next()
            ibsGotten += 1
            
            infoBoxTypeCounter[ib.infoBoxType.lower()] += 1
            
            if "person" in ib.infoBoxType:
                uglyLog("\n".join(ib.getTSVLines()), "output.tsv")
                
            ##debug stuff
            #~ if infoBoxTypeCounter[ib.infoBoxType.lower()] == 1:
                #found new one!
                #~ print ib.infoBoxType
            
            #~ print "".join(ib.infoBoxStringList)
            #~ print "\n"*3
            
            #Continously write some information about our efforts
            if ibsGotten % 10000 == 0:
                dt = time.time() - startTime
                prc = 100.0 * float(atLine) / 810000000
                est = (dt/(prc/100))
                left = est - dt
                
                #~ s = "%s infoBoxes generated in %.1f minutes, " % \
                    #~ (ibsGotten, dt/60.0)
                s = "%sk generated infoBoxes. " % (ibsGotten/1000)
                s += "line=%s (%.1fprc,left=%dm), " % (atLine, prc, left/60)
                s += "%.1f ib's/s" % (ibsGotten/dt)
                
                uglyLog(s+"\n")
                print(s)
            
            
            #just showing some statistics on most common infoBoxTypes after 
            #we've gotten some progress
            if ibsGotten == 285000:
                items = infoBoxTypeCounter.items()
                items.sort(key=lambda x: x[1], reverse=True)
                
                for item in items:
                    if "person" in item[0]:
                        print item[1], item[0]
                
        except StopIteration:
            print "StopIteration reached!"
            dt = time.time() - startTime
            s = "Done generating."
            s += "Generated %s infoboxes, taking %d seconds (=%.1f minutes)" % \
                (ibsGotten, dt, dt/60.0)
            s += " at an average of %.1f articles per second" % \
                (ibsGotten/dt)
                
            uglyLog(s)
            print(s)
            
            break

if __name__ == "__main__":
    main()
