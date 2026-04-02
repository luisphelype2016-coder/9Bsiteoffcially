function mudarTema(tema){

    // salva no backend (Flask)
    fetch("/mudar_tema/" + tema)
    .then(() => {

        // aplica no body sem precisar recarregar
        document.body.className = tema

    })

}