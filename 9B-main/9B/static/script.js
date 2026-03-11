function abrirIA(){
    let chat = document.getElementById("iaChat");
    chat.style.display = chat.style.display === "block" ? "none" : "block";
}

function enviarIA(){
    let input = document.getElementById("iaInput");
    let msg = input.value;

    if(msg === "") return;

    let mensagens = document.getElementById("iaMensagens");
    mensagens.innerHTML += "<p><b>Você:</b> " + msg + "</p>";

    fetch("/ia", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({pergunta: msg})
    })
    .then(res => res.json())
    .then(data => {
        mensagens.innerHTML += "<p><b>TPG:</b> " + data.resposta + "</p>";
        mensagens.scrollTop = mensagens.scrollHeight;
    });

    input.value = "";
}