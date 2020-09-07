import requests
import json
import string
import re
import random
import pronouncing as pr


## call API and create a list of authors
def author_grabber(url):
    
    '''Input necessary PoetryDB URL ('https://poetrydb.org/author') to retrieve a list of available authors.'''

    # API request
    authors = requests.get(url)
    
    # create and return a list of author names
    authors = [author for author in authors.json()['authors']]
    return authors


## call API and create a list of poem titles for each author
def title_grabber(author):
    
    '''Input an author's name as a string.
       Output a list of all titles associated with that author.'''
    
    # required beginning to the URL
    base_url = 'https://poetrydb.org/author/'
    
    # reformat author name to URL requirements, adding title argument replacing spaces
    url_addon = (author + '/title').replace(' ', '%20')
    
    # API request and list creation
    try:
        titles = requests.get(base_url + url_addon)
        titles = [title['title'] for title in titles.json()]
        
    # if an error occurs, print author name
    except:
        print(author)
        pass
    
    # return titles list
    return titles


## call API and create a list of the lines of a poem
## convert list to a string, joining them with '\n' 
def poem_grabber(title, remove_punct=True):
    
    '''Input a poem title as a string.
       Output poem as a '\n'-separated string.'''
    
    # required beginning to the URL
    base_url = 'https://poetrydb.org/title/'
    
    # UPDATE: reformat title name to disregard anything after a parenthesis or bracket
    if '(' in title:
        title_prepped = re.sub(" *\\(.*", "", title)
    elif '[' in title:
        title_prepped = re.sub(" *\\[.*", "", title)
    else:
        title_prepped = title
    
    # reformat title name to URL requirements, adding lines.json argument, replacing various characters,
    # and accounting for special cases
    url_addon = (title_prepped + '/lines.json').replace(' ', '%20').replace(')', '').replace(']', '')\
                                                .split('/', 1)[0].split('^', 1)[0]
    
    try:
        # API request
        response = requests.get(base_url + url_addon)
        # create list
        lines = response.json()[0]['lines']
        # join list to a string, make lowercase, deal with certain characters, 
        # and replace long spaces with tabs
        poem = " \n ".join(lines).lower().replace("’", "'").replace("‘","'").replace('-', ' ').\
                                            replace('—', ' ').replace('  ', ' \t ')
        
        if remove_punct:
            # remove punctuation (optional)
            poem = poem.translate(str.maketrans('', '', string.punctuation))
        
    # if an error occurs, print title and make the poem a tab
    except:
        print(title)
        poem = '\t'
        
    # return poem as string
    return poem


## revert endline and tab characters back into dictionary
def lines_tabs_creator(po_dict, endline_sub, tab_sub):
    
    '''Input a Markov dictionary with strings that were used as substitutes for endline and tab characters.
       Output a dictionary with endline and tab characters back in their rightful place.'''
    
    # iterate through dictionary
    for word, followers in po_dict.items():
        
        # iterate through each value's list
        for i,follower in enumerate(followers):
            
            # replace endline substitution with endline character 
            if follower == endline_sub:
                followers[i] = '\n'
                
            # replace tab substitution with tab character 
            elif follower == tab_sub:
                followers[i] = '\t'
            
            # skip over other characters
            else:
                continue
    
    # return dictionary with re-replaced terms
    return po_dict


## ask the user to provide a length for the poem (in numerals)
def word_quantifier():
    
    '''No input necessary. Function to interact with user and obtain a desired word count.'''
    
    # instantiate a while loop that breaks when conditions are satisfied
    while True:
        
        # input the number of words desired (converting string input to integer)
        try:
            word_count = int(input('What length doth thy sweet nothings require? '))
            
            # if input greater than 1000, prompt user to ask for fewer
            while word_count > 1000:
                word_count = int(input('Surely thine sweet nothings require less breadth!\nCease skylarking and present me a length of reason! '))
                
        # if input other than a number, prompt user to try again
        except ValueError:
            print('Art thou a dullard? Enumerate!')
            continue
            
        # don't recall the point of this...
        else:
            break
            
    # return user input
    return word_count


## generate poetry from dictionary of words that appear in the PoetryDB's archive of poems
def auto_pometizer(po_dict, to_rhyme=None, to_print=True):
    
    '''Input Markov dictionary.
       Optional input using rhyme replacements -- choose one from: ['endline', 'random', 'all']. Defaults to no replacements.
       Output generated poem. Defaults to also printing generated poem.'''
    
    # ask user for number of words and store value
    word_count = word_quantifier()
    
    # instantiate an empty list
    auto_pome = []
    
    # initialize a random word from dictionary's keys
    first_word = random.choice(list(po_dict.keys()))
    
    # add that word to the list
    auto_pome.append(first_word)
    
    # while loop to run until word count is reached
    while len(auto_pome) < word_count:

        # randomly choose next word from previous word's value (list of words that follow)
        next_word = random.choice(po_dict[auto_pome[-1]])

        # add to list
        auto_pome.append(next_word)
    
        # if rhyme replacements chosen
        if to_rhyme:

            # if 'endline' chosen
            if to_rhyme == 'endline':

                # check if previous "word" was endline character
                if auto_pome[-1] == '\n':

                    # replace word before endline character with a random rhyme, if available
                    try:
                        rhyme_words = pr.rhymes(auto_pome[-2])
                        auto_pome[-2] = random.choice(rhyme_words)

                    # if no rhyme available, move on
                    except:
                        pass
              
            # if 'random' chosen
            elif to_rhyme == 'random':
                
                # still uses previous "word" being endline character to initiate choosing a random word to replace
                if auto_pome[-1] == '\n':
                    
                    # replace random word within generated words with a random rhyme, if available
                    try:
                        random_num = random.choice(range(len(auto_pome)))
                        rhyme_words = pr.rhymes(auto_pome[random_num])
                        auto_pome[random_num] = random.choice(rhyme_words)
        
                    # if no rhyme available, move on
                    except:
                        pass
            
            # if 'all' chosen, the function will do rhyme replacements after original generation is complete
            else:
                pass
                
        # default (no rhyme replacements)
        else:
            continue
    
    # if 'all' chosen
    if to_rhyme == 'all':
        
        # instantiate empty list
        auto_rhymed = []
        
        # loop over original generated words list
        for word in auto_pome:
            
            # replace each with a random rhyme (if available) and add to new list
            try:
                rhyme_word = random.choice(pr.rhymes(word))
                auto_rhymed.append(rhyme_word)
                
            # if not available, add original word to new list
            except:
                auto_rhymed.append(word)
                
        # turn list into string
        auto_rhymed = (' ').join(auto_rhymed)
        
        # print string (poem!)
        if to_print:
            print('\n\n\n ' + auto_rhymed)
        
        # return string (poem!)
        return auto_rhymed
    
    # if no rhyme replacements or 'endline' or 'random'
    else:
        # turn list into string
        auto_pome = (' ').join(auto_pome)
        
        # print string (poem!)
        if to_print:
            print('\n\n\n ' + auto_pome)
        
    # return string (poem!)
    return auto_pome