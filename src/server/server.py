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
        
        self.statistics = statistics.Statistics(JSONFileName,
            statisticsOutputFileName, verbose=False)
            
        print "Statistics module loaded!"
        
    def loadTemplates(self):
        try:
            with open("template.html") as f:
                self.template = f.read()
            
            with open("query_template.html") as f:
                self.queryTemplate = f.read()
        except:
            print "Problem opening template"
            self.template = "PROBLEM LOADING TEMPLATE"
            self.queryTemplate = "PROBLEM LOADING QUERYTEMPLATE"
        
    def start(self):
        self.app.run(host=self.host, port=self.port)
        
    def setupRouting(self):
        r = self.app.route
        r("/", callback=self.index)
        r("/submit_query", method="GET", callback=self.submit_query)
        
    def index(self):
        self.loadTemplates()
        return template(self.template, queryform="<b>BIG</b>")
        
    def submit_query(self):
        queryInput = request.GET.get("query_input")
        
        print "Got queryInput = '%s'" % queryInput
        
        returnedImageName = "error.png"
        try:
            self.statistics.performQuery(queryInput=queryInput)
        except:
            print "Problem calling statistics.performQuery()"
        
        #Return things
        self.loadTemplates()
        returnedImageName = "imagename.png"
        return template(self.template,
            queryform=template(self.queryTemplate, imagename=returnedImageName))
        
        
def main():
    host = "0.0.0.0"
    port = 8080
    server = Server(host=host, port=port)
    server.start()
    
    
        
if __name__ == "__main__":
    main()