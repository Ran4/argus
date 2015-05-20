#Antipattern attack! TODO: Fix this...
import os
import sys
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))


from bottle import Bottle, route, run, template, request, static_file

import statistics

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
        self.loadStatistics()
        
        self.loadTemplates()
        self.app = Bottle()
        self.setupRouting()
        
    def loadStatistics(self):
        JSONFileName = os.path.abspath(
            "../../output/infobox_output_cleaned.json")
        print JSONFileName
        
        statisticsOutputFileName = os.path.abspath(
            "../../stats/statistics_output_server.txt")
        
        cleanedKeysFileName = os.path.abspath(
                "../../output/attribute_keys_cleaned.txt")
        
        if not os.path.isfile(cleanedKeysFileName):
            print "Couldn't find attribute_keys_cleaned file at '%s'" % \
                cleanedKeysFileName
            cleanedKeysFileName = None
        
        self.statistics = statistics.Statistics(JSONFileName,
            statisticsOutputFileName, cleanedKeysFileName,
            verbose=False)
            
        self.queryImageOutputFilePath = os.path.abspath(
            "../../stats/plots/query_output.png")
            
        print "Statistics module loaded!"
        
    def loadTemplates(self):
        try:
            with open("template.html") as f:
                self.template = f.read()
            
            with open("image_template.html") as f:
                self.imageTemplate = f.read()
        except:
            print "Problem opening template"
            self.template = "PROBLEM LOADING TEMPLATE"
            self.imageTemplate = "PROBLEM LOADING IMAGE TEMPLATE"
        
    def start(self):
        self.app.run(host=self.host, port=self.port)
        
    def setupRouting(self):
        r = self.app.route
        r("/", callback=self.index)
        r("/submit_query", method="GET", callback=self.submit_query)
        r('/static/:filename', callback=self.serveStatic)
        
    
    def serveStatic(self, filename):
        root = os.path.abspath("../../stats/plots/")
        return static_file(filename,
            root=root)
        
    def index(self):
        self.loadTemplates()
        return template(self.template,
            default_query_value="",
            in_search_checked="",
            imagetemplate="",
            textresponse="")
        
    def submit_query(self):
        queryInput = request.GET.get("query_input")
        useSmartTranslation = not bool(request.GET.get("no_smart_translation"))
        inSearch = bool(request.GET.get("in_search"))
        queryType = request.GET.get("query_type")
        
        print "Got queryInput = '%s'" % queryInput
        print "inSearch:", inSearch
        
        textResponse = "Statistics query crashed..."
        if inSearch:
            searchType = "in_search"
        else:
            searchType = None
        
        textResponse, imageWasSaved = self.statistics.performQuery(
            queryInput, self.queryImageOutputFilePath,
            queryType, searchType, useSmartTranslation,
            verbose=False)
            
        if imageWasSaved:
            #get this from after / in self.queryImageOutputFilePath instead
            
            splittedPath = os.path.split(self.queryImageOutputFilePath)
            print "splitted path:", str(splittedPath)
            path, fname = splittedPath
            
            imageName = fname
            #imageName = "query_output.png"
        else:
            imageName = "server_error.png"
            
        maxTextResponseLength = 80*1000
        if len(textResponse) > maxTextResponseLength:
            textResponse = textResponse[:maxTextResponseLength] + \
                "\n(%s more characters were dropped from output)" % \
                    (len(textResponse) - maxTextResponseLength)
                    
        
        #Return things
        self.loadTemplates()
        return template(self.template,
            default_query_value=queryInput,
            in_search_checked="checked"*inSearch,
            imagetemplate=template(self.imageTemplate, imagename=(imageName)),
            textresponse=textResponse
        ).replace("&lt;","<").replace("&gt;",">").replace('&quot;','"').replace("&#039;",'"')
        
        
def main():
    host = "0.0.0.0"
    port = 8080
    server = Server(host=host, port=port)
    server.start()
    
    
        
if __name__ == "__main__":
    main()
