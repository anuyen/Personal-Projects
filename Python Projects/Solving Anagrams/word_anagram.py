"""_summary_

    Use a dictionary file to find all the single-word
    anagrams for a single English word.
"""
from load_dictionary import load
import sys
import time

path = "c:/Users/antng/OneDrive/Documents/GitHub/learning/Python/Impractical Python Projects/Solving Anagrams/"

word_set = set(load(f"{path}words.txt"))

word = input("\nEnter your word: ").lower()
print(f'\nFinding Anagram for your word "{word}"\n...\n...\n...')
performance =[]

def loop_anagram():
    start_time = time.time()
    anagram_list = []
    sub_word = sorted(list(word))

    for x in word_set:
        dict_word = sorted(list(x))
        if sub_word == dict_word:
            anagram_list.append(x)

    print(*anagram_list,sep="\n")
    print(f"Number of anagrams: {len(anagram_list)}")

    end_time = time.time()
    print(f"Runtime = {end_time - start_time}\n")
    performance.append(f"loop time: {end_time - start_time}")
    
def loop2_anagram():
    start_time = time.time()
    anagram_list = []
    sub_word = sorted(list(word))

    for x in word_set:
        #check if same length --> if not then pass
        if len(x) != len(sub_word):
            pass
        dict_word = sorted(list(x))
        if sub_word == dict_word:
            anagram_list.append(x)

    print(*anagram_list,sep="\n")
    print(f"Number of anagrams: {len(anagram_list)}")

    end_time = time.time()
    print(f"Runtime = {end_time - start_time}\n")
    performance.append(f"loop2 time: {end_time - start_time}")

loop_anagram()
loop2_anagram()

print(*performance,sep="\n")
            
    