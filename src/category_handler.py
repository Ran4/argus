import re
import os

import logger

logPath = os.path.abspath("../logs/categoryhandler_log.log")
logNewDataPath = os.path.abspath("../logs/categoryhandler_newvalues.log")

def handleCategory(d, category):
    """Takes a category, and a  dictionary that the
        category will be saved in.
    
    ##TODO: If d has a key "__categories__", properly parsed categories
    ##    will be removed from it.
    """
    
    keyValuePairs = _handleCategory(d, category)
    
    #~ for key, value in keyValuePairs:
        #~ if key is not None and value is not None:
    
    if keyValuePairs:
        s2 = " AND ".join("%s=%s" % keyValuePair for keyValuePair in keyValuePairs)
        s = "%s -> %s\n" % (category, s2)
        logger.writeToFile(s, logPath, timeStamp=True)
            #s = "%s -> %s = %s\n" % (category, key, value)
            #logger.writeToFile(s, logPath, timeStamp=True)
            
            #print "Category handled:", s.encode("utf-8")
    
def _handleCategory(d, category):
    def handleCollision(key, value):
        
        
        if key in d:
            if isinstance(d[key], list):
                if value.lower() not in map(lambda x: x.lower(), d[key]):
                    d[key].append(value)
            else: #Turn it into a list
                if value.lower() != d[key].lower():
                    d[key] = [d[key], value]
        else: #new data! Yeah!
            d[key] = value
            
            logger.writeToFile("%s=%s\n" % (key, value), logNewDataPath, timeStamp=True)
    
    c = category
    lc = category.lower()
    key = None
    value = None
    
    #People from X -> residence = X
    if lc.startswith("people from "):
        key = "residence"
        value = c[len("people from "):].strip()
        handleCollision(key, value)
        return [(key, value)]
    
    #X of Y descent -> ethnicity = Y, nationality = X
    match = re.match("(?i)(.+?)(?: people)* of (.+?) descent", c)
    if match and len(match.groups(1)) == 2:
        key, value = "ethnicity", match.groups(1)[1].strip()
        handleCollision(key, value)
        
        key2, value2 = "nationality", match.groups(1)[0].strip()
        handleCollision(key2, value2)
        return [(key, value), (key2, value2)]
        
    #Deaths from X -> cause_of_death = X
    if lc.startswith("deaths from "):
        key = "cause_of_death"
        value = c[len("deaths from "):].strip()
        handleCollision(key, value)
        return [(key, value)]
        
    #X alumni -> alma_mater = X
    if lc.endswith(" alumni"):
        key = "alma_mater"
        value = c[:-len(" alumni")]
        handleCollision(key, value)
        return [(key, value)]
    
    #no match was found    
    return None

def test():
    pass

if __name__ == "__main__":
    test()