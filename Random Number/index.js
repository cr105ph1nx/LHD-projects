const hash = Math.PI/666;
var last, num;

function randomNumber(){
    while(num == last)
        num = (new Date().getTime()) * hash;
        num = Math.floor(num);

    return last = num;
}

// Output
console.log(randomNumber());
