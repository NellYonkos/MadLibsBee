#sample dictionaries
import re
import random

letterpots = {
    "ehprsyz": [
        "zephyrs",
        "zephyr",
        "hypers",
        "sphery",
        "sypher",
        "hyper",
        "hypes",
        "preys",
        "pyres",
        "shyer",
        "spyre",
        "espy",
        "heps",
        "hers",
        "hery",
        "hesp",
        "heys",
        "hyes",
        "hype",
        "hyps",
        "pehs",
        "prey",
        "prez",
        "prys",
        "pyes",
        "pyre",
        "rehs",
        "reps",
        "resh",
        "ryes",
        "rype",
        "spry",
        "sype",
        "syph",
        "yeps",
        "zeps"
    ]
}


def totalpoints(letterpot):
    """Calculate whole number point value for each letter in letter pot based on
    frequency. More rare = more points. Max value is 10 points, minimum value is
    1.

    Args:
        letterpot (dict): A dictionary with 7 character string as the key 
        and a list of strings as value. The list of strings is all of the 4+ 
        letter words that can be made with the 7 characters. 
        
    Returns:
        letterpoints (dict): A dictionary with single letter strings as keys, 
        and integer game point values as the mapped value. Game points are 
        between 1-10. 10 being the rarest letter, 1 being the most common. 
        If there is an equal proportion of all letters in letterpots.
    """
    
    
    #get count of each letter in all letterpot words
    words = letterpots[letterpot]
    lettercount = {}
    for word in words:
        for letter in word:
            if letter in lettercount:
                lettercount[letter] += 1
            else:
                lettercount[letter] = 1
    
    #calculate total count of letters in letterpot
    totalletters = sum(lettercount.values())
    
    #calculate relative freq of letters in letterpot
    letterproportion = {}
    for letter in lettercount:
        letterproportion[letter] = lettercount[letter]/totalletters
    
    #least/most common letter
    minfreq = min(letterproportion.values())
    maxfreq = max(letterproportion.values())
    
    #calculate each letter's point value
    letterpoints = {}
    for letter in letterproportion:
        if maxfreq == minfreq:
            letterpoints[letter] = 10
        else:
            score = (maxfreq - letterproportion[letter]) / (maxfreq - minfreq) #0-1 scale
            letterpoints[letter] = round(1 + score * 9, 0) #10-1 scale

    return(letterpoints)
    
def extract_placeholders(story):
    """
    Extracts all placeholder words from a story that represent missing parts of speech.

    A placeholder is defined as a part of speech followed by a number (example: 'noun1', 'verb2').
    This function looks for whole words in that format and returns them as a list.

    Args:
        story (str): The input story containing placeholders for missing words.

    Returns:
        list: A list of placeholder strings found in the story (e.g., ['noun1', 'verb2']).
    """
    return re.findall(r'\b(?:noun|verb|adjective|pronoun|plural noun)\d+\b', story)

def help(letterpot):
    """Takes the words out of a dictionary of words corresponding to the chosen
    7 letters and filters out the guessed words. Prints out a word that has been
    randomly chosen from the unguessed words as the first and last letters of 
    the word with the middle letters being unknown.

    Args:
        letterpot (str): A dictionary with 7 character string as the key 
        and a list of strings as value. The list of strings is all of the 4+ 
        letter words that can be made with the 7 characters. (This will most 
        likely be done in a class, but is here for interim deliverable)
    """
    
    #Initializes a dictionary for the words and a list of guesses made
    #This will most likely be done in a class (not directly in here)
    words = letterpots[letterpot]
    guessed_words = []
    
    #Initialized a new list then appends unguessed words to that list
    temp_list = []
    for word in words:
        if word not in guessed_words and word not in temp_list:
            temp_list.append(word)
            
    #Pulls a random word out of the temporary list and uses it as a help word
    help_word = random.choice(temp_list)
    temp_list.remove(help_word)
    
    #Create a length of the word where the middle letters are the "-" symbol
    space_length = (len(help_word) - 2) * "-"
    
    #Print the first and last letters of the word with the middle "-" symbols
    print(f"Here is your hint\n{help_word[0] + space_length + help_word[-1]}")
    
#totalpoints("ehprsyz")


