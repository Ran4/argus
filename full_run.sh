#!/bin/bash
echo Calling xmlwikiparser2.py to output raw infobox values, should take 30-45 minutes with an ssd
python xmlwikiparser2.py debug/enwiki_first35klines.txt ibs_person_raw.json

echo Calling javac java_key_cleaner.java
javac java_key_cleaner.java

echo Calling attribute_cleaner.py ibs_person_raw.json infobox_output_cleaned.json debug/attribute_keys_cleaned.txt
python attribute_cleaner.py ibs_person_raw.json infobox_output_cleaned.json debug/attribute_keys_cleaned.txt
 
