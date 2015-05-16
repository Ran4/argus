import sys
import collections

import attribute_key_parser
import attribute_value_parser

import json

def saveFiles(cleanedKeysCounter, cleanedInfoBoxList,
        outputFileName, outputKeysFileName, verbose):
    #Dump a list of key values that we used 
    if verbose: print "Trying to save cleaned attribute keys to file..."
    keyAndCount = sorted(cleanedKeysCounter.items(),
        key=lambda x: x[1], reverse=True)
    keyAndCountToStringFunction = lambda x: str(x[1]) + " " + x[0].encode("utf-8")
    keyCountString = "\n".join(map(keyAndCountToStringFunction, keyAndCount))
    try:
        with open(outputKeysFileName, "w") as f:
            f.write(keyCountString)
    except IOError as e:
        print "Problem saving cleaned attribute keys to file {}".format(
                outputKeysFileName)
    if verbose:
        print "Successfully wrote cleaned attribute keys to file {}".format(
                outputKeysFileName)
       
        
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
    if verbose: print "Starts cleaning up InfoBox data..."
    cleanedInfoBoxList = []
    counter = collections.Counter({
            "ignored_new_keys":0,
            "ignored_new_values":0,
            "changed_infoboxes":0,
            "total_attributes":0,
            })
    cleanedKeysCounter = collections.Counter()
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
            newValue = attribute_value_parser.parseAttributeValue(ib[key])
            #~ if verbose: print "V: {} -> {}".format(ib[key], newValue)
            if not newValue:
                counter["ignored_new_values"] += 1
                continue
            
            #update our attribute dictionary
            attributeDict[newKey] = newValue
            if newKey != key or newValue != ib[key]:
                counter["changed_infoboxes"] += 1
            
        cleanedInfoBoxList.append(attributeDict) 
        
    if verbose:
        print "{}/{} keys and {}/{} values was ignored".format(
            counter["ignored_new_keys"], counter["total_attributes"],
            counter["ignored_new_values"], counter["total_attributes"])
        
        print "Changed {} infoboxes, will now write {} infoboxes".format(
                counter["changed_infoboxes"], len(cleanedInfoBoxList))
        
    return cleanedInfoBoxList, cleanedKeysCounter

def loadInfoBoxList(inputFileName, verbose):
    with open(inputFileName) as inputFile:
        #~ infoBoxList = json.load(inputFile)
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
    attributeKeyParser = attribute_key_parser.AttributeKeyParser(keyCounter)
    cleanedInfoBoxList, cleanedKeysCounter = cleanInfoBoxList(
            attributeKeyParser, infoBoxList, verbose)
    saveFiles(cleanedKeysCounter, cleanedInfoBoxList,
                    outputFileName, outputKeysFileName, verbose)
    
def main():
    if len(sys.argv) != 3+1: #The right number of arguments wasn't given
        inputFileName = "ibs_person_raw_76M.json"
        outputFileName = "infobox_output_cleaned.json"
        outputKeysFileName = "debug/attribute_keys_cleaned.txt"
        print "Usage:"
        print "attribute_cleaner inputFileName outputFileName outputKeysFileName"
        print "Default values:"
        print "attribute_cleaner {} {} {}".format(inputFileName,
                outputFileName, outputKeysFileName)
        response = raw_input("Use default values (y/n)? ")
        
        if response.lower() not in ("y", "yes"):
            return
    else:
        inputFileName = sys.argv[1]
        outputFileName  = sys.argv[2]
        outputKeysFileName  = sys.argv[3]
    
    clean(inputFileName, outputFileName, outputKeysFileName, verbose=True)

if __name__ == "__main__":
    main()
