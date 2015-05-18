defaultFileName = "../logs/log.log"

def writeToFile(s, fileName=defaultFileName, verbose=False):
    """Appends a string s to a file...
    """
    try:
        with open(fileName, "a") as logFile:
            logFile.write(s)
            
        if verbose:
            print "Appended {} chars to file {}".format(
                    len(s), fileName)
    except IOError as e:
        print e.strerror
        print "Error saving to logfile {}".format(fileName)
        print "Error content: {}".format(
                s[:8000] + "...."*(len(s)>8000))
        
