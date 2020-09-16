# app building library
import streamlit as st

# necessary libraries
import json
import random
import pronouncing as pr


## generate poetry from dictionary of words that appear in the PoetryDB's archive of poems
def auto_pometizer(po_dict, word_count, to_rhyme=None):


    '''
    Interactive function to generate a string of text using a Markov dictionary.

    Optional ability to replace words with a randomly chosen rhyme.


    Input
    -----
    po_dict : dict
        Markov chain dictionary with strings as keys and lists of strings as values.

    word_count : int
        Number of words requested by user.


    Optional input
    --------------
    to_rhyme : str
        Type of rhyming replacements to employ (default=None).

        Choose one of: [None, 'endline', 'random', 'all']

        If `None`, no replacements are made.
        If `endline`, converts words before endline (`\n`) character to randomly 
        chosen rhyme, if available.
        If `random`, randomly chooses a word, after an endline (`\n`) character is 
        generated, to be replaced by a randomly chosen rhyme, if available.
        If `all`, converts all words to randomly chosen rhyme, if available.

    to_print : bool
        Whether to print the generated poem (default=True).


    Output
    ------
    auto_poem : str
        Generated string of text including `\n` and `\t` characters.

    '''
    
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
        
        # return string (poem!)
        return auto_rhymed
    
    # if no rhyme replacements or 'endline' or 'random'
    else:
        # turn list into string
        auto_pome = (' ').join(auto_pome)
        
    # return string (poem!)
    return auto_pome



# open big dictionary!
with open("poems_dictionary.json", "r") as hello:
    poems_dictionary = json.load(hello)
    
    
# message from the recommender-bot
st.title('auto_pometizer beckons you.')
st.header('"Hark! I offer a most ineffable verse."')
st.subheader('Should thou seek further refinement, amend my tunings larboard.')

# number of poem recommendations in sidebar
# NOTE: text in separate markdown because couldn't figure out
# how to change font size within number_input
st.sidebar.markdown('#### What length doth thy sweet nothings require?')
num_option = st.sidebar.number_input(
	'',
	# set min/max values and default value of 100
	min_value=1, max_value=1000, value=50)

# format blank space
st.sidebar.markdown('')
# format blank space
st.sidebar.markdown('')

# a fateful decision, to filter or not to filter
st.sidebar.markdown('#### Wouldst thou desire rhyming obfuscations?')
to_rhyme_option = st.sidebar.radio(
    '',
    ['no', 'yes'])

# filter parameters in the sidebar
if to_rhyme_option == 'yes':

    # format blank space
    st.sidebar.markdown('')
    # format blank space
    st.sidebar.markdown('')

    # title
    st.sidebar.markdown('#### By which fashion?')
    method_option = st.sidebar.radio(
        '',
        ['endline', 'random', 'all'])

else:
    method_option = None

auto_pome = auto_pometizer(poems_dictionary, word_count=num_option, to_rhyme=method_option)

# format blank space
st.markdown('')
# format blank space
st.markdown('')

if st.button('BEGET!'):
    # format blank space
    st.markdown('')
    # format blank space
    st.markdown('')

    st.text(auto_pome)

