import requests
import random
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import parse_qs
from unidecode import unidecode
from time import sleep


def good_word(word, lang):
    #looks up a word's dictionary page -- returns True if there is a valid definition. False otherwise
    _url = 'https://www.ezglot.com/words.php?l=' + lang + '&w=' + word
    r = requests.get(url = _url)
    data = BeautifulSoup(r.content, 'html5lib') 
    if data.find('h4', id='definitions') != None:
        return True
    return False

if __name__ == '__main__':
    
    _url = 'https://www.ezglot.com/words-starting-with.php' #the international wordle dictionary I'm referencing
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    languages = ['eng', 'fra', 'ita', 'lat', 'por', 'spa']
    
    for language in languages:
        with open(language + '.txt', 'w') as fptr:
            #create a .txt file with in the local path
            for letter in alphabet:
                print(language  + ' : ' + letter) #keep track of where the program is
                
                '''
                The website lists all of the 5 letter words as links to their own dictionary pages,
                so I just search for those urls and snag the word parameter from it
                There's probably a much cleaner way to do it but I'm pretty inexperienced with this stuff
                '''
                _params = {'w' : letter,'l' : language, 'length' : '5'}
                r = requests.get(url = _url, params = _params)
                data = BeautifulSoup(r.content, 'html5lib') 
                all_urls = data.find('body').find_all('ul')[1].find_all('a', href=True) #it's ugly, but this line returns all of the dictionary page links
                if len(all_urls) == 0:
                    continue 
                for url in all_urls:
                    parsed_url = urlparse(url['href']) #parse the url to find the actual word name
                    word = parse_qs(parsed_url.query)['w'][0]
                    if good_word(word,language):
                        fptr.write(unidecode(word) + '\n') #unidecode gets rid of accents
