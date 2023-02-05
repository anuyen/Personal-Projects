"""_summary_
Takes a message encrypted with the route cipher,
the number of columns and rows in the transpositional
matrix, and a key.
Output the plain translated plaintext

Will decrypt all "common" route cipher where
the route starts at the top of bottom of a column
and continues up and/or down columns
"""
     
cipher_text = "16 12 8 4 0 1 5 9 13 17 18 14 10 6 2 3 7 11 15 19"
print(f"\nOriginial cipher text is:\n{cipher_text}")
cipher_list = cipher_text.split(" ")

COLS    = 4
ROWS    = 5
key     = '-1 2 -3 4' # negative num == UP
print(f"\nColumns\t={COLS}\
        \nRows\t={ROWS}\
        \nkey\t={key}")

translation_matrix = [None]*COLS
plaintext = '' # where answer will go
start = 0
stop = ROWS

# turn key into a list of int
key_int = [int(x) for x in key.split(' ')]

# turn cipher list into cipher matrix
for i in range(len(translation_matrix)):
    translation_matrix[i] = cipher_list[start:stop]
    start   += ROWS
    stop    += ROWS

for x in key_int:
    if x < 0: # if x is positive --> travel DOWN
        pass
    else:
        translation_matrix[abs(x)-1] = translation_matrix[abs(x)-1][::-1]
    
while len(translation_matrix[COLS-1]) > 0:
    for x in translation_matrix:
        plaintext+=f"{x.pop()} "
        
print(f"\nFinal translation:\n{plaintext}\n")
