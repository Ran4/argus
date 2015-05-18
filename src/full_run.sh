#!/bin/bash
echo Calling xmlwikiparser2.py to output raw infobox values, should take 30-45 minutes with an ssd
python xmlwikiparser2.py  ../raw_output/ibs_person_raw.json
#python xmlwikiparser2.py ../debug/enwiki_first35klines.txt ../raw_output/ibs_person_raw.json

#Skip the previous step by getting the json here: https://mega.co.nz/#!YwUlSDRR!EAbguiWFg5ppVBsw5fRGoYQCuBjVvMTOoxTcuwH9I14
echo Calling javac java_key_cleaner.java
javac java_key_cleaner.java

echo Calling attribute_cleaner.py ../raw_output/ibs_person_raw.json ../output/infobox_output_cleaned.json ../debug/attribute_keys_cleaned.txt
python attribute_cleaner.py ../raw_output/ibs_person_raw.json ../output/infobox_output_cleaned.json ../debug/attribute_keys_cleaned.txt
 
