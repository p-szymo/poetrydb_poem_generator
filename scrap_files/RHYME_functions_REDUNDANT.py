import requests
import json
import string
import re
import random
import pronouncing as pr


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
