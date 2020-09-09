# [auto_pometizer](https://polar-earth-97611.herokuapp.com/), a Markov chain poetry generator
After gathering all the poetry available from [PoetryDB](https://github.com/thundercomb/poetrydb), I turn it into a text file as one long string (with lines separated by ```\n```).

I then create a dictionary with each word in the string as a key and a list of the words that immediately follow each of those key words in the string. I had to do some switcharoo maneuvering to include newline (```\n```) and tab (```\t```) characters among the keys and within the values of the poem dictionary.
  
Within the auto-pometizer function, you can then input a word count (1000 or fewer words, *note: newline and tab characters are included in the count*), as well as whether or not to use a rhyming function (of which there are three varieties).

Best of all, it is now an [app](https://polar-earth-97611.herokuapp.com/)!

## To use the app locally, run the following in Terminal (after cloning the repo):
```streamlit run app.py```


## How it works

The poetry generator randomly chooses its first word from the dictionary's keys, then a random word within that key's value, which becomes the next word and the next key; it then chooses a random word within that second word's value, which becomes the next word and the next key, and on and on until the word count is reached.

Within the ```auto_pometizer``` function, the optional ```to_rhyme``` argument employs the rhyming function from Allison Parrish's [Pronouncing](https://github.com/aparrish/pronouncingpy) to change words at the end of every line (```to_rhyme='endline'```), randomly throughout the generated text (```to_rhyme='random'```), and all the words within the generated text (```to_rhyme='all'```).


## List of files
- **scrap_files** folder - backups, old workbooks, old texts/jsons, and other scraps.
  - includes NLTK-tokenized version of dictionary with some punctuation (poetic apostrophes and hyphens)
    - lacks some proper segmentation but not as oversegmented as the wordninja version
- **.gitignore** - list of files to ignore.
- **Procfile** - requirement for Heroku deploy.
- **README.md** - this very file!
- **app.py** - file with app layout and auto_pometizer function (reconfigured for use with Streamlit).
- **auto_pometizer.ipynb** - the main workbook, polished, from beginning to end. One can start by opening from the Markov dictionary.
- **functions.py** - text file with functions, from API calls to the final poetry generator.
- **poems_dictionary.json** - the hero poetry dictionary.
- **poems_raw.txt** - the initial string compiled from PoetryDB.
- **requirements.txt** - requirement for Heroku deploy.
- **scraping_sandbox.ipynb** - notebook with an example of scraping the work of one particular poet.
- **setup.sh** - requirement for Heroku deploy.
