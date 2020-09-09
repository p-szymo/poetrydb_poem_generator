import requests
import json
import string
import re
import random
import pronouncing as pr


# call API and create a list of authors
def author_grabber(url):
    '''
    Function to retrieve a list of authors available on PoetryDB.


    Input
    -----
    url : str
        For PoetryDB, use:
        `https://poetrydb.org/author`


    Output
    ------
    authors : list (str)
        List of poet names with poems available on PoetryDB.

    '''

    # API request
    authors = requests.get(url)

    # create and return a list of author names
    authors = [author for author in authors.json()['authors']]

    return authors


# call API and create a list of poem titles for each author
def title_grabber(author):
    '''
    Function to retrieve a list of poem titles available on PoetryDB from a particular poet.


    Input
    -----
    author : str
        Preprocessed name of poet with poems on PoetryDB.
        Example: `Walt Whitman`.


    Output
    ------
    titles : list (str)
        List of poem titles available on PoetryDB.

    '''

    # required beginning to the URL
    base_url = 'https://poetrydb.org/author/'

    # reformat author name to URL requirements, adding title argument
    # replacing spaces
    url_addon = (author + '/title').replace(' ', '%20')

    # API request and list creation
    try:
        titles = requests.get(base_url + url_addon)
        titles = [title['title'] for title in titles.json()]

    # if an error occurs, print author name
    except BaseException:
        print(author)
        pass

    # return titles list
    return titles


# call API and create a list of the lines of a poem
# convert list to a string, joining them with '\n'
def poem_grabber(title, remove_punct=True):
    '''
    Function to scrape a poem that is available on PoetryDB. Poem is a series of lines 
    joined by `\n` into a single string.


    Input
    -----
    title : str
        Preprocessed title of poem on PoetryDB.
        Example: `A Song of Autumn`.


    Optional input
    --------------
    remove_punct : bool
        Whether to remove all punctuation from the returned poem (default=True).


    Output
    ------
    poem : str
        List of poem titles available on PoetryDB.

    Prints any poem titles that weren't successfully scraped.

    '''

    # required beginning to the URL
    base_url = 'https://poetrydb.org/title/'

    # UPDATE: reformat title name to disregard anything after a parenthesis or
    # bracket
    if '(' in title:
        title_prepped = re.sub(" *\\(.*", "", title)
    elif '[' in title:
        title_prepped = re.sub(" *\\[.*", "", title)
    else:
        title_prepped = title

    # reformat title name to URL requirements, adding lines.json argument, replacing 
    # various characters, and accounting for special cases
    url_addon = (
        title_prepped +
        '/lines.json').replace(
        ' ',
        '%20').replace(
            ')',
            '').replace(
                ']',
                '') .split(
                    '/',
                    1)[0].split(
                        '^',
        1)[0]

    try:
        # API request
        response = requests.get(base_url + url_addon)
        # create list
        lines = response.json()[0]['lines']
        # join list to a string, make lowercase, deal with certain characters,
        # and replace long spaces with tabs
        poem = " \n ".join(lines).lower().replace(
            "’",
            "'").replace(
            "‘",
            "'").replace(
            '-',
            ' '). replace(
                '—',
                ' ').replace(
                    '  ',
            ' \t ')

        if remove_punct:
            # remove punctuation (optional)
            poem = poem.translate(str.maketrans('', '', string.punctuation))

    # if an error occurs, print title and make the poem a tab
    except BaseException:
        print(title)
        poem = '\t'

    # return poem as string
    return poem


# revert endline and tab characters
def lines_tabs_creator(po_dict, endline_sub, tab_sub):
    '''
    Function to revert endline (`\n`) and tab (`\t`) substitutions to their respective 
    characters within a Markov dictionary.

    Substitutions should have been made to the pre-tokenized string on which the 
    dictionary is based.


    Input
    -----
    po_dict : dict
        Markov chain dictionary with strings as keys and lists of strings as values.

    endline_sub : str
        Characters used as substitution for `\n`.

    tab_sub : str
        Characters used as substitution for `\t`.


    Output
    ------
    po_dict : str
        Markov chain dictionary with endline and tab characters.

    '''

    # iterate through dictionary
    for word, followers in po_dict.items():

        # iterate through each value's list
        for i, follower in enumerate(followers):

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


# ask the user to provide a length for the poem (in numerals)
def word_quantifier(max_count):
    '''
    Function to interact with user and obtain their desired word count.

    Continually interacts with user until an integer below a certain value is imputed.


    Input
    -----
    max_count : int
        Maximum limit of words a user may request.


    Output
    ------
    word_count : int
        Number of words requested by user.

    '''

    # instantiate a while loop that breaks when conditions are satisfied
    while True:

        # input the number of words desired (converting string input to
        # integer)
        try:
            word_count = int(
                input('What length doth thy sweet nothings require? '))

            # if input greater than 1000, prompt user to ask for fewer
            while word_count > max_count:
                word_count = int(input(
                    'Surely thine sweet nothings require less breadth!\nCease skylarking and present me a length of reason! '))

        # if input other than a number, prompt user to try again
        except ValueError:
            print('Art thou a dullard? Enumerate!')
            continue

        # don't recall the point of this...
        else:
            break

    # return user input
    return word_count


# generate poetry from Markov dictionary
def auto_pometizer(po_dict, max_count=1000, to_rhyme=None, to_print=True):
    '''
    Interactive function to generate a string of text using a Markov dictionary.

    Optional ability to replace words with a randomly chosen rhyme.


    Input
    -----
    po_dict : dict
        Markov chain dictionary with strings as keys and lists of strings as values.


    Optional input
    --------------
    max_count : int
        Maximum limit of words a user may request (default=1000).

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

    # ask user for number of words and store value
    word_count = word_quantifier(max_count)

    # instantiate an empty list
    auto_pome = []

    # initialize a random word from dictionary's keys
    first_word = random.choice(list(po_dict.keys()))

    # add that word to the list
    auto_pome.append(first_word)

    # while loop to run until word count is reached
    while len(auto_pome) < word_count:

        # randomly choose next word from previous word's value (list of words
        # that follow)
        next_word = random.choice(po_dict[auto_pome[-1]])

        # add to list
        auto_pome.append(next_word)

        # if rhyme replacements chosen
        if to_rhyme:

            # if 'endline' chosen
            if to_rhyme == 'endline':

                # check if previous "word" was endline character
                if auto_pome[-1] == '\n':

                    # replace word before endline character with a random
                    # rhyme, if available
                    try:
                        rhyme_words = pr.rhymes(auto_pome[-2])
                        auto_pome[-2] = random.choice(rhyme_words)

                    # if no rhyme available, move on
                    except BaseException:
                        pass

            # if 'random' chosen
            elif to_rhyme == 'random':

                # still uses previous "word" being endline character to
                # initiate choosing a random word to replace
                if auto_pome[-1] == '\n':

                    # replace random word within generated words with a random
                    # rhyme, if available
                    try:
                        random_num = random.choice(range(len(auto_pome)))
                        rhyme_words = pr.rhymes(auto_pome[random_num])
                        auto_pome[random_num] = random.choice(rhyme_words)

                    # if no rhyme available, move on
                    except BaseException:
                        pass

            # if 'all' chosen, the function will do rhyme replacements after
            # original generation is complete
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

            # replace each with a random rhyme (if available) and add to new
            # list
            try:
                rhyme_word = random.choice(pr.rhymes(word))
                auto_rhymed.append(rhyme_word)

            # if not available, add original word to new list
            except BaseException:
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
