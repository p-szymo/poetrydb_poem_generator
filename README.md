# auto_pometizer, a Markov-chain poetry generator
After gathering all the poetry available from [PoetryDB](https://github.com/thundercomb/poetrydb), I turned it into a text file as one long string (with lines separated by *\n*).

I created a dictionary with each word in the string as a key and a list of the words that immediately follow each of those key words in the string. I had to do some switcharoo maneuvering to include *\n*s and *\t*s among the keys and within the values of the poem dictionary.
  
I created a function prompting users to input a word count (1000 or fewer words, **note: *\n*s and *\t*s are included in the count**).


## How it works

The poetry generator randomly chooses its first word from the dictionary's keys, then a random word within that key's value, which becomes the next word and the next key; it then chooses a random word within that second word's value, which becomes the next work and the next key, and on and on until the word count is reached.

I also created an optional *to_rhyme* setting that employs the rhyming function from Allison Parrish's [pronouncing](https://github.com/aparrish/pronouncingpy) to change words at the end of every line, randomly throughout the generated text, and all the words within the generated text.


## Next steps
- Build and deploy a user-friendly app.


## List of files
- **poem_generator_workbook.ipynb** - the main workbook, polished, from beginning to end. One can start by opening from the JSON file.
- **functions.py** - text file with functions, from api calls to the final poetry generator.
- **poems_dictionary.json** - the hero poetry dictionary.
- **poems_raw.txt** - the initial string compiled from PoetryDB.
- **scrap_files** folder - backups, old workbooks, old texts/jsons, and other scraps

  - includes NLTK-tokenized version of dictionary with some punctuation (poetic apostrophes and hyphens)
  
    - lacks some proper segmentation but not as oversegmented as the wordninja version
