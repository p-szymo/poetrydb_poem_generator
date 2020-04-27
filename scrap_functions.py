import requests
import json
import string
import re
import random

def author_grabber(url):
    authors = requests.get(url)
    authors = [author for author in authors.json()['authors']]
    return authors

def title_grabber(author):
    base_url = "http://poetrydb.org/author/"
    url_addon = (author + '/title').replace(" ", "%20")
    try:
        titles = requests.get(base_url + url_addon)
        titles = [title['title'] for title in titles.json()]
    except:
        print(author)
        pass
    return titles

### experimentation with keeping hyphens, apostrophes, and ampersands did not pan out
def poem_grabber(title):
    base_url = 'http://poetrydb.org/title/'
    url_addon = (title + '/lines.json').replace(" ", "%20").replace(')', '').replace(']', '').split('/', 1)[0].split('^', 1)[0]
    mod_punct = '!"#$%\()*+,./:;<=>?@[\\]^_`{|}~'
    try:
        response = requests.get(base_url + url_addon)
        lines = response.json()[0]['lines']
        poem = ' \n '.join(lines).lower()
        for mark in mod_punct:
            poem = poem.replace(mark, '') 
        poem = poem.replace('  ', '\t ').replace('--', '').replace('—', '').replace('‘','').replace('’','').replace(
                            "' ", " ").replace(" '", " ")
    except:
        print(title)
        pass
    return poem

def lines_tabs_creator(po_dict):
    new_line = 'airplane'
    tab = 'automobile'
    for word, followers in po_dict.items():
        for i,follower in enumerate(followers):
            if follower == new_line:
                followers[i] = '\n'
            elif follower == tab:
                followers[i] = '\t'
            else:
                continue
    return po_dict

def word_quantifier():
    word_count = int(input("What length doth thy sweet nothings require? "))
    while word_count > 1000:
        word_count = int(input("Surely thine sweet nothings require less breadth!\nCease skylarking and present me a length of reason! "))
    return word_count

def auto_pometizer(po_dict):
    word_count = word_quantifier()
    auto_pome = []
    first_word = random.choice(list(po_dict.keys()))
    auto_pome.append(first_word)
    while len(auto_pome) < word_count:
        next_word = random.choice(po_dict[auto_pome[-1]])
        auto_pome.append(next_word)
    print('\n\n\n ' + (' ').join(auto_pome))