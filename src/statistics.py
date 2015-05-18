import sys
import os
import json
import collections
from collections import Counter
from pprint import pprint as pp
from operator import itemgetter, attrgetter

from termcolor import colored
import logger

statisticsOutputFileName = os.path.abspath(
    "../stats/statistics_output.txt")

class Statistics:
    def __init__(self, JSONFileName, verbose):
        self.verbose = verbose
        try:
            with open(JSONFileName) as jsonFile:
                self.JSONLists = json.load(jsonFile)
                self.j = self.JSONLists
        except:
            print colored("Statistics failure: couldn't load JSON file '%s'" %\
                JSONFileName, "yellow")
            sys.exit()
            
        #Clear statistics output file
        with open(statisticsOutputFileName, "w") as f:
            f.write("")
            
        print "Loaded JSON and emptied statistics output file (%s)" % \
            statisticsOutputFileName
            
    def statOutput(self, s):
        if self.verbose:
            print s
        logger.writeToFile(s.encode("utf-8"), statisticsOutputFileName)
    
    
    
    
    def doStatistics(self):
        mostCommonFormat = self.mostCommonFormat
        
        ##
        
        self.commonNames = self.commonNameSubStringsCounter().most_common(50)
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
        print "len(deathDates):", len(deathDates)
        
        global deathDates
        exit()
        
        ##
        
        
    def doPlots(self, showPlots=True):
        import matplotlib.pyplot as plt #use matplotlib to plot stuff
        opj = os.path.join
        plotFileOutputPath = os.path.abspath("../stats/plots/")
        
        if self.verbose: print "Plotting started..."
        #################################################################
        
        
        if self.verbose: print "  Plotting most common names value"
        #Example: self.commonNames = [("john", 1877), ("william", 987)]
        commonNamesValues = map(itemgetter(1), self.commonNames)
        xx = range(len(commonNamesValues))
        #plt.plot(xx, commonNamesValues)
        #if showPlots: plt.show()
        
        
        if self.verbose: print "  Plotting most common last letter of values"
        commonLastLetterValues = map(itemgetter(1), self.lastLetterInValueStats)
        xx = range(len(commonLastLetterValues))
        plt.plot(xx, commonLastLetterValues)
        if showPlots: plt.show()
        
        
        #################################################################
        if self.verbose: print "Plotting complete!"
            
    def mostCommonFormat(self, mostCommonList):
        return ", ".join(map(lambda x: "%s (%s)" % x, mostCommonList))
    
    def getAllValues(self, ofType=None, key=None, expandLists=False):
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
                        retvalues += value
        
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
    
    JSONFileName = os.path.abspath("../output/infobox_output_cleaned.json")
    
    global s #TODO: remove me, just used for debugging
    
    s = Statistics(JSONFileName, verbose)
    s.doStatistics()
    if not noPlots:
        s.doPlots(showPlots)
    
    global j #TODO: remove me, just used for debugging
    j = s.JSONLists

if __name__ == "__main__":
    main(showPlots=True)
    
