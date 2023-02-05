"""
    Description:
    
    Input: input.txt
    Ouput: output.txt
    
    The input.txt contains the message you want to encrypt simple route cipher encryption,
    famously used by the Union during the American Civil war.

    The program will:
    1. Split words from input and assign numerical values in order (dictionary)
    2. Check if a cipher matrix can be made from the text
    3. If cipher matrix cannot be made, trim text so a nice cipher matrix can be made
    For simplicity, program will only trim words at the end
    4. Give user a choice of which cipher matrix to choose from
    5. Write output.txt with the scrambled text, columns/rows, and the key for deciphering it
"""

import random

def check_prime(num):
    if num >1:
        for i in range(2,num):
            if (num%i)==0:
                print(num," is not a prime number")
                return True
            else:
                print(num," is a prime number")
                return False


def main():
    path = "c:/Users/antng/Documents/GitHub/learning/Python/Impractical Python Projects/American Civil War Cipher/"
    with open(f"{path}input.txt") as input:
        entry = ""
        for line in input:
            entry += line
        
    entry_list = entry.split()
    l = len(entry_list)

    words_at_end = ""
    while not check_prime(l):
        words_at_end += entry_list.pop()
        l -= 1

    matrix_option = []

    for x in range(2,l-1):
        if l%x == 0:
            matrix_option.append([x,int(l/x)])

    print("\nHere are the choices for your cipher matrix:\n")

    for index in range(len(matrix_option)):
        print(f"{index+1}.{matrix_option[index]}\n")

    choice = random.choice(range(len(matrix_option)))

    print(f"Randomly chosen encryption matrix {choice + 1}")

    COLS = matrix_option[choice][0]
    ROWS = matrix_option[choice][1]

    print("Generating random key...")

    key = [x*random.choice([1,-1]) for x in range(1,COLS+1)]

    print(f"\nColumns\t={COLS}\
            \nRows\t={ROWS}\
            \nkey\t={key}")

    start = 0
    cipher_matrix = []
    for x in range(COLS):
        cipher_matrix.append(entry_list[start:start+ROWS])
        start+=ROWS

    for x in key:
        if x > 0:
            pass
        else:
            cipher_matrix[int(abs(x)-1)] = cipher_matrix[int(abs(x)-1)][::-1]

    final_ans = ""
    for x in cipher_matrix:
        final_ans+=(f"{x[0]} {x[1]} ")

    print("\nYour cipher is: \n")
    print(final_ans,"\n")

    key_out = ""
    for x in key:
        key_out += f"{x} "
    with open(f"{path}output.txt","w") as output:
        output.write("Cipher:")
        output.write(f"\n{final_ans}")
        output.write(f"\nColumns\t={COLS}\
                    \nRows\t={ROWS}\
                    \nkey\t={key_out}")
        output.write("\nWords at the end:\n")
        output.write(f"{words_at_end}")

if __name__ == "__main__":
    main()