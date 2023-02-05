"""
This is the automated version of the the previous
phrase anagram 

I will attempt to clean up the previous script
and create a script to automatically output
one random anagram phrase :) (because all combos 
would take forever)
"""
import sys
import time
import random
from collections import Counter
from load_dictionary import load

start_time = time.time()
PATH = "c:/Users/antng/OneDrive/Documents/GitHub/learning/Python/Impractical Python Projects/Solving Anagrams/"
WORD_SET = set(load(f"{PATH}words.txt"))
INPUT = input("\nEnter your name: ").lower().replace(' ','')
LIMIT = len(INPUT)

def phrase_length(phrase_list):
    """Function for finding length of phrase"""
    phrase_length = 0
    for x in phrase_list:
        phrase_length += len(x)
    return phrase_length

def find_anagram(word_bank):
    """
    Function for finding anagrams
    It takes in the word bank and returns a list of anagrams
    that can be made from the word bank
    """
    choices = []
    for word in WORD_SET:
        if Counter(word) <= word_bank:
            choices.append(word)
    return choices

def find_final_anagram(word_bank):
    """Find the final anagram"""
    choices = []
    for word in WORD_SET:
        if Counter(word) == word_bank:
            choices.append(word)
    return choices

def check_final_solution(sol):
    """Check Final Solution"""
    if Counter(sol.replace(' ','')) == Counter(INPUT):
        print("\nSUCCESS\n")
    else:
        print("\nFAILURE...Trying Again\n")
        main()

def main():
    """Main Function"""
    while True:
        word_bank = Counter(INPUT)
        final_phrase = []

        while phrase_length(final_phrase) < LIMIT:
            length = phrase_length(final_phrase)

            if final_phrase != []:
                print("(Your phrase so far is:)")
                print(' '.join(final_phrase))

            if LIMIT - 1 == length:
                break
            if LIMIT - length > 2:
                choices = find_anagram(word_bank)
            elif LIMIT - length == 2:
                #this means that there are 
                print("This combination does not work...Let's start over")
                final_phrase = []
                word_bank = Counter(INPUT)
                choices = find_anagram(word_bank)
            else:
                choices = find_final_anagram(word_bank)

            if len(choices) == 0:
                print("This combination does not work...Let's start over")
                final_phrase = []
                word_bank = Counter(INPUT)
                choices = find_anagram(word_bank)

            print(f"Number of possible words = {len(choices)}")

            # randomly pick a choice for user
            user_choice = random.choice(choices)
            print(f"Word chosen = {user_choice}")

            # subtract words from choice from word bank and add it to final phrase
            word_bank = word_bank - Counter(user_choice)
            final_phrase.append(user_choice)
            
        print("Your final anagram is:\n",' '.join(final_phrase))
        check_final_solution(' '.join(final_phrase))
        break

if __name__ == "__main__":
    main()

end_time = time.time()
print(f"Runtime = {end_time-start_time}")