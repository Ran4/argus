#!/usr/bin/env python2
import re

from termcolor import colored
import os

class AttributeKeyParser:
    """Class that is used to clean keys
    """
    #def __init__(self, keyCounter):
    def __init__(self, keyTranslationFileName, verbose=False):
        """Parses a list of keys and tries to find patterns to be used to
        clean keys.
        """

        #Calls Java code
        cleanedKeysFileName = "attribute_keys_cleaned.txt"
        try:
            cmd = "java attribute_key_cleaner %s %s" % \
                    (keyTranslationFileName, cleanedKeysFileName)
            if verbose: print "Trying to run command '%s'" % cmd
            ret = os.system(cmd)
            if verbose: print "Return value from command: %s" % ret
            if ret != 0:
                raise
        except:
            print colored("Problem calling '%s', quitting..." % cmd, "yellow")
            exit()
            
        print "(presumably) successfully saved cleaned file as %s" % \
            cleanedKeysFileName
            
            
        #Loads file
        self.translationDict = {}
        try:
            with open(cleanedKeysFileName) as f:
                for line in f:
                    raw, cleaned = line.split("\t")
                    self.translationDict[raw] = cleaned
        except:
            print colored("Problem reading list of cleaned keys from file",
                    "yellow")
            exit()
        
        if verbose: print "Loaded translation dictionary from file"

    def findNewKey(self, key):
        """Takes a key as a string, and changes it to be more generic
        E.g. "date of birth" -> "birthdate"
        """
        newKey = key
        
        #~  key = key.replace("_", "-").replace(" ", "-")
        #~  
        #~  match = re.match("(.+)-of-(.+)", key)
        #~  if match and len(match.groups()) == 2:
        #~      newKey = match.groups(2) + match.groups(1)
        
        assert(isinstance(newKey, unicode) or isinstance(newKey, str))
        
        return newKey
    
   
def test(verbose=False):
    print "Testing AttributeKeyParser.findNewKey"
    
    import attribute_cleaner
    inputFileName = attribute_cleaner.defaultInputFileName
    infoBoxList = attribute_cleaner.loadInfoBoxList(inputFileName,
            verbose)
    keyCounter = attribute_cleaner.getKeyCounter(infoBoxList)
    keyTranslationFileName = "attribute_keys_raw.txt"
    attribute_cleaner.saveKeyCounterToFile(keyCounter,
            keyTranslationFileName, verbose)
    attributeKeyParser = AttributeKeyParser(keyTranslationFileName, verbose)
    
    inValues = ["dateofbirth",
            "date of birth",
            "date_of_birth",
            "date-of-birth",
            "date_of birth",
            ]

    outValues = ["dateofbirth",
            "birthdate",
            "birthdate",
            "birthdate",
            "birthdate",
            ]
   
    for inValue, outValue in zip(inValues, outValues):
        retValue = attributeKeyParser.findNewKey(inValue)
        
        if verbose:
            print "'" + inValue + "'"
            if retValue == outValue:
                print "->"
            else:
                print colored("-> ERROR! Should be '%s'" % outValue, "magenta")
            print "'" + outValue + "'"
            print
        assert(retValue == outValue)
    
    
    print "Successfully tested AttributeKeyParser.findNewKey"
    
if __name__ == "__main__":
    test(verbose=True)
