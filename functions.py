import requests
import json
import string
import re
import random

def author_grabber(url):
    authors = requests.get(url)
    authors = [author for author in authors.json()['authors']]
    return authors

# def author_url_creator(author_list):
#     url_addon_author_titles = [('/' + author + '/title').replace(" ", "%20") for author in author_list]
#     return url_addon_author_titles

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

def poem_grabber(title):
    base_url = 'http://poetrydb.org/title/'
    url_addon = (title + '/lines.json').replace(" ", "%20").replace(')', '').replace(']', '').split('/', 1)[0].split('^', 1)[0]
    try:
        response = requests.get(base_url + url_addon)
        lines = response.json()[0]['lines']
        poem = " \n ".join(lines).lower()
        poem = poem.translate(str.maketrans('', '', string.punctuation)).replace(
            '    ', '\t ').replace('  ', ' ').replace('—', '').replace('‘','').replace('’','')
    except:
        print(title)
        pass
    return poem

def lines_tabs_creator(po_dict):
    new_line = 'x2'
    tab = 'y2'
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

def auto_pometizer():
    word_count = word_quantifier()
    auto_pome = []
    first_word = random.choice(list(poems_dictionary.keys()))
    auto_pome.append(first_word)
    while len(auto_pome) < word_count:
        next_word = random.choice(poems_dictionary[auto_pome[-1]])
        auto_pome.append(next_word)
    print('\n\n\n ' + (' ').join(auto_pome))