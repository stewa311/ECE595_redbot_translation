import requests
import random
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import parse_qs
from unidecode import unidecode
from time import sleep

_url = 'https://www.ezglot.com/words-starting-with.php' #the international wordle dictionary I'm referencing
alphabet = 'abcdefghijklmnopqrstuvwxyz'
languages = ['eng', 'fra', 'ita', 'lat', 'por', 'spa']
all_urls = [] 

'''
The website lists all of the 5 letter words as links to their own dictionary pages,
so I just search for those urls and snag the word parameter from it
There's probably a much cleaner way to do it but I'm pretty inexperienced with this stuff
'''

while len(all_urls) == 0:
    #loop in case letter/country combo doesn't have any existing words
    letter = alphabet[random.randint(0,25)] #pick random letter
    language = random.choice(languages) #pick random language
    _params = {'w' : letter,'l' : language, 'length' : '5'}
    r = requests.get(url = _url, params = _params)
    data = BeautifulSoup(r.content, 'html5lib') 
    all_urls = data.find("body").find_all("ul")[1].find_all('a', href=True) #it's ugly, but this line returns all of the dictionary page links
    
print('Finding all 5 letter words in ' + language + ' that start with ' + letter + '\n')
sleep(2)

for url in all_urls:
    parsed_url = urlparse(url['href']) #parse the url to find the actual word name
    word = parse_qs(parsed_url.query)['w'][0]
    print(unidecode(word)) 
    '''
    unidecode removes the accents from all of the letters.
    We can keep the accents on words if we want to display them, 
    but at some point in the process we'll need to use this function to compare letters and whatnot
    '''


    