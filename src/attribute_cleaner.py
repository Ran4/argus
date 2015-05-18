#!/usr/bin/env python2
import sys
import os
import collections
import json

import attribute_key_parser
import attribute_value_parser
import logger

def saveKeyCounterToFile(keyCounter, fileName, verbose):
    if verbose: print "Trying to save attribute keys to file..."
    keyAndCount = sorted(keyCounter.items(),
        key=lambda x: x[1], reverse=True)
    keyAndCountToStringFunction = lambda x: \
        str(x[1]) + " " + x[0].encode("utf-8")
    keyCountString = "\n".join(map(keyAndCountToStringFunction, keyAndCount))
    try:
        with open(fileName, "w") as f:
            f.write(keyCountString)
    except IOError as e:
        print "Problem saving attribute keys to file {}".format(
                fileName)
    if verbose:
        print "Successfully wrote attribute keys to file {}".format(
                fileName)

def saveFiles(cleanedKeysCounter, cleanedInfoBoxList,
        outputFileName, outputKeysFileName, verbose):
    
    saveKeyCounterToFile(cleanedKeysCounter, outputKeysFileName, verbose)
        
    #Dump our new, cleaned InfoBoxList to a new JSON 
    newJSONString = json.dumps(cleanedInfoBoxList, indent=2)
    try:
        with open(outputFileName, "w") as f:
            f.write(newJSONString)
    except IOError as e:
        print "Problem saving cleaned JSON to file {}, quitting...".format(
                outputFileName)
        exit()

    if verbose:
        print "Successfully wrote cleaned data to file {}".format(
                outputFileName)
        
def cleanInfoBoxList(attributeKeyParser, infoBoxList, verbose):
    if verbose: print "\nStarts cleaning up InfoBox data..."
    cleanedInfoBoxList = []
    counter = collections.Counter({
            "ignored_new_keys":0,
            "ignored_new_values":0,
            "changed_infoboxes":0,
            "total_attributes":0,
            })
    cleanedKeysCounter = collections.Counter()
    attributeValueParser = attribute_value_parser.AttributeValueParser(verbose)
    for ib in infoBoxList:
        attributeDict = {}
        #ib is a dictionary, where the keys are attribute keys
        for key in ib:
            counter["total_attributes"] += 1
            
            #Handle keys
            newKey = attributeKeyParser.findNewKey(key)
            
            cleanedKeysCounter[newKey] += 1
            
            #~ if verbose: print "K: {} -> {}".format(key, newKey)
            if not newKey:
                counter["ignored_new_keys"] += 1
                continue
            
            #Handle values
            newValue = attributeValueParser.parseAttributeValue(ib[key],
                    verbose=False)
            #~ if verbose: print "V: {} -> {}".format(ib[key], newValue)
            if not newValue:
                counter["ignored_new_values"] += 1
                continue
            
            #update our attribute dictionary
            attributeDict[newKey] = newValue
            if newKey != key or newValue != ib[key]:
                counter["changed_infoboxes"] += 1
            
        cleanedInfoBoxList.append(attributeDict) 
        
    
    s = "{}/{} keys and {}/{} values was ignored".format(
        counter["ignored_new_keys"], counter["total_attributes"],
        counter["ignored_new_values"], counter["total_attributes"])
    if verbose: print s
    logger.writeToFile(s, timeStamp=True)
        
    s = "%s keys not found" % numNotFound
    logger.writeToFile(s, timeStamp=True)
    if verbose: print s
    
    s = "Changed {} infoboxes, will now write {} infoboxes".format(
            counter["changed_infoboxes"], len(cleanedInfoBoxList))
    logger.writeToFile(s, timeStamp=True)
    if verbose: print s
        
    return cleanedInfoBoxList, cleanedKeysCounter

def loadInfoBoxList(inputFileName, verbose):
    with open(inputFileName) as inputFile:
        print "Trying to load JSON file from %s" % inputFile
        
        infoBoxList = json.load(inputFile, encoding="latin-1")
        assert isinstance(infoBoxList, list)
        if verbose:
            print "Successfully loaded infoBoxList from JSON",
            print "({} infoboxes loaded)".format(len(infoBoxList))
            
    return infoBoxList

def getKeyCounter(infoBoxList):
    keyCounter = collections.Counter()
    for ib in infoBoxList:
        for key in ib:
            #TODO: remove this, this is already done in xmlwikiparser2.py
            if "\t" in key:
                key = key.replace("\t", "")
            keyCounter[key] += 1

    return keyCounter

def clean(inputFileName, outputFileName, outputKeysFileName,
        verbose=False):
    """Cleans InfoBox data read from a file, and writes the cleaned
        data back to another file.
    Also saves the new key outputs as a new file 
        
    The first input filename is for the InfoBoxJSON
    The output filenames is for the cleaned JSON output and the cleaned
    key output, respectively
    """
    
    infoBoxList = loadInfoBoxList(inputFileName, verbose)
    keyCounter = getKeyCounter(infoBoxList)
    
    assert(all(["\t" not in key for key in keyCounter.keys()]))
    
    keyTranslationFileName = os.path.abspath("../raw_output/attribute_keys_raw.txt")
    saveKeyCounterToFile(keyCounter, keyTranslationFileName, verbose)
    attributeKeyParser = attribute_key_parser.AttributeKeyParser(
            keyTranslationFileName, verbose)
    cleanedInfoBoxList, cleanedKeysCounter = cleanInfoBoxList(
            attributeKeyParser, infoBoxList, verbose)
    saveFiles(cleanedKeysCounter, cleanedInfoBoxList,
                    outputFileName, outputKeysFileName, verbose)
    
defaultInputFileName = os.path.abspath("../raw_output/ibs_person_raw_76M.json")
defaultOutputFileName = os.path.abspath("../output/infobox_output_cleaned.json")
defaultOutputKeysFileName = os.path.abspath("../output/attribute_keys_cleaned.txt")
    
def main():
    if len(sys.argv) != 3+1: #The right number of arguments wasn't given
        inputFileName = defaultInputFileName
        outputFileName = defaultOutputFileName
        outputKeysFileName = defaultOutputKeysFileName
        print "Usage:",
        print "attribute_cleaner inputFileName outputFileName outputKeysFileName"
        print "Default values:",
        print "attribute_cleaner {} {} {}".format(inputFileName,
                outputFileName, outputKeysFileName)
        response = raw_input("Use default values (y/n)? ")
        
        if response.lower() not in ("y", "yes"):
            return
    else:
        inputFileName = os.path.abspath(sys.argv[1])
        outputFileName  = os.path.abspath(sys.argv[2])
        outputKeysFileName  = os.path.abspath(sys.argv[3])
    
    clean(inputFileName, outputFileName, outputKeysFileName, verbose=True)

if __name__ == "__main__":
    main()
