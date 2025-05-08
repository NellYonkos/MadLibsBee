
#sample dictionaries
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

partofspeech = {
    "noun": [
        "zephyr", "hyper", "hype", "prey", 
        "pyre", "spyre", "prez", "prys", "resh", "rype", "sype", "syph"   
    ],
    "plural noun": [
        "zephyrs", "hypers", "hypes", "preys", "pyres", "hers", "heps", "heys", 
        "hyes", "pehs", "pyes", "rehs", "reps", "ryes", "yeps", "zeps"
    ],
    "verb": [
        "hype", "hypes", "prey", "preys", "espy", "heps", "sypher"
    ],
    "adjective": [
        "hyper", "sphery", "shyer", "spry", "hep"
    ],
    "pronoun": [
        "hers"
    ]
}



    



#filler function
def checkword(inputword, letterpot):
    """checks input word validity"""
    return True

def inputpoints(inputword, letterpot):
    """calculates the additional score for each input word"""
    letterpoints = totalpoints(letterpot) #deliv1 function 
    
    if checkword(inputword, letterpot) == True:
        #calculating input word score
        earnedpoints = 0
        for letter in inputword:
            earnedpoints += letterpoints[letter]
            
        return (earnedpoints)
    else:
        return("This is not a valid word from the letter pot. Try again.")
    


def maxscore(inputword, letterpot):
    letterpoints = totalpoints(letterpot) #deliv1 function 

    #calculate possible max score
    possiblepoints = 0
    for letter in lettercount:
        possiblepoints += lettercount[letter] * letterpoints[letter]
    

#############most of this should prob be child functions of deliv1

