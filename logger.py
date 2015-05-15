defaultFileName = "log.log"

def writeToFile(s, fileName=defaultFileName):
    """Appends a string to a file...
    """
    try:
        fileName = fileName
        with open(fileName, "a") as logFile:
            logFile.write(s)
    except:
        print "Error saving to logfile"
