/**
 * Telephone Number Validator
Return true if the passed string looks like a valid US phone number.
 */

const { off } = require("process")
const { number } = require("yargs")

function telephoneCheck(str) {
    let numberArr = str.match(/\d/g)
    let nonNumArr = str.match(/\D/g)
    if(numberArr.length < 10 || numberArr.length > 11){
        return false
    } else if (numberArr.length == 10 && str.match(/\D/g) == null){
        return true
    } else if (numberArr.length > 10 && str.match(/\D/g) == null){
        return false
    } else if (numberArr.length == 11 && numberArr[0] != 1){
        return false
    } else if(nonNumArr.length == 2 && nonNumArr[0] == ' ' && nonNumArr[1] == ' ') {
        return true
    } else if (nonNumArr.length == 2 && nonNumArr[0] == '-' && nonNumArr[1] == '-'){
        return true
    } else if (nonNumArr.length == 3 && nonNumArr[0] == ' ' && nonNumArr[1] == ' ' && nonNumArr[2] == ' ') {
        return true
    } else if (nonNumArr.length == 3 && nonNumArr[0] == '(' && nonNumArr[1] == ')' && nonNumArr[2] == '-') {
        return true
    } else if (nonNumArr.length == 3 && nonNumArr[0] == ' ' && nonNumArr[1] == '-' && nonNumArr[2] == '-') {
        return true
    } else if (nonNumArr.length == 5 && nonNumArr[0] == ' ' && nonNumArr[1] == '(' && nonNumArr[2] == ')' && nonNumArr[3] == ' ' && nonNumArr[4] == '-') {
        return true
    } else if (nonNumArr.length > 5){
        return false
    }  else {
        return false
    }
}

function telephoneCheck(str) {
    let numberArr = str.match(/\d/g)
    let nonNumArr = str.match(/\D/g)
    let nonNumStr = nonNumArr.join("")
    if(numberArr.length > 10 && numberArr[0] != 1){
        return false // if there are more than 10 numbers, and the first number is not 1, return false
    } else if(numberArr.length < 10){
        return false
    } else if (numberArr.length == 10 && str.match(/\D/g) == null){
        return true
    } else if(nonNumArr.length == 4 && nonNumArr[0] !== '('){
        return false
    } else if (nonNumArr.length == 2 && nonNumArr[0] == ' ' && nonNumArr[1] == ' '){
        return true
    } else if (nonNumArr.length == 2 && nonNumArr[0] == '-' && nonNumArr[1] == '-'){
        return true
    }
    else {
        return false
    }
}

telephoneCheck("555-555-5555");

//spaces dont matter

if(str.match().length == 2){

}