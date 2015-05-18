import json

def main():
    fileName = "ibs_person_raw_150515_60M.json"
    with open(fileName) as f:
        # loadedJSON = json.load(f)
        loadedJSON = json.loads(f.read())
        print "loadedJson type:", type(loadedJSON)
        print "loadedJson len:", len(loadedJSON)

if __name__ == "__main__":
    main()
