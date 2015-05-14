#!/bin/bash
#This takes the second column from the first -n lines of person_output.tsv,
#lowercases them, then sorts them and removes the unique values
#head -n 185000 person_output.tsv | cut -f 2 | tr "[:upper:]" "[:lower:]" | sort -u

# same but the entire thing
cat person_output.tsv | cut -f 2 | tr "[:upper:]" "[:lower:]" | sort -u
