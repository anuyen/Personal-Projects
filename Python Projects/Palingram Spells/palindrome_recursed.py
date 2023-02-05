"""
In this program, I will go back to palindromes but with recursion

Then, I will test two programs against each other to see which
is faster, recusion of regular loops
"""

import cProfile
from load_dictionary import load
import sys

path = "c:/Users/antng/OneDrive/Documents/GitHub/learning/Python/Impractical Python Projects/Palingram Spells/"

word_list = load(f"{path}words.txt")
word_set = set(word_list)

# to throw in another test, lets also include list
# so total, there will be 4 tests

def pal_list():
    print("\nlist")
    pali_list = []
    
    print(f"\nNumber of words in source = {len(word_list)}")

    for word in word_list:
        if word == word[::-1]:
            pali_list.append(word)

    print(f"\nNumber of palindromes found = {len(pali_list)}\n")

def pal_list_recursive():
    print("list recursive")
    pali_list = []
    
    print(f"\nNumber of words in source = {len(word_list)}")

    def check_string(sub_word):
        if len(sub_word) == 1 or len(sub_word) == 0:
            pali_list.append(word)
        elif sub_word[-1] == sub_word[0]:
            sub_word = sub_word[1:len(sub_word)-1]
            check_string(sub_word)
        else:
            pass

    for word in word_list:
        sub_word = list(word)
        check_string(sub_word)

    print(f"\nNumber of palindromes found = {len(pali_list)}\n")

def pal_set():
    print("set")
    pali_list = []
    
    print(f"\nNumber of words in source = {len(word_set)}")

    for word in word_set:
        if word == word[::-1]:
            pali_list.append(word)

    print(f"\nNumber of palindromes found = {len(pali_list)}\n")
    
def pal_set_recursive():
    print("set recursive")
    pali_list = []
    
    print(f"\nNumber of words in source = {len(word_set)}")

    def check_string(sub_word):
        if len(sub_word) == 1 or len(sub_word) == 0:
            pali_list.append(word)
        elif sub_word[-1] == sub_word[0]:
            sub_word = sub_word[1:len(sub_word)-1]
            check_string(sub_word)
        else:
            pass

    for word in word_set:
        sub_word = list(word)
        check_string(sub_word)

    print(f"\nNumber of palindromes found = {len(pali_list)}\n")
    
cProfile.run('pal_list()')
cProfile.run('pal_list_recursive()')
cProfile.run('pal_set()')
cProfile.run('pal_set_recursive()')
