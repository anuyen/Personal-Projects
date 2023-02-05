/*
Cash Register
Design a cash register drawer function checkCashRegister() that accepts purchase price 
as the first argument (price), payment as the second argument (cash), and cash-in-drawer 
(cid) as the third argument.

cid is a 2D array listing available currency.

The checkCashRegister() function should always return an object with a status key and a change key.

Return {status: "INSUFFICIENT_FUNDS", change: []} if cash-in-drawer is less than the change due, 
or if you cannot return the exact change.

Return {status: "CLOSED", change: [...]} with cash-in-drawer as the value for the key change
if it is equal to the change due.

Otherwise, return {status: "OPEN", change: [...]}, with the change due in coins and bills
, sorted in highest to lowest order, as the value of the change key.

Currency Unit	Amount
Penny	$0.01 (PENNY)
Nickel	$0.05 (NICKEL)
Dime	$0.1 (DIME)
Quarter	$0.25 (QUARTER)
Dollar	$1 (ONE)
Five Dollars	$5 (FIVE)
Ten Dollars	$10 (TEN)
Twenty Dollars	$20 (TWENTY)
One-hundred Dollars	$100 (ONE HUNDRED)
See below for an example of a cash-in-drawer array:
*/

//final code
function checkCashRegister(price, cash, cid) {
  let dif = (cash - price)*100

  function Answer(status, change){
    this.status = status
    this.change = change
  }

  let dif100 = {
    rem : function(n){return n%10000},
    num: 10000,
    name : "ONE HUNDRED"} // 0
  let dif20 = {
    rem : function(n){return n%2000},
    num: 2000,
    name : "TWENTY"}  // 1
  let dif10 = {
    rem : function(n){return n%1000},
    num: 1000,
    name : "TEN"}   // 2
  let dif5 = {
    rem : function(n){return n%500},
    num: 500,
    name: "FIVE"}     // 3
  let dif1 = {
    rem : function(n){return n%100},
    num: 100,
    name: "ONE"}     // 4
  let difqu = {
    rem : function(n){return n%25},
    num: 25,
    name: "QUARTER"} // 5
  let difdime ={
    rem : function(n){return n%10},
    num: 10,
    name: "DIME"}//6
  let difnic = {
    rem : function(n){return n%5},
    num: 5,
    name: "NICKEL"} //7
  let difpen = {
    rem : function(n){return n%1},
    num: 1,
    name: "PENNY"} //8

  let difArr = [dif100,dif20,dif10,dif5,dif1,difqu,difdime,difnic,difpen]

  let cashBox = cid.map(list => list).reverse()
  for(let i = 0; i < cashBox.length; i++){
    cashBox[i][1] = Math.round(cashBox[i][1] *100)
  }

  let answerArr = []
  for(let i = 0; i < difArr.length; i++){
    if(dif < difArr[i].num){
      dif = dif
    } else if(difArr[i].rem(dif) == 0){ 
      if(cashBox[i][1] >= dif){
        answerArr.push([difArr[i].name, dif/100])
        dif = 0 
      } else if (cashBox[i][1] < dif){
        answerArr.push([difArr[i].name, cashBox[i][1]/100])
        dif = dif - cashBox[i][1]
      }
    }else {
      if(cashBox[i][1] >= dif - difArr[i].rem(dif)){
        answerArr.push([difArr[i].name, (dif - difArr[i].rem(dif))/100])
        dif = difArr[i].rem(dif)
      } else if (cashBox[i][1] < dif - difArr[i].rem(dif)){
        answerArr.push([difArr[i].name, cashBox[i][1]/100])
        dif = dif - cashBox[i][1]
      }
    }
  }

  let sumReturned = 0
  for(let i = 0; i < answerArr.length; i++){
    sumReturned += answerArr[i][1]
  }
  console.log(sumReturned)

  let cashBoxSum = 0
  for(let i = 0; i < cid.length; i++){
    cashBoxSum += cid[i][1]/100
  }
  console.log(cashBoxSum)

  if(cash - price == cashBoxSum){
    return new Answer("CLOSED",cid.map(list => [list[0],list[1]/100]))
  } else if(sumReturned >= cash - price){
    return new Answer("OPEN",answerArr)
  } else if(cashBoxSum/100 < cash - price){
    return new Answer("INSUFFICIENT_FUNDS",[])
  }

}


//End Final Code

const { diff } = require("jest-diff")

function checkCashRegister(price, cash, cid) {
  let dif = (cash - price)*100
  
  if(dif < 0){
    return new Answer("INSUFFICIENT_FUNDS",[])
  } if(change > 0){
    
  }
}


function Answer(status, change){
  this.status = status
  this.change = change
}


let dif100 = {
  rem : function(n){return n%10000},
  num: 10000,
  name : "ONE HUNDRED"} // 0
let dif20 = {
  rem : function(n){return n%2000},
  num: 2000,
  name : "TWENTY"}  // 1
let dif10 = {
  rem : function(n){return n%1000},
  num: 1000,
  name : "TEN"}   // 2
let dif5 = {
  rem : function(n){return n%500},
  num: 500,
  name: "FIVE"}     // 3
let dif1 = {
  rem : function(n){return n%100},
  num: 100,
  name: "ONE"}     // 4
let difqu = {
  rem : function(n){return n%25},
  num: 25,
  name: "QUARTER"} // 5
let difdime ={
  rem : function(n){return n%10},
  num: 10,
  name: "DIME"}//6
let difnic = {
  rem : function(n){return n%5},
  num: 5,
  name: "NICKEL"} //7
let difpen = {
  rem : function(n){return n%1},
  num: 1,
  name: "PENNY"} //8

let difArr = [dif100,dif20,dif10,dif5,dif1,difqu,difdime,difnic,difpen]
//this array of objects calls is for iterating

dif = 10100 //times 100
answerArr = []

while(dif > 0){ //while the difference between cash - price is possible run below function
  for(let i = 0; i < difArr.length; i++){
    if(difArr[i].rem(dif) == 0){ //if remainder after dif/current bill is 0 (even change)

      answerArr.push([difArr[i].name, dif/difArr[i].num])//push Name of bill and the total value of bills ()
      dif = 0

    }else if (difArr[i].rem(dif) > 0){

      let count = (dif-difArr[i].rem(dif))/difArr[i].num
      answerArr.push([difArr[i].name, count*difArr[i].num/100])
      dif = difArr[i].rem(dif)

    }
  }
}
answerArr
//this will return the exact change if all bills are available in the cash drawer\
//also, I was lazy and just timed everything by 100 instead of accoutning for the .cents
//so rememebr to times the dif value by 100 also 

function Receiver(x,y){
  this[`${x}`] = y
}

cid = [["PENNY", 1.01], ["NICKEL", 2.05], ["DIME", 3.1],
 ["QUARTER", 4.25], ["ONE", 90], ["FIVE", 55], ["TEN", 20],
  ["TWENTY", 60], ["ONE HUNDRED", 100]]

let cashBox = cid.reverse()

for(let i = 0; i < cashBox.length; i++){
  cashBox[i][1] = Math.round(cashBox[i][1] *100)
}

dif = 18000 //times 100
answerArr = []
while(dif > 0){ //while the difference between cash - price is possible run below function
  for(let i = 0; i < difArr.length; i++){
    if(dif-difArr[i].rem(dif) >= cashBox[i][1]){
      answerArr.push([difArr[i].name,cashBox[i][1]]/100)
      dif = dif - cashBox[i][1]
    }else if(difArr[i].rem(dif) == 0 && cashBox[i][1] >= dif){ 
      //if remainder after dif/current bill is 0 (even change), and
      // the value of the current bill in cashbox is greater than the current dif value
      answerArr.push([difArr[i].name, dif/100])
      //push Name of bill and the total value of bills ()
      dif = 0 //exit while loop
    }else if (difArr[i].rem(dif) == 0){ // if the remainer (there is less current bill than required)
      answerArr.push([difArr[i].name,cashBox[i][1]]/100) // give whatver is in cashbox of current bill
      dif = dif - (cashBox[i][1]) // new dif value is current dif minus cashbox
    }else if (difArr[i].rem(dif) > 0 && cashBox[i][1] >= dif-difArr[i].rem(dif)){ 
    // if the remainder of dif/current bill is more than 0 and
    // the value in cashebox of current bill is >= than the current dif value - remainder value
      answerArr.push([difArr[i].name, (dif-difArr[i].rem(dif))/100]) // give whatver is in cashbox of current bill
      dif = difArr[i].rem(dif) //new dif value is remainder * 100
    } 
    else { //terminal condition --> the final value is > than money in cash box...
      dif = 0
    }
  }
}
answerArr


dif = 18000
answerArr = []
  for(let i = 0; i < difArr.length; i++){
    if(dif < difArr[i].num){
      dif = dif
    } else if(difArr[i].rem(dif) == 0){ 
      if(cashBox[i][1] >= dif){
        answerArr.push([difArr[i].name, dif/100])
        dif = 0 
      } else if (cashBox[i][1] < dif){
        answerArr.push([difArr[i].name, cashBox[i][1]/100])
        dif = dif - cashBox[i][1]
      }
    }else {
      if(cashBox[i][1] >= dif - difArr[i].rem(dif)){
        answerArr.push([difArr[i].name, (dif - difArr[i].rem(dif))/100])
        dif = difArr[i].rem(dif)
      } else if (cashBox[i][1] < dif - difArr[i].rem(dif)){
        answerArr.push([difArr[i].name, cashBox[i][1]/100])
        dif = dif = dif - cashBox[i][1]
      }
    }
  }
answerArr


function Answer(status, change){
  this.status = status
  this.change = change
}

let sumReturned = 0
for(let i = 0; i < answerArr.length; i++){
  sumReturned += answerArr[i][1]
}

let cashBoxSum = 0
for(let i = 0; i < cid.length; i++){
  cashBoxSum += cid[i][1]
}

//version 1
function checkCashRegister(price, cash, cid) {
  let dif = (cash - price)*100

  function Answer(status, change){
    this.status = status
    this.change = change
  }

  let dif100 = {
    rem : function(n){return n%10000},
    num: 10000,
    name : "ONE HUNDRED"} // 0
  let dif20 = {
    rem : function(n){return n%2000},
    num: 2000,
    name : "TWENTY"}  // 1
  let dif10 = {
    rem : function(n){return n%1000},
    num: 1000,
    name : "TEN"}   // 2
  let dif5 = {
    rem : function(n){return n%500},
    num: 500,
    name: "FIVE"}     // 3
  let dif1 = {
    rem : function(n){return n%100},
    num: 100,
    name: "ONE"}     // 4
  let difqu = {
    rem : function(n){return n%25},
    num: 25,
    name: "QUARTER"} // 5
  let difdime ={
    rem : function(n){return n%10},
    num: 10,
    name: "DIME"}//6
  let difnic = {
    rem : function(n){return n%5},
    num: 5,
    name: "NICKEL"} //7
  let difpen = {
    rem : function(n){return n%1},
    num: 1,
    name: "PENNY"} //8

  let difArr = [dif100,dif20,dif10,dif5,dif1,difqu,difdime,difnic,difpen]

  let cashBox = cid.reverse()
  for(let i = 0; i < cashBox.length; i++){
    cashBox[i][1] = Math.round(cashBox[i][1] *100)
  }

  let answerArr = []
  for(let i = 0; i < difArr.length; i++){
    if(dif < difArr[i].num){
      dif = dif
    } else if(difArr[i].rem(dif) == 0){ 
      if(cashBox[i][1] >= dif){
        answerArr.push([difArr[i].name, dif/100])
        dif = 0 
      } else if (cashBox[i][1] < dif){
        answerArr.push([difArr[i].name, cashBox[i][1]/100])
        dif = dif - cashBox[i][1]
      }
    }else {
      if(cashBox[i][1] >= dif - difArr[i].rem(dif)){
        answerArr.push([difArr[i].name, (dif - difArr[i].rem(dif))/100])
        dif = difArr[i].rem(dif)
      } else if (cashBox[i][1] < dif - difArr[i].rem(dif)){
        answerArr.push([difArr[i].name, cashBox[i][1]/100])
        dif = dif = dif - cashBox[i][1]
      }
    }
  }

  if(answerArr.length > 0){
    return new Answer("OPEN",answerArr)
  } else {
    return new Answer("INSUFFICIENT_FUNDS",[])
  }

}

