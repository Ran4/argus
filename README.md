# Argus
Fetches public personal information in natural language from a Wikipedia dump, and stores it in a json-formatted database.

The project is named "Argus" after the hundred-eyed giant of Greek mythology (additionally, Argus was the name of the builder of the Argonauts' ship - the leader of whom was Jason, a name which is a homophone to the database format the program uses).

##Quick start
* Download wikipedia xml dump (http://en.wikipedia.org/wiki/Wikipedia:Database_download) and save it to root directory (`argus/`)
* Clone the repository `git clone https://github.com/Ran4/argus.git`
* Run `./full_run.sh` (possibly modifying the `xmlwikiparser2.py` line).

`full_run.sh` will parse a wikipedia xml dump, finding all the infoboxes and storing them all as a single json file in `raw_output/`. The initial json dump will then be cleaned, with the final output json residing in `output/`.

## Manual run

Start by placing a copy of the full wikipedia xml (e.g. `enwiki-20150304-pages-articles-multistream.xml`) in the `argus/` folder
```
#All paths given are relative to runstart in /src/
 
#xmlwikiparser2.py inputXMLFileName outputJSONFileName
python xmlwikiparser2.py ../enwiki-20150304-pages-articles-multistream.xml ../raw_output/ibs_person_raw.json
javac java_key_cleaner.java
#attribute_cleaner.py inputFileName outputFileName outputKeysFileName
python attribute_cleaner.py ../raw_output/ibs_person_raw.json ../output/infobox_output_cleaned.json ../debug/attribute_keys_cleaned.txt

#Cleaned JSON available here: https://mega.co.nz/#!YwUlSDRR!EAbguiWFg5ppVBsw5fRGoYQCuBjVvMTOoxTcuwH9I14

python statistics.py noshow silent
```

##Requirements
```
Python 2.7
Python modules:
    matplotlib  #Not required: used in statistics.py to generate plots

Java JDK >6
```
