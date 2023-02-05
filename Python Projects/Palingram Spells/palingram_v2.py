"""_summary_

Search English language dictionary to find two-word palingrams

This is the book's attempt at solving this problem...
"""

import sys
from load_dictionary import load

print("\nPalingram Checker 2.0")
path = \
"c:/Users/antng/OneDrive/Documents/GitHub/learning/Python/Impractical Python Projects/Palingram Spells/"

word_list = load(f"{path}words.txt")

def find_palingram():
    """Find dict palingram"""
    pal_list = []
    for word in word_list:
        end = len(word)
        rev_word = word[::-1]
        if end > 1:
            for i in range(end):
                # if palidromic sequence exist at the end
                # and reversed core sequence exist in word_list
                if word[i:] == rev_word[:end-i] and rev_word[end-i:] in word_list:
                    pal_list.append(f"{word} {rev_word[end-i:]}")
                # if core sequence is palindromic and is in word_list
                if word[:i] == rev_word[end-i:] and rev_word[:end-i] in word_list:
                    pal_list.append(f"{rev_word[:end-i]} {word}")
    return pal_list

pal = find_palingram()
sorted_pal = sorted(pal)

print(*sorted_pal,sep="\n")
print(f"\nNumber of palingrams = {len(sorted_pal)}")