# RUDIMENTARY POETRY GENERATOR
* Gathered all the poetry available from the PoetryDB into a text file as one long string (lines separated by ' \n ').

  * Created a dictionary with each word in the string as a key and a list of the words that immediately follow each of those key words in the string.
  
  * Had to do some switcharoo maneuvering to include '\n's and '\t's among the keys and within the values of the poem dictionary.
  
* Created a function prompting users to input a word count (1000 or fewer words, *note: '\n's and '\t's are included in the count*)

* Poetry generator randomly chooses a first key, then a random word within that key's value, then a random word within that second word's value, until the word count is reached.



## Next steps
* Play around with regex to only strip certain characters from the raw poems string. For example, keep hyphens, apostrophes, etc. within words.

  * Possibly increase frequency of '\t' by re-defining it as 2 spaces instead of 4.
  
* Apply Allison Parrish's [pronouncing](https://github.com/aparrish/pronouncingpy) to certain words.



## List of files
* **functions.py** - text file with functions, from api calls to the final poetry generator.
* **poem_generator_workbook.ipynb** - the main workbook, polished, from beginning to end. One can start by opening from the JSON file.
* **poems_dictionary.json** - the hero poetry dictionary.
* **poems_dictionary.txt** - backed up as a text file.
* **poems_raw.txt** - the initial string compiled from PoetryDB.
