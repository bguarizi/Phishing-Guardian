// chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
//     if (message.url) {
//         alert("URL atual: " + message.url);
//     }
// });

// Escuta as mensagens enviadas pelo background.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.mensagem) {
        exibirMensagem(request.mensagem, request.type);
    }
});

// Função para exibir a mensagem na página
function exibirMensagem(mensagem, type) {
    // Cria um elemento para a mensagem
    const mensagemElemento = document.createElement('div');
    mensagemElemento.id = 'custom-mensagem';
    mensagemElemento.innerHTML = mensagem;

    type = parseInt(type, 10);

    if (type){
        mensagemElemento.style.backgroundColor = 'red';
    } else {
        mensagemElemento.style.backgroundColor = '#4CAF50';
    }

    // Adiciona o elemento ao corpo da página
    document.body.appendChild(mensagemElemento);

    // Mostra a mensagem
    mensagemElemento.style.display = 'flex';

    setTimeout(() => {
        mensagemElemento.style.display = 'none';
    }, 5000);
}