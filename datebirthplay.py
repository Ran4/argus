import re

ss = """
birth_date
birthdate
date-of-birth
date_of_birth
""".split("\n")[1:-1]

print(ss)

for word in ss:
    print "%s -> %s" % (word, fixWord(word))


def fixWord(word):
    newWord = word.replace("-","_").replace(" ","_")
    ofMatches = re.match("(.+)_of_(.+)", newWord)
    if ofMatches and len(ofMatches.groups()) == 2:
        newWord = ofMatches.group(2) + ofMatches.group(1)
    
    newWord = newWord.replace("_", "")
    return newWord
