#!/bin/bash
echo Calling xmlwikiparser2.py, might take 20-30 minutes
python xmlwikiparser2.py infobox_output_raw.json

echo Calling attribute_cleaner.py
python attribute_cleaner.py infobox_output_raw.json attribute_keys_raw.txt
