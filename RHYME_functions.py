import requests
import json
import string
import re
import random
import pronouncing as pr


## call API and create a list of authors
def author_grabber(url):
#     url = "http://poetrydb.org/author"
    authors = requests.get(url)
    authors = [author for author in authors.json()['authors']]
    return authors


## call API and create a list of poem titles for each author
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


## call API and create a list of the lines of a poem
## convert list to a string, joining them with '\n' 
def poem_grabber(title):
    base_url = 'http://poetrydb.org/title/'
    url_addon = (title + '/lines.json').replace(" ", "%20").replace(')', '').replace(']', '').split('/', 1)[0].split('^', 1)[0]
    try:
        response = requests.get(base_url + url_addon)
        lines = response.json()[0]['lines']
        poem = " \n ".join(lines).lower()
        poem = poem.translate(str.maketrans('', '', string.punctuation)).replace(
            '  ', '\t ').replace('—', '').replace('‘','').replace('’','')
    except:
        print(title)
        pass
    return poem


## temporarily change newline and tab characters so they don't disappear during segmentation
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


## ask the user to provide a length for the poem (in numerals)
def word_quantifier():
    while True:
        try:
            word_count = int(input("What length doth thy sweet nothings require? "))
            while word_count > 1000:
                word_count = int(input("Surely thine sweet nothings require less breadth!\nCease skylarking and present me a length of reason! "))
        except ValueError:
            print("Art thou a dullard? Enumerate!")
            continue
        else:
            break
    return word_count


## generate poetry from dictionary of words that appear in the PoetryDB's archive of poems
def auto_pometizer(po_dict):
    word_count = word_quantifier()
    auto_pome = []
    first_word = random.choice(list(po_dict.keys()))
    auto_pome.append(first_word)
    while len(auto_pome) < word_count:
        next_word = random.choice(po_dict[auto_pome[-1]])
        auto_pome.append(next_word)
    print('\n\n\n ' + (' ').join(auto_pome))


## swaps the last words of each line for a rhyming word, if there are any rhymes available
def auto_pometizer_endline_rhymer(po_dict):
    word_count = word_quantifier()
    auto_pome = []
    first_word = random.choice(list(po_dict.keys()))
    auto_pome.append(first_word)
    while len(auto_pome) < word_count:
        next_word = random.choice(po_dict[auto_pome[-1]])
        auto_pome.append(next_word)
        if auto_pome[-1] == '\n':
            try:
#                 print(auto_pome[-2]) # uncomment both print statements if you want proof of rhyming
                rhyme_words = pr.rhymes(auto_pome[-2])
                auto_pome[-2] = random.choice(rhyme_words)
#                 print(auto_pome[-2]) # uncomment both print statements if you want proof of rhyming
            except:
                pass
    print('\n\n\n ' + (' ').join(auto_pome))


## swaps a random word for a rhyming word, if there are any rhymes available
def auto_pometizer_random_rhymer(po_dict):
    word_count = word_quantifier()
    auto_pome = []
    first_word = random.choice(list(po_dict.keys()))
    auto_pome.append(first_word)
    while len(auto_pome) < word_count:
        next_word = random.choice(po_dict[auto_pome[-1]])
        auto_pome.append(next_word)
        if auto_pome[-1] == '\n':
            try:
                random_num = random.choice(range(len(auto_pome)))
#                 print(auto_pome[random_num], random_num) # uncomment both print statements if you want proof of rhyming
                rhyme_words = pr.rhymes(auto_pome[random_num])
                auto_pome[random_num] = random.choice(rhyme_words)
#                 print(auto_pome[random_num]) # uncomment both print statements if you want proof of rhyming
            except:
                pass
    print('\n\n\n ' + (' ').join(auto_pome))
    

## rhymes everything it possibly can
def auto_pometizer_full_rhymer(po_dict):
    word_count = word_quantifier()
    
    auto_pome = []
    first_word = random.choice(list(po_dict.keys()))
    auto_pome.append(first_word)
    while len(auto_pome) < word_count:
        next_word = random.choice(po_dict[auto_pome[-1]])
        auto_pome.append(next_word)
        
    auto_rhymed = []
    for word in auto_pome:
        try:
            rhyme_word = random.choice(pr.rhymes(word))
            auto_rhymed.append(rhyme_word)
        except:
            auto_rhymed.append(word)
        
    print('\n\n\n ' + (' ').join(auto_rhymed))
