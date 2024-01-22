var zBool = NULL;

function changeText(myBool){
    var btn = document.getElementById("submit");

    if (myBool == "NULL"){
        btn.innerHTML="Submit Time";
    }else if (myBool == true){
        btn.innerHTML="Time in";
    }else{
        btn.innerHTML="Time out";
    }

}
function pipeLine(myBool){
    zBool = myBool;
    return NULL;
}
