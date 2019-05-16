#linguistic
## Added the time test
import datetime

## poc
# <https://pypi.org/project/pyspellchecker/> (accessed May 13, 2019)

from spellchecker import SpellChecker
START_TIME = datetime.datetime.now()

def printDifTime(now):
    print(now - START_TIME)
    

spell = SpellChecker()

# find those words that may be misspelled
misspelled = spell.unknown(['something', 'is', 'hapenning', 'here'])
printDifTime(datetime.datetime.now())

for word in misspelled:
    # Get the one `most likely` answer
    print(spell.correction(word))
    printDifTime(datetime.datetime.now())

    # Get a list of `likely` options
    print(spell.candidates(word))
    printDifTime(datetime.datetime.now())

# If the Word Frequency list is not to your liking, you can add additional text to generate a more appropriate list for your use case.

from spellchecker import SpellChecker

spell = SpellChecker()  # loads default word frequency list
spell.word_frequency.load_text_file('./my_free_text_doc.txt')
printDifTime(datetime.datetime.now())

# if I just want to make sure some words are not flagged as misspelled
spell.word_frequency.load_words(['microsoft', 'apple', 'google'])
spell.known(['microsoft', 'google'])  # will return both now!

# If the words that you wish to check are long, it is recommended to reduce the distance to 1. This can be accomplished either when initializing the spell check class or after the fact.

from spellchecker import SpellChecker

spell = SpellChecker(distance=1)  # set at initialization

# do some work on longer words

spell.distance = 2  # set the distance parameter back to the default


# Additional Methods

# On-line documentation is available; below contains the cliff-notes version of some of the available functions:

# correction(word): Returns the most probable result for the misspelled word

# candidates(word): Returns a set of possible candidates for the misspelled word

# known([words]): Returns those words that are in the word frequency list

# unknown([words]): Returns those words that are not in the frequency list

# word_probability(word): The frequency of the given word out of all words in the frequency list
# The following are less likely to be needed by the user but are available:

# edit_distance_1(word): Returns a set of all strings at a Levenshtein Distance of one based on the alphabet of the selected language

# edit_distance_2(word): Returns a set of all strings at a Levenshtein Distance of two based on the alphabet of the selected language

### Time
# >>> import datetime
# >>> datetime.datetime.now()
# datetime.datetime(2009, 1, 6, 15, 8, 24, 78915)

# >>> print(datetime.datetime.now())
# 2018-07-29 09:17:13.812189