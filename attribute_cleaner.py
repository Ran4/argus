import sys
import collections

import attribute_key_parser
import attribute_value_parser

def clean(inputFileName, keysFileName,
        outputFileName, outputKeysFileName,
        verbose=False):
    """Cleans InfoBox data read from a file, and writes the cleaned
        data back to another file.
        
    The two input filenames is for the InfoBoxJSON and a list of
        attribute key values.
    The output filenames is for the cleaned output
    """
    #Get attribute keys
    with open(keysFileName) as keysFile:
        keyList = keysFile.read().split("\n")
        keyCounter = collections.Counter(keyList)
        if verbose: print "Successfully loaded attribute keys from JSON"
        
    attributeKeyParser = attribute_key_parser.AttributeKeyParser(keyList)
    
    #Get infoboxes 
    with open(inputFileName) as inputFile:
        infoBoxList = json.load(inputFile)
        assert isinstance(infoBoxList, list)
        if verbose: print "Successfully loaded infoBoxList from JSON"
    
    #Clean up infobox data
    cleanedInfoBoxList = []
    counter = collections.Counter({
            "ignored_new_keys":0,
            "ignored_new_values":0,
            "changed_infoboxes":0,
            })
    for ib in infoBoxList:
        attributeDict = {}
        for key in ib:
            #Handle keys
            #newKey = attribute_key_parser.findNewKey(keyList, key)
            newKey = attributeKeyParser.findNewKey(key)
            if verbose: print "K: {} -> {}".format(key, newKey)
            if not newKey:
                counter["ignored_new_keys"] += 1
                continue
            
            
            #Handle values
            newValue = attribute_value_parser.parseAttributeValues(ib[value])
            if verbose: print "V: {} -> {}".format(ib[value], newValue)
            if not newValue:
                counter["ignored_new_values"] += 1
                continue
            
            attributeDict[newKey] = newValue
            if newKey != key or newValue != ib[value]:
                counter["changed_infoboxes"] += 1
            
        cleanedInfoBoxList.append(attributeDict) 
        if verbose:
            print "{}/{} keys and {}/{} values was ignored".format(
                    counter["ignored_new_keys"], len(ib),
                    counter["ignored_new_values"], len(ib))
        
    if verbose:
        print "Changed {} infoboxes, will now write {} infoboxes".format(
                counter["changed_infoboxes"], len(cleanedInfoBoxList))
    newJSONString = json.dumps(cleanedInfoBoxList, indent=4)
    if verbose:
        print "Successfully wrote cleaned data to file {}".format(
                cleanedFilename)

def main():
    if len(sys.argv) != 4+1: #The right number of arguments wasn't given
        inputFileName = "ibs_person_raw_150515_60M.json"
        keysFileName = "attribute_keys_raw.txt"
        outputFileName = "infobox_output_cleaned.json"
        outputKeysFileName = "attribute_keys_cleaned.txt"
        print "Usage:"
        print "attribute_cleaner {} {} {} {}".format(inputFileName,
                keysFileName, outputFileName, outputKeysFileName)
        response = raw_input("Use default values (Y/N)? ")
        
        if response.lower() not in ("y", "yes"):
            return
    else:
        inputFileName = sys.argv[1]
        keysFileName  = sys.argv[2]
        outputFileName  = sys.argv[3]
        outputKeysFileName  = sys.argv[4]
    
    clean(inputFileName, keysFileName,
        outputFileName, outputKeysFileName)

if __name__ == "__main__":
    main()
