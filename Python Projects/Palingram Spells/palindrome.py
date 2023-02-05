"""_summary_

Load dictionary as list using load_dictonary module

Find palindromes in the list

Print palindromes out
"""

import sys
from load_dictionary import load

def main():
    """
    Main function
    """
    print("\nPalindrome Checker 1.0")
    path = "c:/Users/antng/OneDrive/Documents/GitHub/learning/Python/Impractical Python Projects/Palingram Spells/"

    while True:
        word_list = load(f"{path}words.txt")
        pali_list = []

        print(f"\nNumber of words in source = {len(word_list)}")

        for word in word_list:
            if word == word[::-1]:
                pali_list.append(word)

        print(f"\nNumber of palindromes found = {len(pali_list)}\n")
        print(*pali_list,sep="\t")
        break

if __name__ == "__main__":
    main()