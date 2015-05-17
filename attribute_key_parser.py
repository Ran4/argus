#!/usr/bin/env python2
import re

from termcolor import colored

class AttributeKeyParser:
    """Class that is used to clean keys
    """
    def __init__(self, keyCounter):
        """Parses a list of keys and tries to find patterns to be used to
        clean keys.
        
        keyList is a raw list of attribute keys (including e.g. duplicates)
        keyCounter is a collections.Counter object, where the keys
        (keyCounter.keys()) are the attribute keys and the values
        (e.g. keyCounter["name"]) are the total number of occurances of
        that attribute key.
        """
        self.keyCounter = keyCounter

        ##DO STUFF HERE
        
        self.valueToSave = "hejsan"

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
    
    keyList = ["date of birth", "date_of_birth", "birthdate", "birthdate"]
    import attribute_cleaner
    inputFileName = attribute_cleaner.defaultInputFileName
    infoBoxList = attribute_cleaner.loadInfoBoxList(inputFileName,
            verbose=False)
    keyCounter = attribute_cleaner.getKeyCounter(infoBoxList)
    attributeKeyParser = AttributeKeyParser(keyCounter)
    
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
    test()
