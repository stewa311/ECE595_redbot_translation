import json

def filter_names(words,names):
    #filter out any of the words that are just names
    _words = []
    for word in words:
        if word not in names:
            _words.append(word)
    return _words

if __name__ == '__main__':
    with open('names.txt') as fptr:
        #names.txt is a filtered version of the list of all 2021 baby names provided by the social security administration
        names = set(fptr.read().splitlines()) 


    langs = ['eng', 'fra', 'ita', 'lat', 'por', 'spa']
    for lang in langs:
        with open(lang + '.txt', 'r') as fptr:
            words = fptr.read().splitlines()

        #remove duplicate words
        words = list(set(words))
        words = filter_names(words,names)
        
        with open(lang+'.json', 'w') as fptr:
            json.dump(words, fptr)
