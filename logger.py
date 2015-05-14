


def writeToFile(s, fileName="log.txt"):
    """Appends a string to a file...
    """
    try:
        fileName = fileName
        with open(fileName, "a") as logFile:
            logFile.write(s)
    except:
        print "Error saving to logfile"
