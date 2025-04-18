#sample dictionaries
import re

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
    return re.findall(r'\b(?:noun|verb|adjective|pronoun|plural noun)\d+\b', story)

#totalpoints("ehprsyz")


