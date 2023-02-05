    In this project, I will load dictionary files from the internet 
and use Python to discover first palindromes and then the more complex
palingrams in those files.

    Then, I will use a tool called cProfile to analyze my script's performance

    Note: 
    In 2011, DC Comics published an interesting sorcerer hero
named Zatanna, who was cursed to only be able to cast spells by
speaking palindromatically. She's only able to think up of
two-word phases such as "nurses run", "stack cats", or "puff up"

    My program is aimed at helping Zatanna find better spells

    Prompt from:
    Vaughan, Lee. 2019. "Impractical Python Projects". Chapter 2 Page 19

    Words from:
    https://greenteapress.com/thinkpython2/code/words.txt 

Lesson learned:
    Using sets is much faster for lookups compared to using list
    The same function with list takes around 300 seconds
    Where as the same function using set only take 0.627 seconds
    This is the case for palingram, not palindrome