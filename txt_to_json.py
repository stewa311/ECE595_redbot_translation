import json

'''
super quick program that removes duplicate entries and transfers the words from the .txt files to json arrays
'''

if __name__ == '__main__':
    langs = ['eng', 'fra', 'ita', 'lat', 'por', 'spa']
    for lang in langs:
        with open(lang + '.txt', 'r') as fptr:
            words = fptr.read().splitlines()

        #remove duplicate words
        words = list(set(words))
        
        with open(lang+'.json', 'w') as fptr:
            json.dump(words, fptr)