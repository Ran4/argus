#!/usr/bin/env python2
import re
import os

from termcolor import colored
import logger

class AttributeKeyParser:
    """Class that is used to clean keys
    """
    #def __init__(self, keyCounter):
    def __init__(self, keyTranslationFileName, verbose=False):
        """Parses a list of keys and tries to find patterns to be used to
        clean keys.
        """
        
        self.numNotFound = 0
        
        #print colored("WARNING! KEY CLEANING IGNORED!", "magenta")
        #return

        #Calls Java code
        cleanedKeysFileName = os.path.abspath(
                "../output/attribute_keys_cleaned.txt")
        self.warningLogMessageFileName = os.path.abspath(
                "../logs/attributekeyparser_warnings.log")
        
        #Clear log file
        with open(self.warningLogMessageFileName, "w") as f:
            f.write("")
        
        try:
            cmd = "java java_key_cleaner %s %s" % \
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
                    raw, cleaned = line.strip().split("\t")
                    self.translationDict[raw] = cleaned
        except:
            print colored("Problem reading list of cleaned keys from file",
                    "yellow")
            exit()
        
        if verbose: print "Loaded translation dictionary from file"
        
        #Ignore these keys completely
        self.ignoredKeys = ["image", "alt", "caption", "image_size",
            "footnotes", "background", "module", "bgcolor",
            "signature", "signature_alt",]

    def findNewKey(self, key, verbose=False):
        """Takes a key as a string, and changes it to be more generic
        E.g. "date of birth" -> "birthdate"
        """
        newKey = key
        
        if key in self.ignoredKeys:
            return ""
        
        if key in self.translationDict:
            newKey = self.translationDict[key]
        else:
            if key == "":
                return ""
            self.numNotFound += 1
            warningMessage = "WARNING: '%s' not found in translation dict" % key
            print colored(warningMessage.encode("utf-8"), "magenta")
            
            logger.writeToFile((warningMessage+"\n").encode("utf-8"),
                    self.warningLogMessageFileName, timeStamp=True)
            
            return newKey
        
        assert(isinstance(newKey, unicode) or isinstance(newKey, str))
        
        return newKey
    
   
def test(verbose=False):
    print "Testing AttributeKeyParser.findNewKey"
    
    import attribute_cleaner
    inputFileName = attribute_cleaner.defaultInputFileName
    infoBoxList = attribute_cleaner.loadInfoBoxList(inputFileName,
            verbose)
    keyCounter = attribute_cleaner.getKeyCounter(infoBoxList)
    keyTranslationFileName = os.path.abspath("../raw_output/attribute_keys_raw.txt")
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
