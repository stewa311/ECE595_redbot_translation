import json

langs = ['eng', 'fra', 'ita', 'lat', 'por', 'spa']
for lang in langs:
    with open(lang + '.txt', 'r') as fptr:
        words = fptr.read().splitlines()
        
    with open(lang+'.json', 'w') as fptr:
        json.dump(words, fptr)