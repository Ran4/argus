import re

class AttributeKeyParser:
    """Class that is used to clean keys
    """
    def __init__(self, keyList):
        """Parses a list of keys and tries to find patterns to be used to
        clean keys.
        
        keyList is a raw list of attribute keys (including e.g. duplicates)
        """
        self.keyList = keyList

        ##DO STUFF HERE

    def findNewKey(self, key):
        """Takes a key as a string, and changes it to be more generic
        E.g. "date of birth" -> "birthdate"
        """
        return key
    
   
#~ def test():
#~     print "Testing AttributeKeyParser..."
#~     
#~     keyList = ["date of birth", "date_of_birth", "birthdate", "birthdate"]
#~     attributeKeyParser = AttributeKeyparser(keyList)
#~     
#~     f = attributeKeyParser.findNewKeys
#~    
#~     for value, 
#~     assert(f() == "")
#~     
#~     print "#"*20
#~     print "SUCCESSFULLY TESTED AttributeKeyParser"
#~     print "#" * 20
    
if __name__ == "__main__":
    pass
    #~ test()
