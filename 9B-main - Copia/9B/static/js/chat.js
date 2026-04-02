setInterval(() => {
    fetch("/chat_dados")
    .then(r => r.text())
    .then(data => {
        document.getElementById("chat").innerHTML = data;
    });
}, 2000);