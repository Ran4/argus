#Antipattern attack! TODO: Fix this...
import os
import sys
import time
from operator import itemgetter

from pprint import pprint

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
                
            with open("search_template.html") as f:
                self.searchTemplate = f.read()
        except:
            print "Problem opening template"
            self.template = "PROBLEM LOADING TEMPLATE"
            self.imageTemplate = "PROBLEM LOADING IMAGE TEMPLATE"
            self.searchTemplate = "PROBLEM LOADING SEARCH TEMPLATE"
        
    def start(self):
        self.app.run(host=self.host, port=self.port)
        
    def setupRouting(self):
        r = self.app.route
        r("/", callback=self.index)
        r("/submit_query", method="GET", callback=self.submit_query)
        r("/submit_search_query", method="GET",
            callback=self.submit_search_query)
        r('/static/:filename', callback=self.serveStatic)
        r('/image/:filename', callback=self.serveImage)
    
    def serveStatic(self, filename):
        root = os.path.abspath(".")
        return static_file(filename, root=root)
    
    def serveImage(self, filename):
        root = os.path.abspath("../../stats/plots/")
        return static_file(filename,
            root=root)
        
    def index(self):
        self.loadTemplates()
        
        return self.submit_search_query()
            
    def submit_search_query(self):
        self.loadTemplates()
        
        def getReturnTemplate(textResponse):
            return template(self.searchTemplate,
                default_query_value1=userInput1 or "",
                default_query_value2=userInput2 or "",
                in_search_checked="checked"*bool(inSearch),
                case_sensitive_checked="checked"*bool(caseSensitive),
                textresponse=textResponse).replace("&lt;","<").replace("&gt;",">").replace('&quot;','"').replace("&#039;",'"')
        
        userInput1 = request.GET.get("query_search_input1")
        userInput2 = request.GET.get("query_search_input2")
        useSmartTranslation = not bool(request.GET.get("no_smart_translation"))
        inSearch = bool(request.GET.get("in_search"))
        caseSensitive = bool(request.GET.get("case_sensitive"))
        
        print "in server.submit_search_query, inputs:"
        print userInput1
        print userInput2
        
        textResponse = ""
        requiredKeyValues = None
        requestedValuesKeys = None
        
        requiredKeyValues = []
        requestedValuesKeys = []
        if userInput1:
            for req in map(lambda x: x.strip(), userInput1.split(",")):
                if req.count("=") > 1:
                    resp = "Problems parsing required keys!  "
                    resp += "More than one '=' found in '%s'" % req
                    return getReturnTemplate(resp)
                
                if "=" in req:
                    reqKey, reqValue = req.split("=")
                    requiredKeyValues.append((reqKey, reqValue))
                else:
                    requiredKeyValues.append((req, ""))
                
        if userInput2:
            for outKey in map(lambda x: x.strip(), userInput2.split(",")):
                requestedValuesKeys.append(outKey)
                
            if not requestedValuesKeys:
                resp = "No requested values found!"
                return getReturnTemplate(resp)
        
        if requiredKeyValues and requestedValuesKeys:
            #~ if "url" in requestedValuesKeys:
                #~ requestedValuesKeys.replace
            
            #perform search here
            if inSearch:
                searchType = "in_search"
            else:
                searchType = None
                
            searchRet = self.statistics.search(requiredKeyValues,
                requestedValuesKeys, searchType, caseSensitive)
                
            searchRet = searchRet[:150000]
            
            ##AS LONG TABLE
            #~ textResponseList = []
            #~ for article in searchRet:
                #~ lineList = []
                #~ for kv in article:
                    
                    #~ if kv[0].lower() == "wikiurl":
                        #~ attributeKey = "WP URL:"
                    #~ else:
                        #~ attributeKey = kv[0]
                        
                    #~ values = list(kv[1:])
                    #~ if len(values) > 1:
                        #~ respValue = "; ".join(values)
                    #~ else:
                        #~ if kv[0].lower() == "wikiurl":
                            #~ respValue = "<a href=%s>%s</a>" % \
                                #~ (values[0], values[0].split("/")[-1])
                        #~ else:
                            #~ if isinstance(values[0], list):
                                #~ values[0] = "; ".join(values[0])
                                
                            #~ respValue = values[0]
                        
                    #~ lineList.append("<tr><th>%s</th> <th>%s</th></tr>" % \
                        #~ (attributeKey, respValue))
                        
                #~ textResponseList.append("\n".join(lineList))
            
            #~ textResponse = "<table>\n" + \
                #~ "\n".join(textResponseList) + \
                #~ "\n</table>"
                
            ##AS SHORT TABLE
            textResponseList = []
            
            table = ["<table>"]
            table.append("<tr>")
            
            #column names
            table.append("".join(
                map("<th>{}</th>".format, requestedValuesKeys)))
            table.append("</tr>")
            
            i = 0
            for article in searchRet:
                i += 1
                
                if i % 2 == 0:
                    table.append("<tr class='table_even'>")
                else:
                    table.append("<tr class='table_odd'>")
                
                for key, value in article:
                    if isinstance(value, list):
                        value = "; ".join(value)
                            
                    
                    if key.lower() == "wikiurl": #remove http:/.../ part
                        shownValue = value.split("/")[-1].replace("_", " ")
                            
                        url = "http://en.wikipedia.org/w/index.php?search=%s" %\
                            value.split("/")[-1].replace(" ", "%20")
                            
                        value = "<a href=%s>%s</a>" % (url, shownValue)
                    else:
                        #Don't show really long lines
                        characterLengthLimit = 90
                        if len(value) > characterLengthLimit:
                            value = value[:characterLengthLimit-3] + "..."
                    
                    table.append('<th>%s</th>' % value)
                    
                table.append("</tr>")
            
            table.append("</table>")
            textResponse = "\n".join(table)
            
            
        else:
            textResponse = "Not enough values to perform search."
        
        return getReturnTemplate(textResponse)
        
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
