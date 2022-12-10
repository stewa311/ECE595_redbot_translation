import json
import requests
from bs4 import BeautifulSoup

'''
Program takes language json files and filters out all words that are either popular names or
exclusively listed as proper nouns on their EZ Glot definition page 
'''


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
        
    languages = ['eng', 'fra', 'ita', 'lat', 'por', 'spa']
    for lang in languages:
        print('\n\nFiltering ' + lang + '...\n\n')
        with open(lang +'.json') as file:
            words = json.load(file)
        words = filter_names(words,names) #filter out names from SSA list
        
        goodWords = []
        badWords = []   
        lenWords = len(words)
        i = 1
        for word in words:
            print(i, '/', lenWords) #keep track of where the program is for my own sanity
            i += 1
            properNoun = True
            _url = 'https://www.ezglot.com/words.php?l=' + lang + '&w=' + word
            r = requests.get(url = _url)
            try:
                #all words should have a valid dictionary table but for some reason errors pop up one out of every few thousand so I added a try/except statement
                data = BeautifulSoup(r.content, 'html5lib').find_all('ul')[1]
                for li in data.find_all("li"):
                    if len(li.text) > 11:
                        if li.text[:11] != "Proper noun":
                            #keep words that have any non-proper noun definitions
                            properNoun = False
                            break
                if not properNoun:
                    goodWords.append(word)
            except:
                pass

                
        with open(lang + '.json', 'w') as fptr:
                    json.dump(goodWords, fptr)
                
