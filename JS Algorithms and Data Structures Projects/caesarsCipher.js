"abcdefghijklmnopqrstuvwxyz"

let answer = []
for(let i = 0; i < str.length; i++){
    if(str[i] = " "){answer.push(" ")}
    else {}
}

/**
 *                   Caesars Cipher
One of the simplest and most widely known ciphers is a Caesar cipher, 
also known as a shift cipher. In a shift cipher the meanings of the letters
 are shifted by some set amount.

A common modern use is the ROT13 cipher, where the values of the letters are 
shifted by 13 places. Thus A ↔ N, B ↔ O and so on.

Write a function which takes a ROT13 encoded string as input and returns a decoded string.

All letters will be uppercase. Do not transform any non-alphabetic character 
(i.e. spaces, punctuation), but do pass them on.
 */


function rot13(str) {
    let alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('')
    let arr = str.match(/[A-Z\W]/g)
    let answer = []
    for(let i = 0; i < arr.length; i++){
        if(alphabet.indexOf(arr[i]) == -1){
            answer.push(arr[i])
        } else if (alphabet.indexOf(arr[i]) < 13){
            answer.push(alphabet[alphabet.indexOf(arr[i])+13])
        } else {
            answer.push(alphabet[alphabet.indexOf(arr[i])-13])
        }
    }
    return answer.join("")
}
  
rot13("SERR PBQR PNZC");