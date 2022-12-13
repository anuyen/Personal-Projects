//          Roman Numeral Converter


function convertToRoman(num) {
    let answer = []
    function split1000(num){return [Math.floor(num/1000), num%1000]}
    function split100(num){return [Math.floor(num/100), num%100]}
    function split10(num){return [Math.floor(num/10), num%10]}


    for(let i = 0; i < split1000(num)[0]; i++){
        answer.push('M')
    }

    let num100 = split1000(num)[1]
    let h = split100(num100)[0]
    if(h == 5){
        answer.push('D')
    } else if(h == 9){
        answer.push('CM')
    }else if(8 >= h && h >= 6){
        answer.push('D')
        let dif = h - 5
        for(let i = 0; i < dif; i++){
            answer.push('C')
        }
    } else if(h == 4){
        answer.push('CD')
    }   else if(3 >= h && h >= 1){
        for(let i = 0; i < h; i++){
            answer.push('C')
        }
    }

    let num10 = split100(num100)[1]
    let t = split10(num10)[0]
    if(t == 5){
        answer.push('L')
    } else if(t == 9){
        answer.push('XC')
    }else if(8 >= t && t >= 6){
        answer.push('L')
        let dif = t - 5
        for(let i = 0; i < dif; i++){
            answer.push('X')
        }
    } else if(t == 4){
        answer.push('XL')
    }   else if(3 >= t && t >= 1){
        for(let i = 0; i < t; i++){
            answer.push('X')
        }
    }

    let f = split10(num10)[1]
    if(f == 5){
        answer.push('V')
    } else if(f == 9){
        let dif = 10 - f
        for(let i = 0; i < dif; i++){
            answer.push('I')
        }
        answer.push('X')
    }else if(8 >= f && f >= 6){
        answer.push('V')
        let dif = f - 5
        for(let i = 0; i < dif; i++){
            answer.push('I')
        }
    } else if(f == 4){
        answer.push('IV')
    }   else if(3 >= f && f >= 1){
        for(let i = 0; i < f; i++){
            answer.push('I')
        }
    }

    return answer.join("");
}
   
convertToRoman(36);