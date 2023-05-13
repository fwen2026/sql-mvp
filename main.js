function getAndSendData(e){
    window.location = "http://127.0.0.1:5500/index.html";
    let data = new FormData();
    console.log("Worked");
}

let submitButton = document.querySelector("input[name=submit-button]");
submitButton.addEventListener('click', getAndSendData());