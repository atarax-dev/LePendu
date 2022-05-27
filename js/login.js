let logLeft = document.getElementById("block-log-left");
let logRight = document.getElementById("block-log-right");
console.log(logLeft)



logLeft.addEventListener('mouseover', function mouseOverLeft(){
    logLeft.style.transform = "scale(1.05)";
    logRight.style.transform = "scale(0.95)";
    logRight.style.filter = "blur(2px)";
})
logLeft.addEventListener('mouseout' , function mouseOutLeft(){
    logLeft.style.transform = "scale(1)";    
    logRight.style.transform = "scale(1)";
    logRight.style.filter = "blur(0)";
})
logRight.addEventListener('mouseover' , function mouseOverRight (){
    logRight.style.transform = "scale(1.05)";
    logLeft.style.transform = "scale(0.95)";
    logLeft.style.filter = "blur(2px)";
})
logRight.addEventListener('mouseout' , function mouseOutRight(){
    logRight.style.transform = "scale(1)";    
    logLeft.style.transform = "scale(1)";
    logLeft.style.filter = "blur(0)";
})

let btnLogLeft = document.getElementById("btn-log-left");
let btnLogRight = document.getElementById("btn-log-right");

btnLogLeft.addEventListener('mouseover' , function btnCilckLeft (){
    logLeft.style.transform = "scale(1)"
})
btnLogLeft.addEventListener('mouseout' , function btnOutLeft (){
    logLeft.style.transform = "scale(0)"
})
btnLogRight.addEventListener('mouseover' , function btnCilckRight (){
    logRight.style.transform = "scale(1)"
})
btnLogRight.addEventListener('mouseout' , function btnOutRight (){
    logRight.style.transform = "scale(0)"
})
