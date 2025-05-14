"""
Spelling Bee MadLibs Fusion Game

This interactive Python game is a combination of a spelling bee challenge and a MadLibs story generator.

Players are given a set of 7 letters (a "letter pot") and must guess as many valid English words 
with the letters in the letter pot. Each word must be at least 4 letters long and match a specific 
part of speech (ex., noun, verb). Points are awarded based on letter rarity and word validity. Players 
can also request 1 hint. After the guessing phase, the game uses the player's words to fill in the story 
(provided in the file we submit). Any remaining blanks are automatically filled using a fallback dictionary.
The story template should use placeholders in the format: `<noun1>`, `<verb2>`, `<plural noun3>`, etc. But in this case
we will submit a story with that condition met (samplestory.txt).

Example Run Code:
python3 madlibs.py story1.txt
"""

import re
import random
from argparse import ArgumentParser
import sys

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
    ],
    "aceilms": [
        "malices","limaces","amices","camels","camise","claims","clames",
        "climes","macles","maleic","malice","mascle","melics","mescal",
        "scamel","emails","mailes","mesail","mesial","samiel","calms","camel",
        "claim","clams","clime","macle","malic","melic","acmes","amice","cames"
        "camis","maces","mesic","micas","alecs","almes","ceils","email","ileac",
        "laces","laics","lames","limas","limes","maile","mails","males","malis",
        "meals","miles","salic","salmi","scale","slice","slime","smile","mesia",
        "saice","aisle","acme","calm","came","cami","cams","clam","clem","emic",
        "mace","macs","mica","mice","mics","scam","aces","aesc","aims","alec",
        "alme","alms","amie","amis","asci","cals","case","ceas","ceil","cels",
        "ciel","elms","ices","lace","lacs","laic","lame","lams","leam","lice",
        "lima","lime","maes","mail","male","mali","mals","mase","meal","mela",
        "mels","mesa","mile","mils","mise","saic","saim","same","seam","semi",
        "sice","sima","slam","slim","ails","ales","ilea","isle","lase","leas",
        "leis","lias","lies","sail","sale","seal","seil","sial","sile","slae"
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
        "sera", "slae", "arle", "ares", "ales","acme", "aisle", "asci", "calm", "camel", 
        "camise", "case", "claim", "clam", "clime", "email", "isle", "lace", "lame", 
        "lice", "lima", "lime", "mace", "mail", "male", "mali", "malice", "meal", 
        "mesa", "mescal", "mica", "mice", "mile", "sail", "sale", "salmi", "same", 
        "samiel", "scale", "seal", "seam", "semi", "sial", "sima", "slam", 
        "slice", "slime", "smile","ace"

    ],
    "plural noun": [
        "zephyrs", "hypers", "hypes", "preys", "pyres", "hers", "heps", "heys", 
        "hyes", "pehs", "pyes", "rehs", "reps", "ryes", "yeps", "zeps",
        "lawyers", "layers", "rayles", "relays", "walers", "warsle", "wyles", "yawls", 
        "alews", "aryls", "ayres", "eyras", "lyres", "ryals", "swaly", "swayl", "wales", 
        "wares", "weals", "wears", "yales", "years", "arles", "earls", "laers", "lares", 
        "lears", "yaws", "yews", "ways", "weys", "wyes", "laws", "lays", "leys", "lyes", 
        "raws", "rays", "rews", "ryas","aces", "acmes", "ails", "aims", "ales", 
        "alms", "calms", "camels", "cams", "claims", "clams", "climes", "elms", 
        "emails", "ices", "laces", "lacs", "lames", "lams", "leas", "leis", 
        "lies", "limas", "limes", "maces", "macs", "mails", "males", "malices", 
        "malis", "mals", "meals", "micas", "miles", "mils"

    ],
    "verb": [
        "hype", "hypes", "prey", "preys", "espy", "heps", "sypher","swear", 
        "wear", "relay", "resaw", "resay", "slay", "sway", "swale", "swer", 
        "sear", "sale", "seal", "lear", "rase", "rely", "slew","aces", "ails", 
        "aims", "calm", "calms", "came", "case", "claim", "claims", "clam", 
        "clames", "clams", "email", "emails", "ices", "lace", "laces", "lame", 
        "lames", "lams", "lies", "lime", "limes", "mail", "mailes", "mails", 
        "sail", "scale", "scam", "seal", "seam", "slam", "slice", "slim", 
        "slime", "smile"

    ],
    "adjective": [
        "hyper", "sphery", "shyer", "spry", "hep","sweary", "weary", "early", 
        "leary", "slyer", "wary", "awry", "arsey", "easy", 
        "rawly", "swaly", "swayl","calm", "laic", "lame", "mesial", 
        "mesic", "same", "slim"
    ]
}

fillerpartofspeech = {
    "noun": [
        "banana","bug","lizard","breeze","candle","dragon","forest","island",
        "jungle","mountain","pencil","village","fish","snail","octopus","squid"
    ],
    "plural noun": [
        "apples","books","cars","dogs","flowers","bubbles","islands","kites",
        "stars","trees","sharks"
    ],
    "verb": [
        "climb","draw","explore","jump","laugh","paint","run","sing","swim",
        "write","dance"
    ],
    "adjective": [
        "bright","calm","fierce","giant","happy","lazy","quick","shiny","tiny",
        "wild","pretty","ugly"
    ]}


# HERE IS OLD STORY. COMMENTING OUT IN CASE TO TEST CUSTOM STORY FUNCTIONALITY
# story = """
# Just when it seemed every noun1 under the noun2  had been named, 
# researchers at the University of plural noun1, have identified a adjective new 
# one. Called "olo", this shade lies outside the normal range of noun3 vision."
# """

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
        
        lettercount (dict): count of frequency of each letter in the letterpot
        in all of the words that can be made from the letterpot. 
        
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
    

    return re.findall(r'<(.*?)>', story)



def help(letterpot, player):
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
    
    #Initialized a new list then appends unguessed words to that list
    temp_list = []
    for word in words:
        if word not in player.guessed_words and word not in temp_list:
            temp_list.append(word)
            
    #Pulls a random word out of the temporary list and uses it as a help word
    help_word = random.choice(temp_list)
    temp_list.remove(help_word)
    
    #Create a length of the word where the middle letters are the "-" symbol
    space_length = (len(help_word) - 2) * "-"
    
    #Print the first and last letters of the word with the middle "-" symbols
    print(f"Here is your hint\n{help_word[0] + space_length + help_word[-1]}")
    


def isvalid(letterpot_key, userinput, wordtype):
    """
     Figure out whether or not the input was valid. 
 
     Args:
         letterpot (dict): A key in a dictionary with the letters as keys and
         valid words as values.
         
         input (str): A word inputted by the player. 
         
         wordtype (str): type of word, whether it be a noun, verb, or something else.
         
     Returns:
         Output (str): If the input was valid given the constraints, it will
         return the input. Else, it will throw a value error.
     """
    if len(userinput) < 4:
        raise ValueError("This is nto a valid word! Too short!")
     
    # Check if word is valid according to letterpot
    if userinput not in letterpots[letterpot_key]:
        raise ValueError("This is not a valid Word!")
         
    # Check if word is valid according to wordtype constraint
    if userinput not in partofspeech_dict.get(wordtype, []):
        raise ValueError ("This is not a valid word! (Wrong Type)")
    else:
        
  
        return userinput
     
  # Testing out inputpoints as a method in player class to access score   
     
def inputpoints(inputword, letterpot, wordtype):
    """calculates the additional score for each input word based on how rare.
    
    Args:
        inputword (str): word guessed by player
        letterpot (dict): A dictionary with 7 character string as the key 
        and a list of strings as value. The list of strings is all of the 4+ 
        letter words that can be made with the 7 characters. 
        wordtype (str): word part of speech (noun, verb, etc...)
    
    Returns:
        int: points rewarded for this input word and total points possible
             for all input words
        string: stating invalid word if ValueError
        
    Raises:
        ValueError: if isvalid function fails and ValueError is raised there
    
    Skill from list:
        Sequence unpacking
        
    Written by: Nell Yonkos    
    """
    
    letterpoints, lettercount = totalpoints(letterpot) 
    possiblepoints = 0
    earnedpoints = 0
    for letter in lettercount:
        possiblepoints += lettercount[letter] * letterpoints[letter]
    try:
        isvalid(letterpot, inputword, wordtype)
        for letter in inputword:
            earnedpoints += letterpoints[letter]
        return earnedpoints, possiblepoints

    except ValueError:
        return "Invalid word!"

def auto_fill_story(story, player, fillerpartofspeech):
    """
    Fills in missing part of speech words automatically first using player
    input words and then with fillerpartofspeech words as a backup. 
    
    Args:
    story (str): The input story with placeholders like 'noun1', 'verb2', etc.
        partofspeech_dict (dict): A dictionary where keys are parts of speech 
        and values are words for that pos that will work.
    player (object): object with method pos_guess() which has user input words 
        grouped by part of speech. 
    fillerpartofspeech (dict): a dictionary with parts of speech as keys and a 
        few simple words in that part of speech as the keys for each. 
    
    Returns:
        str: The completed story with all placeholders replaced with valid words.
    """
    with open(story, 'r') as f:
        text = f.read()
    # extract_placeholders extracts all the placeholders in story,
    # use this function to substitute the extracted placeholders
    placeholders = extract_placeholders(text)
    
    filled = {}
    used_words = {}
    
    player_pos_words = player.pos_guess(partofspeech_dict)

    
    
    for pos in fillerpartofspeech:
        used_words[pos] = []
        

    for placeholder in placeholders:
        match = re.match(r"(noun|verb|adjective|plural noun)", placeholder)
        if match:
            pos = match.group(1)
            if placeholder not in filled:
                #user input words first
                #playerwords = player_pos_words.get(pos, [])

                shouldpull = [w for w in player_pos_words.get(pos, []) if w not in used_words[pos]]

                #after user input words have been used up, use filler word dictionary
                if not shouldpull: 
                    shouldpull = [w for w in fillerpartofspeech[pos] if w not in used_words[pos]]
                            
                if shouldpull:
                    index = random.randint(0, len(shouldpull) - 1)
                    first = shouldpull[index]
                    used_words[pos].append(first)
                    filled[placeholder] = first
                else:
                    filled[placeholder] = "square"
                            
    for placeholder in placeholders:
        if placeholder in filled: 
            #1 bc only want to replace first occurance only. that way each is unique            
            text = text.replace(f"<{placeholder}>", filled[placeholder], 1)
    
    return text
    
def missed_words(letterpot_key, player):
    """
    Displays how many valid words were missed by the player using set operations.
    
    Args:
        letterpot_key (str): The key to access the letterpot list of valid words.
        player (Player): The Player object containing guessed words.
    
    Side Effects:
        Prints number of missed words and optionally a few examples.
    """
    all_valid = set(letterpots[letterpot_key])
    guessed = set(player.guessed_words)
    missed = all_valid.difference(guessed)

    print(f"You missed {len(missed)} words. Here's a few: {random.sample(list(missed), min(5, len(missed)))}")


def get_word_type(word, partofspeech_dict):
    """gets part of speech for play() function
    Args: 
        word (str): word in letterpot dictionary and partofspeech_dict 
                    dictionary
        partofspeech_dict (dict): dictionary containing lists of valid input 
                                  words sorted into parts of speech keys
    Returns: 
        str: the part of speech key from partofspeech_dict of the word
    """
    for i in partofspeech_dict:
        if word in partofspeech_dict[i]:
            return i
    
def play(story):
    """
    plays game allowing user input, takes user name, explains rules, checks
    input word validity, gives score per input word, allows hint command,
    prints story with words filled in
    
    Args:
        story (str): path to a text file containing a story
    
    
    Side effects:
    - prints game rules
    - prints instructions to player and allows them to user input
    - prints a madlibs style story including valid user input words
    """
    
    
    print("Ready to play our Spelling Bee MadLibs Fusion game?!\n")
    name = input("Player name:  ")
    player = Player(name)
    
    # Try to make gamepot random?
    game_pot = random.choice(list(letterpots.keys()))
    print(f"Okay, {name}... your letters are \"{game_pot}\"\n")
    print("You can only use each letter once per word and your input words must be at least 4 letters long.\n")
    print("They've also got to be real words in the English dictionary-- I'll be checking.\n")
    print("One word per guess. Type 'HELP' for a hint (just 1 per game). Type 'DONE' when you're out.\n\n")
    
    letterpoints, lettercount = totalpoints(game_pot)
    help_points = 3
    
    # second instance of guessed_words, this time a "global variable idk how to access from class"
    while True:
        userinput = input("Give me a word (or HELP or DONE):  ").lower()
        if userinput == "done":
            break
        # testing to see if help function works
        elif userinput == "help":
            help_points -= 1 
            if help_points > 1:     
            # utilize help function only if enough help points are available
                help(game_pot, player)
               #print(f"You have {help_points} hints left")
            else:
                print("You have used up all your hints")
        
        elif userinput in player.guessed_words:
            print("You've already guessed that.")
        
        else:
            player.guessed_words.append(userinput)
            
            wordtype = get_word_type(userinput, partofspeech_dict)
            ####want to change so i don't need this if statement below, this shouldn't be necessisary 
            if wordtype is None:
                print("Invalid word!")
                continue
            # modifier = "" ##### no suffix, maybe make that optional in the whole code
            points = inputpoints(userinput, game_pot, wordtype)
            if points == "Invalid word!":
                 print("Invalid word!")
            else:
                earnedpoints, possiblepoints = points
                player.add_score(earnedpoints)
                print(f"You've found {player.score} out of {possiblepoints} possible.")
            
            
    print("Ready for your story ◡̈\n") #repeats the same noun for multiple blanks, doesn't catch "plural noun"
    print("Here it is:\n")
    missed_words(game_pot, player)
    #print("FOR TESTING PURPOSES:\n")
    #print(player.pos_guess(partofspeech_dict))
    # auto_fill_story is what fills in the story, DO REGEX STUFF IN AUTOFILLSTORY
    
    # STORY IS NOT INPUTTED
    print(auto_fill_story(story, player, fillerpartofspeech))
                
    
def parse_args(arglist):
    """ Parse command-line arguments.
    
    Expect one mandatory arguments:
        - story: a path to a file containing a fill-in-the-blank story
        
    
    
    Args:
        arglist (list of str): arguments from the command line.
    
    Returns:
        namespace: the parsed arguments, as a namespace.
        By: Vonn Sayasa
    """
    parser = ArgumentParser()
    parser.add_argument("story", help="Path to the TXT file"
                            "containing story")
    return parser.parse_args(arglist)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    play(args.story)
