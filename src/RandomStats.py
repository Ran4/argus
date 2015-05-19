import json,re,os
from pprint import pprint

def getStatistics(s,data):
    statistics = {}
    for d in data:
        if s in d:
            n = d[s]
            if(isinstance(n,(list,tuple))):
                n = ",".join(n)
            if not n in statistics:
                statistics[n] = 0
            statistics[n]+=1
            
    statList = statistics.items()
    return sorted(statList,key=lambda x: x[1], reverse=True)
    
def getCategories(s,data):
    found = {}
    for d in data:
        for f in d.keys():
            if(s in f):
                if not f in found:
                    found[f] = 0
                found[f] += 1
    return sorted(found.items(),key=lambda x: x[1], reverse=True)
                    
# Get categories given partial value of attribute
def getCategoriesReverse(s, data):
    found = {}
    for d in data:
        for k,v in d.items():
            if(s in v):
                if not k in found:
                    found[k] = 0
                found[k] += 1
    return sorted(found.items(),key=lambda x: x[1], reverse=True)

def search(queryIn, queryOut, data):
    """ 
        queryIn: ((key, value))
        queryOut: (key)
        data: json data
        returns: ((key, value))
    """
    
    results = []
    
    for d in data:
        passed = True
        for kv in queryIn:
            if not(kv[0] in d and kv[1] in d[kv[0]]):
                passed = False
                break
        if(passed):
            r = []
            for k in queryOut:
                if k in d:
                    r.append((k,d[k]))
                else:
                    r.append((k,""))
            results.append(r)
    return results

def getAverageWikipedianBirthYear(data):
    years = 0.0
    persons = 0.0
    missed = 0
    
    pat = re.compile(".*?([0-9]{4}).*?")
    for d in data:
        if("birth_date" in d):
            db = d["birth_date"]
            if(isinstance(db,(list,tuple))):
                db = ",".join(db)
            a = pat.match(db)
            try:
                i = int(a.group(1))
                persons+=1
                years = years*(persons-1)/(persons)+i/persons
            except:
                #print db
                missed+=1
    global DEBUG
    if(DEBUG):
        print "MISSED",missed,"OF",missed+persons,"PERSONS"
    return years
    
def getAverageWikipedianDeathYear(data):
    years = 0.0
    persons = 0.0
    missed = 0
    
    pat = re.compile(".*?([0-9]{4}).*?")
    for d in data:
        if("death_date" in d):
            db = d["death_date"]
            if(isinstance(db,(list,tuple))):
                db = ",".join(db)
            a = pat.match(db)
            try:
                i = int(a.group(1))
                persons+=1
                years = years*(persons-1)/(persons)+i/persons
            except:
                #print db
                missed+=1
    global DEBUG
    if(DEBUG):
        print "MISSED",missed,"OF",missed+persons,"PERSONS"
    return years

def getAverageWikipedianHeight(data):
    height = 0.0
    persons = 0.0
    
    missing = 0
    
    patCM = re.compile(".*?([0-9]{3}).*?")
    patM = re.compile(".*?([0-9]\.[0-9]{2}).*?")
    
    for d in data:
        if("height" in d):
            dh = d["height"]
            if(isinstance(dh,(list,tuple))):
                dh = ",".join(dh)
            # CM TRY
            a = patCM.match(dh)
            try:
            #    print dh
                i = int(a.group(1))
                persons+=1
                height = height*(persons-1)/(persons)+i/persons
            except:
                a = patM.match(dh)
                try:
                    i = int(float(a.group(1))*100)
                    persons+=1
                    height = height*(persons-1)/(persons)+i/persons
                except:
                    missing+=1
    global DEBUG
    if(DEBUG):
        print "MISSED",missing,"OF",int(persons)+missing,"PERSONS"
    return height
    
def getAverageWikipedianName(sa,data):
    firstNameCounter = {}
    lastNameCounter = {}
    
    found = 0
    missed = 0
    
    for d in data:
        if sa in d:
            splitName = d[sa]
            
            if(isinstance(splitName,(list,tuple))):
                splitName = ",".join(splitName)
                
            splitName = splitName.split(" ")
            if(len(splitName)==2):
                if not splitName[0] in firstNameCounter:
                    firstNameCounter[splitName[0]] = 0
                if not splitName[1] in lastNameCounter:
                    lastNameCounter[splitName[1]] = 0
                firstNameCounter[splitName[0]] += 1
                lastNameCounter[splitName[1]] += 1
                found+=1
            else:
                missed+=1
    global DEBUG
    if(DEBUG):
        print "MISSED",missed,"OF",found+missed,"PERSONS"
    s = (sorted(firstNameCounter.items(),key=lambda x: x[1], reverse=True)[0][0]+" "
        +sorted(lastNameCounter.items(),key=lambda x: x[1], reverse=True)[0][0])
    return s.title().encode("utf-8")

FNAME = os.path.abspath("../output/infobox_output_cleaned.json")
#FNAME = "infobox_output_cleaned.json"

f = open(FNAME,"r")
raw_data = f.read()
f.close()

data = json.loads(raw_data)

#print getStatistics("birth_date",data)[0:50]

#print getStatistics("hair_color",data)
#print getCategories("occup",data)

DEBUG = False

#print getCategoriesReverse("dirty",data)


#pprint(search([("birth_date","1942")], ["name","wikiURL", "birth_date"], data)[:20])
# michael bloomberg, missing name and wikiURL waaah

#pprint(search([("hair_color","dirty blond")], ["name","wikiURL"], data))

#pprint(search([("birth_date","1956"),("birth_place","london")], ["name","wikiURL"], data))
#pprint(search([("birth_date","195"),("birth_place","london")], ["name","wikiURL"], data))

pprint(getStatistics("height",data)[0:100])

#print "WOOP"
"""
print "BORN:",getAverageWikipedianBirthYear(data)
print "DIED:",getAverageWikipedianDeathYear(data)
print "HEIGHT:",getAverageWikipedianHeight(data)
print "NAME:",getAverageWikipedianName("name",data).encode("utf-8")
print "NATIVE NAME:",getAverageWikipedianName("native_name",data)
print "NICKNAME:",getStatistics("nickname",data)[0][0].title().encode("utf-8")
print "OTHER NAME:",getAverageWikipedianName("other_names",data)
print "OTHER NAME2:",getAverageWikipedianName("othername",data)
print "PSEUDONYM:",getAverageWikipedianName("pseudonym",data)
print "FATHER:",getAverageWikipedianName("father",data)
print "MOTHER:",getAverageWikipedianName("mother",data)
print "OCCUPATION:",getStatistics("occupation",data)[0][0].title().encode("utf-8")
print "PROFESSION:",getStatistics("profession",data)[0][0].title().encode("utf-8")
print "EMPLOYER:",getStatistics("employer",data)[0][0].title().encode("utf-8")
print "RETIRED:",getStatistics("retired",data)[0][0].title().encode("utf-8")
print "LATERWORK:",getStatistics("laterwork",data)[0][0].title().encode("utf-8")
print "NATIONALITY:",getStatistics("nationality",data)[0][0].title().encode("utf-8")
print "ETHNICITY:",getStatistics("ethnicity",data)[0][0].title().encode("utf-8")
print "SPOUSE:",getAverageWikipedianName("spouse",data)
print "BIRTHPLACE:",getStatistics("birth_place",data)[0][0].title().encode("utf-8")
print "ORIGIN:",getStatistics("origin",data)[0][0].title().encode("utf-8")
print "DEATHPLACE:",getStatistics("death_place",data)[0][0].title().encode("utf-8")
print "DEATH CAUSE:",getStatistics("death_cause",data)[0][0].title().encode("utf-8")
print "COUNTRY:",getStatistics("country",data)[0][0].title().encode("utf-8")
print "CITIZENSHIP:",getStatistics("citizenship",data)[0][0].title().encode("utf-8")
print "CHILDREN:",getStatistics("children",data)[0][0].title().encode("utf-8")
print "ALMA MATER:",getStatistics("alma_mater",data)[0][0].title().encode("utf-8")
print "EDUCATION:",getStatistics("education",data)[0][0].title().encode("utf-8")
print "COLLEGE:",getStatistics("college",data)[0][0].title().encode("utf-8")
print "FIELD:",getStatistics("field",data)[0][0].title().encode("utf-8")
print "SUBJECT:",getStatistics("subject",data)[0][0].title().encode("utf-8")
print "RELIGION:",getStatistics("religion",data)[0][0].title().encode("utf-8")
print "PARTY:",getStatistics("party",data)[0][0].title().encode("utf-8")
print "RESIDENCE:",getStatistics("residence",data)[0][0].title().encode("utf-8")
print "AWARDS:",getStatistics("awards",data)[0][0].title().encode("utf-8")
print "PRIZES:",getStatistics("prizes",data)[0][0].title().encode("utf-8")
print "BACKGROUND:",getStatistics("background",data)[0][0].title().encode("utf-8")
print "INSTRUMENT:",getStatistics("instrument",data)[0][0].title().encode("utf-8")
print "NOTABLE INSTRUMENT:",getStatistics("notable_instruments",data)[0][0].title().encode("utf-8")
print "DEBUT YEAR:",getStatistics("debutyear",data)[0][0].title().encode("utf-8")
print "POSITION:",getStatistics("position",data)[0][0].title().encode("utf-8")
print "DEBUT TEAM:",getStatistics("debutteam",data)[0][0].title().encode("utf-8")
print "KNOWN FOR:",getStatistics("known_for",data)[0][0].title().encode("utf-8")
print "OFFICE:",getStatistics("office",data)[0][0].title().encode("utf-8")
print "TITLE:",getStatistics("title",data)[0][0].title().encode("utf-8")
print "RESTING PLACE:",getStatistics("resting_place",data)[0][0].title().encode("utf-8")
print "PLACE OF BURIAL:",getStatistics("placeofburial",data)[0][0].title().encode("utf-8")
print "PLACE OF BURIAL2:",getStatistics("place of burial",data)[0][0].title().encode("utf-8")
print "GENERAL:",getStatistics("rank",data)[0][0].title().encode("utf-8")
print "BRANCH:",getStatistics("branch",data)[0][0].title().encode("utf-8")
print "BATTLES:",getStatistics("battles",data)[0][0].title().encode("utf-8")
print "COMMANDS:",getStatistics("commands",data)[0][0].title().encode("utf-8")
print "UNIT:",getStatistics("unit",data)[0][0].title().encode("utf-8")
print "INFLUENCED:",getStatistics("influenced",data)[0][0].title().encode("utf-8")
print "INFLUENCES:",getStatistics("influences",data)[0][0].title().encode("utf-8")
print "ALLEGIANCE:",getStatistics("allegiance",data)[0][0].title().encode("utf-8")
print "WEIGHT:",getStatistics("weight",data)[0][0].title().encode("utf-8")
print "DOCTORAL ADVISOR:",getAverageWikipedianName("doctoral_advisor",data)
print "MOVEMENT:",getStatistics("movement",data)[0][0].title().encode("utf-8")
print "SUCCESSION:",getStatistics("succession",data)[0][0].title().encode("utf-8")
print "PC UPDATE:",getStatistics("pcupdate",data)[0][0].title().encode("utf-8")
print getStatistics("native_name_lang",data)[0:30]
"""

#print 
#print search([("relations","nehru")],("name","wikiURL"),data)
