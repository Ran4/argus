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

def statOutput(s, verbose=True):
    print s
    logger.writeToFile(s.encode("utf-8"), statisticsOutputFileName)

class Statistics:
    def __init__(self, JSONFileName):
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
            
        print "Loaded JSON and reset statistics output file (%s)" % \
            statisticsOutputFileName
    
    def doStatistics(self):
        mostCommonFormat = self.mostCommonFormat
        
        self.commonNames = self.commonNameSubStringsCounter().most_common(500)
        statOutput("Most common name substrings: %s" % mostCommonFormat(
            self.commonNames))
        
    def doPlots(self):
        import matplotlib.pyplot as plt #use matplotlib to plot stuff
        opj = os.path.join
        plotFileOutputPath = os.path.abspath("../stats/plots/")
        
        print "Plotting started..."
        
        print "  Plotting most common names value"
        #Example: self.commonNames = [("john", 1877), ("william", 987)]
        commonNamesValues = map(itemgetter(1), self.commonNames)
        xx = range(len(commonNamesValues))
        plt.plot(xx, commonNamesValues)
        
        plt.show()
        
        
        print "Plotting complete!"
            
    def mostCommonFormat(self, mostCommonList):
        return ", ".join(map(lambda x: "%s (%s)" % x, mostCommonList))
        
        
    def getAllValues(self, key, ofType=None):
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
            for nameSubString in [val.split() for val in self.getAllValues("name", unicode)
                    if len(val) <= 80]: #Don't take name values that are too long
                for subString in nameSubString:
                    if subString in ["the", "of"]:
                        continue
                    nameSubStrings.append(subString)
                
            #print "nameSubStrings:"
            #print nameSubStrings
            
            global c
            
            c = Counter(nameSubStrings)
            
            return c
            
        

def main():
    JSONFileName = os.path.abspath(
        "../output/infobox_output_cleaned.json")
    
    global s #TODO: remove me, just used for debugging
    
    s = Statistics(JSONFileName)
    s.doStatistics()
    s.doPlots()
    
    global j #TODO: remove me, just used for debugging
    j = s.JSONLists

if __name__ == "__main__":
    main()
