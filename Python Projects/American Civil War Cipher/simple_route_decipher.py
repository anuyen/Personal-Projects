""" 
Solve simple route cipher given cipher text and key
"""

def main():
    """Main"""
    print("\nWelcome to route decipherer\n")
    
    # Input intake
    cipher_text = input("Paste your cipher text here:\n")
    key = input("\nPaste your key here:\n")
    
    # Turn key and cipher into lists
    key_int = [int(x) for x in key.split(' ')]
    cipher_list = cipher_text.split(" ")
    
    # Derive row and col
    COLS = len(key_int)
    ROWS = int(len(cipher_list)/COLS)
    
    print(f"\nColumns\t={COLS}\
            \nRows\t={ROWS}\
            \nkey\t={key}")
    
    translation_matrix = [None]*COLS
    plaintext = '' # where answer will go
    start = 0
    stop = ROWS

    # turn cipher list into cipher matrix
    for i in range(len(translation_matrix)):
        translation_matrix[i] = cipher_list[start:stop]
        start   += ROWS
        stop    += ROWS

    # use key to rearrange cipher matrix
    for x in key_int:
        if x < 0: # if x is positive --> travel DOWN
            pass
        else:
            translation_matrix[abs(x)-1] = translation_matrix[abs(x)-1][::-1]

    # append result in order
    while len(translation_matrix[COLS-1]) > 0:
        for x in translation_matrix:
            plaintext+=f"{x.pop()} "
  
    print(f"\nFinal translation:\n{plaintext}\n")
    
if __name__ == "__main__":
    main()