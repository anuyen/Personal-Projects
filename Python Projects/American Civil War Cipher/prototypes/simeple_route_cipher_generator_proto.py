"""
Takes in a message

Decide matrix formation

Choose key

Output cipher
"""
import random

entry = "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19"

entry_list = entry.split(" ")
l = len(entry_list)

matrix_option = []

for x in range(2,l-1):
    if l%x == 0:
        matrix_option.append([x,int(l/x)])

print("\nHere are the choices for your cipher matrix:\n")

for index in range(len(matrix_option)):
    print(f"{index+1}.{matrix_option[index]}\n")

choice = int(input("Select the number corresponding to your choice: \n")) - 1

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