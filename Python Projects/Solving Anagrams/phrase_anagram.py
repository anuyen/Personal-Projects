"""
    Program will build an anagram phrase from the letters of given name

    for example:
    Clint Eastwood --> old west action

    User will input a name, then they get to pick the words in the final
    phrase sequentially

    for example:
    Clin Eastwood --> old
                  --> west
                  --> action

    This program will use Counter (similar to map reduce) to reduce
    the input into a dictionary of letters

    for example:
    Maddam --> {a:2,d:2,m:2}

    Then, it will find words that can be created from word bank
"""
import sys
from collections import Counter
from load_dictionary import load

PATH = "c:/Users/antng/OneDrive/Documents/GitHub/learning/Python/Impractical Python Projects/Solving Anagrams/"
word_set = set(load(f"{PATH}words.txt"))
name = input("\nEnter your name: ").lower().replace(' ','')

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
    for word in word_set:
        if Counter(word) <= word_bank:
            choices.append(word)
    return choices

def find_final_anagram(word_bank):
    """Find the final anagram"""
    choices = []
    for word in word_set:
        if Counter(word) == word_bank:
            choices.append(word)
    return choices

def check_final_solution(sol):
    """Check Final Solution"""
    if Counter(sol.replace(' ','')) == Counter(name):
        print("\nSUCCESS")
    else:
        print("\nYou're a failure LOL. Let's try again")
        main()

def main():
    """Main Function"""
    word_bank = Counter(name)
    #print(word_bank)
    final_phrase = []
    limit = len(name)

    while True:
        while phrase_length(final_phrase) < limit:
            #print(limit-1)
            #print(phrase_length(final_phrase))
            print(f"Word length remaining: {limit - phrase_length(final_phrase)}")
            if limit-1 == phrase_length(final_phrase):
                break
            # give choices for user to choose from
            if limit - phrase_length(final_phrase) > 2:
                choices = find_anagram(word_bank)
            elif limit - phrase_length(final_phrase) == 2:
                print("This combination does not work...Let's start over")
                final_phrase = []
                word_bank = Counter(name)
                choices = find_anagram(word_bank)
            else:
                choices = find_final_anagram(word_bank)

            if len(choices) == 0:
                print("This combination does not work...Let's start over")
                final_phrase = []
                word_bank = Counter(name)
                choices = find_anagram(word_bank)

            print(*choices,sep="\t")

            if final_phrase != []:
                print("(Your phrase so far is:)")
                print(' '.join(final_phrase))

            # collect user choice and verify that it is in the list of choices
            user_choice = input("\nWhich word from the list above would you like to choose?\n")
            while user_choice.lower() not in choices:
                user_choice = input("\nYour chosen word is not in the given list of words. Please try again...\n")
            print("\nGreat choice! Your chosen word is:\n{}\n".format(user_choice))

            # subtract words from choice from word bank and add it to final phrase
            word_bank = word_bank - Counter(user_choice)
            #print(word_bank)
            final_phrase.append(user_choice)

        print("Your final anagram is:\n",' '.join(final_phrase))
        check_final_solution(' '.join(final_phrase))
        break

if __name__ == "__main__":
    main()

"""
How counter works
Counter turns your string into hash code
--> which can be compared via comparison operators (<,>,=)
--> you can also perform subtraction and addition (+,-)

from collections import Counter
word_bank = Counter(name)
word_bank = Counter({'t': 2, 'o': 2, 'c': 1, 'l': 1, 'i': 1, 'n': 1, 'e': 1, 'a': 1, 's': 1, 'w': 1, 'd': 1})
                
word = 'lint'
word_counter = Counter(word)
word_counter = Counter({'l': 1, 'i': 1, 'n': 1, 't': 1})

word_counter < word_bank ==> True
word_counter = word_bank ==> False
Counter("x") < word_bank ==> False

rem_word = word_bank - word_counter
rem_word = Counter({'c': 1, 't': 1, 'e': 1, 'a': 1, 's': 1, 'w': 1, 'o': 2, 'd': 1})
"""