"""_summary_

Search English language dictionary to find two-word palingrams

The program examines the first word to determine a core word

Core word properties:
1. Odd or even length
2. One contingous part of the word spells out a real word
3. Contingious part can ocupy part of or full word
4. The other contingous part of the word is a palindrome
5. The palindromic part can ocupy part or all of the word
6. Palindromic sequence does not have to be a real word
(unless it ocupies the entire word)
7. The two parts cannot overlap or share letters
8. The sequence is reversible

Steps:
1. Input file into a word list
2. Reverse word --> see if reversed word exist in word list
3. Find palindromic sequence at beginning of reversed word
    Note: Palindromic squence can be a single letter
4. See if reversed_word(without palindromic seq) is in word list

This is my own attempt at solving this problem...
"""

import sys
from load_dictionary import load

def main():
    """
    Main function
    """
    print("\nPalingram Checker 1.0")
    path = \
    "c:/Users/antng/OneDrive/Documents/GitHub/learning/Python/Impractical Python Projects/Palingram Spells/"

    while True:
        word_list = load(f"{path}words.txt")
        pal_list = []
        reversed_list = [x[::-1] for x in word_list]

        for word in word_list:
            # find direct palingrams(ie. yam may)
            if word in reversed_list and word != word[::-1]:
                pal_list.append(f"{word} {word[::-1]}")

            # find palingrams with palindromic sequence (ie. yank nay)
            end = len(word)
            for i in range(end):
                if word[:i] in reversed_list and word[i:] == word[i:][::-1]:
                    pal_list.append(f"{word} {word[:i][::-1]}")

        print(*pal_list,sep="\n")
        print(f"\nNumber of palingrams = {len(pal_list)}")

        break

if __name__ == "__main__":
    main()