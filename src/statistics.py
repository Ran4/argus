import sys
import os
import json
import collections
from collections import Counter
from pprint import pprint as pp
from operator import itemgetter, attrgetter

from termcolor import colored
import logger

class Statistics:
    def __init__(self, JSONFileName, statisticsOutputFileName, verbose):
        self.verbose = verbose
        self.statisticsOutputFileName = statisticsOutputFileName
        try:
            with open(JSONFileName) as jsonFile:
                self.JSONLists = json.load(jsonFile)
                self.j = self.JSONLists
        except:
            print colored("Statistics failure: couldn't load JSON file '%s'" %\
                JSONFileName, "yellow")
            sys.exit()
            
        #Clear statistics output file
        with open(self.statisticsOutputFileName, "w") as f:
            f.write("")
            
        print "Loaded JSON and emptied statistics output file (%s)" % \
            self.statisticsOutputFileName
            
    def statOutput(self, s, verboseOverride=None):
        if verboseOverride is not None:
            verbose = verboseOverride
        else:
            verbose = self.verbose
        
        if verbose:
            print s
        logger.writeToFile(s.encode("utf-8"), self.statisticsOutputFileName)
    
    
    def doStatistics(self):
        mostCommonFormat = self.mostCommonFormat
        
        ##
        
        self.commonNames = self.commonNameSubStringsCounter().most_common(100)
        self.statOutput("Most common name substrings: %s" % mostCommonFormat(
            self.commonNames))
        
        ##
        lastLetters = []
        for pageDict in self.j:
            for value in pageDict.values():
                if isinstance(value, unicode):
                    lastLetters.append(value[-1])
            
        print "len(lastLetters):", len(lastLetters)
        
        self.lastLetterInValueStats = []
        for char in "abcdefghijklmnopqrstuvwxyz":
            self.lastLetterInValueStats.append((char, lastLetters.count(char)))
            
        self.statOutput("Most common last letters: %s" % mostCommonFormat(
            self.lastLetterInValueStats))
            
        ##
        deathDates = self.getAllValues(key="death_date", expandLists=False)
        #print "len(deathDates):", len(deathDates)
        
        #http://pastebin.com/9rHnQZkH
        
        ##
        
        for key in ["salary", "known_for"]:
            values = self.getAllValues(key=key, expandLists=True)
            s = "####Found %s values with the key '%s'" % (len(values), key)
            self.statOutput(s, verboseOverride=True)
            if self.verbose: print colored(s, "white")
            if self.verbose: print "Values:", map(lambda x: x.encode("utf-8"), values)
            self.statOutput("\n".join(values), verboseOverride=False)
            
            s = "####End of %s" % key
            self.statOutput(s, verboseOverride=False)
            if self.verbose: print colored(s, "white")
        
        ##
        
    def doPlots(self, showPlots=True):
        import matplotlib.pyplot as plt #use matplotlib to plot stuff
        opj = os.path.join
        plotFileOutputPath = os.path.abspath("../stats/plots/")
        
        if self.verbose: print "Plotting started..."
        #################################################################
        
        
        if self.verbose: print "  Plotting most common names value"
        ##Example: self.commonNames = [("john", 1877), ("william", 987)]
        commonNamesValues = map(itemgetter(1), self.commonNames)
        xx = range(len(commonNamesValues))
        plt.plot(xx, commonNamesValues)
        if showPlots: plt.show()
        
        
        if self.verbose: print "  Plotting most common last letter of values"
        commonLastLetterValues = map(itemgetter(1), self.lastLetterInValueStats)
        xx = range(len(commonLastLetterValues))
        plt.plot(xx, commonLastLetterValues)
        if showPlots: plt.show()
        
        
        #################################################################
        if self.verbose: print "Plotting complete!"
            
    def mostCommonFormat(self, mostCommonList):
        return ", ".join(map(lambda x: "%s (%s)" % x, mostCommonList))
    
    def getAllValues(self, ofType=None, key=None, expandLists=True):
        retValues = []
        for pageDict in self.j:
            for pageDictKey in pageDict:
                value = pageDict[pageDictKey]
                if key is not None and pageDictKey != key:
                    continue
                
                if isinstance(value, unicode):
                    retValues.append(value)
                else:
                    if expandLists:
                        retValues += value
        
        return retValues
                    
    
    def getAllValuesWithKey(self, key, ofType=None):
        if ofType is None:
            return [pageDict[key] for pageDict in self.j
                if key in pageDict]
        else:
            return [pageDict[key] for pageDict in self.j
                if key in pageDict \
                    and isinstance(pageDict[key], ofType)]
        
    def commonNameSubStringsCounter(self):
        j = self.j
        for pageDict in j:
            nameSubStrings = []
            for nameSubString in [val.split() for val in self.getAllValuesWithKey("name", unicode)
                    if len(val) <= 80]: #Don't take name values that are too long
                for subString in nameSubString:
                    if subString in ["the", "of"]:
                        continue
                    nameSubStrings.append(subString)
            
            return Counter(nameSubStrings)
            

def main(showPlots):
    #Handle arguments
    args = map(lambda x: x.lower(), sys.argv[1:])
    
    if len(args) == 0:
        print "Usage: statistics.py [silent] [noplot] [noshow]"
    
    verbose = True
    if "--silent" in args or "-s" in args or any("silent" in arg for arg in args):
        verbose = False
        
    noPlots = False
    if any("noplot" in arg for arg in args):
        noPlots = True
        
    if any("noshow" in arg for arg in args):
        showPlots = False
    
    #Start running statistics
    
    statisticsOutputFileName = os.path.abspath("../stats/statistics_output.txt")
    
    hugeFileFileName = os.path.abspath("../output/infobox_output_cleaned_150518.json")
    if os.path.isfile(hugeFileFileName):
        print "Found huge file '%s', using that..." % hugeFileFileName
        JSONFileName = hugeFileFileName
    else: #Open smaller version instead
        JSONFileName = os.path.abspath("../output/infobox_output_cleaned.json")
        print "Uses smaller file '%s'" % JSONFileName
    
    print "Statistics will be written to file '%s'" % statisticsOutputFileName
    s = Statistics(JSONFileName, statisticsOutputFileName, verbose)
    
    s.doStatistics()
    if not noPlots:
        s.doPlots(showPlots)
        
    print colored("Done with statistics.py", "green")

if __name__ == "__main__":
    main(showPlots=True)
    
