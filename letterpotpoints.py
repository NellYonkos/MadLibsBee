import re
import random
from argparse import ArgumentParser

letterpots = {
    "ehprsyz": [
        "zephyrs","zephyr","hypers","sphery","sypher","hyper","hypes","preys",
        "pyres","shyer","spyre","espy","heps","hers","hery","hesp","heys",
        "hyes","hype","hyps","pehs","prey","prez","prys","pyes","pyre","rehs",
        "reps","resh","ryes","rype","spry","sype","syph","yeps","zeps"
    ],
    "aerlswy": [
        "lawyers","lawyer", 
        "sawyer","swayer", "sweary","layers", "rayles","relays", "slayer",
        "walers","warsle","rawly","swaly","swayl","weary","wyles","yawls",
        "alews","arsey","aryls","ayres","early","eyras","lawer","layer","leary",
        "lyase","lyres","rayle","relay","resaw","resay","ryals","sawer","sayer",
        "sewar","slyer","swale","sware","sweal","swear","waler","wales","wares",
        "weals","wears","yales","years","arles","earls","laers","lares","laser",
        "lears","rales","reals","seral","awry","sway","swey","waly","wary",
        "ways","weys","wyes","wyle","yawl","yaws","yews","aery","alew","arew",
        "arsy","aryl","awes","awls","ayes","ayre","easy","eyas","eyra","laws",
        "lays","leys","lyes","lyra","lyre","lyse","raws","rays","rely","rews",
        "ryal","ryas","ryes","slaw","slay", "slew","sley","waes","wale","ware",
        "wars","wase","weal","wear","wels","yale","yare","year","yeas","ales",
        "ares","arle","arse","earl","ears","eras","laer","lare","lars","lase",
        "lear","leas","rale","rase","real","sale","seal","sear","sera","slae" 
    ]
}


partofspeech_dict = {
    "noun": [
        "zephyr", "hyper", "hype", "prey", 
        "pyre", "spyre", "prez", "prys", "resh", "rype", "sype", "syph",
        "lawyer", "sawyer", "swayer", "layer", "slayer", "relay", "resaw", "resay", 
        "rayle", "sawer", "sayer", "sewar", "swale", "sware", "sweal", "swear", "waler", 
        "wale", "ware", "wars", "wase", "wear", "laser", "rales", "reals", "seral", 
        "ayre", "alew", "aryl", "eyas", "eyra", "lyase", "lyra", "lyre", "lyse", "ryal", 
        "ryas", "yawl", "aery", "weal", "wale", "year", "sale", "seal", "lear", "rale", 
        "real", "earl", "ears", "arse", "arsey", "swey", "slaw", "slew", "sley", "laws", 
        "lays", "leys", "lyes", "raws", "rays", "rews", "ways", "weys", "wyes", "wyle", 
        "yaws", "yews", "waes", "wels", "laer", "lare", "lars", "lase", "leas", "rase", 
        "sera", "slae", "arle", "ares", "ales"
    ],
    "plural noun": [
        "zephyrs", "hypers", "hypes", "preys", "pyres", "hers", "heps", "heys", 
        "hyes", "pehs", "pyes", "rehs", "reps", "ryes", "yeps", "zeps",
        "lawyers", "layers", "rayles", "relays", "walers", "warsle", "wyles", "yawls", 
        "alews", "aryls", "ayres", "eyras", "lyres", "ryals", "swaly", "swayl", "wales", 
        "wares", "weals", "wears", "yales", "years", "arles", "earls", "laers", "lares", 
        "lears", "yaws", "yews", "ways", "weys", "wyes", "laws", "lays", "leys", "lyes", 
        "raws", "rays", "rews", "ryas"
    ],
    "verb": [
        "hype", "hypes", "prey", "preys", "espy", "heps", "sypher","swear", 
        "wear", "relay", "resaw", "resay", "slay", "sway", "swale", "swer", 
        "sear", "sale", "seal", "lear", "rase", "rely", "slew"
    ],
    "adjective": [
        "hyper", "sphery", "shyer", "spry", "hep","sweary", "weary", "early", 
        "leary", "slyer", "wary", "awry", "arsey", "easy", 
        "rawly", "swaly", "swayl"
    ],
    "pronoun": [
        "hers"
    ]
}

fillerpartofspeech = {
    "noun": [
        "apple","breeze","candle","dragon","forest","island","jungle","mountain",
        "pencil","village"
    ],
    "plural noun": [
        "apples","books","cars","dogs","flowers","houses","islands","kites",
        "stars","trees"
    ],
    "verb": [
        "climb","draw","explore","jump","laugh","paint","run","sing","swim",
        "write"
    ],
    "adjective": [
        "bright","calm","fierce","giant","happy","lazy","quick","shiny","tiny",
        "wild"
    ]}

story = """
Just when it seemed every noun1 under the noun2  had been named, 
researchers at the University of plural noun1, have identified a adjective new 
one. Called "olo", this shade lies outside the normal range of noun3 vision."
"""

class Player:
    """
    A class to represent the player.
    Attributes:
        name (str): Player's name.
        score (int): Player's total score.
        guessed_words (list): List of valid words the player has guessed.
    """
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.guessed_words = []

    def add_score(self, points):
        self.score += points

    def guess_word(self, word):
        self.guessed_words.append(word)
    
    def pos_guess(self, partofspeech_dict):
        pos = {"noun":[], "plural noun":[], "verb":[], "adjective":[]}
        for word in self.guessed_words:
            count = 0
            for i in partofspeech_dict:
                if word in partofspeech_dict[i]:
                    pos[i].append(word)
                    count += 1
            if count == 0:
                pass
        return pos

    def __str__(self):
        return f"{self.name}: {self.score} points"


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
        
    Skill from list: 
        use of a key function (which can be a lambda expression) with the 
        following commands:  min(), max()
        
    Written by: Nell Yonkos
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
    
    #least/most common letter using min() and max() key functions
    minletter = min(letterproportion, key=lambda letter: letterproportion[letter])
    maxletter = max(letterproportion, key=lambda letter: letterproportion[letter])
    minfreq = letterproportion[minletter]
    maxfreq = letterproportion[maxletter]
    
    #calculate each letter's point value
    letterpoints = {}
    for letter in letterproportion:
        if maxfreq == minfreq:
            letterpoints[letter] = 10
        else:
            score = (maxfreq - letterproportion[letter]) / (maxfreq - minfreq) #0-1 scale
            letterpoints[letter] = round(1 + score * 9, 0) #10-1 scale

    return letterpoints, lettercount
    
    
    
def extract_placeholders(story):
    """
    Extracts all placeholder words from a story that represent missing parts of speech.

    A placeholder is defined as a part of speech followed by a number (example: 'noun1', 'verb2').
    This function looks for whole words in that format and returns them as a list.

    Args:
        story (str): The input story containing placeholders for missing words.

    Returns:
        list: A list of placeholder strings found in the story (e.g., ['noun1', 'verb2']).
        
    Skill from list: 
        Regular Expression
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
        
    Skill from list: 
        f-string containing expression
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
    


def isvalid(letterpot, userinput, wordtype, modifier):
    """
     Figure out whether or not the input was valid. 
 
     Args:
         letterpot (dict): A key in a dictionary with the letters as keys and
         valid words as values.
         
         input (str): A word inputted by the player. 
         
         wordtype (str): type of word, whether it be a noun, verb, or something else.
         
         modifier (str): suffix to a word, such as striking(ly), dashing(ly)
         
     Returns:
         Output (str): If the input was valid given the constraints, it will
         return the input. Else, it will throw a value error.
     """
     
    # Check if word is valid according to letterpot
    for letter in userinput:
         if letter not in letterpot:
             raise ValueError ("This is not a valid Word! (Wrong Letters)")
         
    # Check if word is valid according to wordtype constraint
    if userinput not in partofspeech_dict[wordtype]:
        raise ValueError ("This is not a valid word! (Wrong Type)")
    else:
        
        # Check if word contains modifier in its correct position
        if not userinput.endswith(modifier):
            raise ValueError ("This is not a valid word! (Modifier is not present!)")
        else:
            return userinput
     
     
     
def inputpoints(inputword, letterpot, wordtype, modifier):
    """calculates the additional score for each input word
    
    Args:
        inputword (str): word guessed by player
        letterpot (dict): A dictionary with 7 character string as the key 
        and a list of strings as value. The list of strings is all of the 4+ 
        letter words that can be made with the 7 characters. 
        wordtype (str): word part of speech (noun, verb, etc...)
        modifier (str): suffix to a word
    
    Returns:
        f-string: stating how many total points have been found out of possible
        string: stating invalid word if ValueError is thrown
    
    Skill from list:
        Sequence unpacking
        
    Written by: Nell Yonkos    
    """
    letterpoints, lettercount = totalpoints(letterpot) 
    possiblepoints = 0
    for letter in lettercount:
        possiblepoints += lettercount[letter] * letterpoints[letter]
    try:
        isvalid(letterpot, inputword, wordtype, modifier)
        earnedpoints = 0
        for letter in inputword:
            earnedpoints += letterpoints[letter]
        return f"You've found {earnedpoints} out of {possiblepoints} possible."
    except ValueError:
        return "Invalid word!"

def auto_fill_story(story, partofspeech_dict):
    """
    Fills in missing part of speech words automatically using words from the dictionary.
    Args:
    story (str): The input story with placeholders like 'noun1', 'verb2', etc.
        partofspeech_dict (dict): A dictionary where keys are parts of speech and values are words for that pos that
        will work.
    Returns:
        str: The completed story with all placeholders replaced with valid words.
    """
    placeholders = extract_placeholders(story)
    filled = {}
    
    for placeholder in placeholders:
        pos = re.match(r"(noun|verb|adjective|pronoun|plural noun)", placeholder).group()
        if placeholder not in filled:
            filled[placeholder] = random.choice(partofspeech_dict[pos])
            
    for placeholder, word in filled.items():
        story = story.replace(placeholder, word)
    
    return story

def get_word_type(word, partofspeech_dict):
    """gets part of speech for play() function"""
    for i in partofspeech_dict:
        if word in partofspeech_dict[i]:
            return i
    
def play():
    print("Ready to play our Spelling Bee MadLibs Fusion game?!\n")
    name = input("Player name:  ")
    player = Player(name)
    game_pot = "aerlswy"
    print(f"Okay, {name}... your letters are A,E,R,L,S,W,Y\n")
    print("You can only use each letter once per word and your input words must be at least 4 letters long.\n")
    print("They've also got to be real words in the English dictionary-- I'll be checking.\n")
    print("One word per guess. Type 'HELP' for a hint. Type 'DONE' when you're out.\n\n")
    
    letterpoints, lettercount = totalpoints(game_pot)
    
    while True:
        userinput = input("Give me a word (or HELP or DONE):  ").lower()
        if userinput == "done":
            break
        elif userinput == "help":
            pass #########come back!
        elif userinput in player.guessed_words:
            print("You've already guessed that.")
        else:
            wordtype = get_word_type(userinput, partofspeech_dict)
            ####want to change so i don't need this, this shouldn't be necessisary 
            if wordtype is None:
                print("Invalid word!")
                continue
            modifier = "" ##### no suffix, maybe make that optional 
            points = inputpoints(userinput, game_pot, wordtype, modifier)
            if points == "Invalid word!":
                print("Invalid word!")
            else:
                player.guess_word(userinput)
                earnedpoints = sum(letterpoints[letter] for letter in userinput)
                player.add_score(earnedpoints)
                print(points)
                
    print("Ready for your stody ◡̈\n")
    print("Here it is:\n")
    print(auto_fill_story(story, partofspeech_dict))
                
                
                
if __name__ == "__main__":
    play()
