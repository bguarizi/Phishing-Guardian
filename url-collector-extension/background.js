// function mostrarAlerta(mensagem) {
//     var divAlerta = document.createElement('div');
//     divAlerta.id = 'erro';
//     divAlerta.textContent = mensagem;
//     divAlerta.style.position = 'fixed';
//     divAlerta.style.top = '10px';
//     divAlerta.style.left = '50%';
//     divAlerta.style.transform = 'translateX(-50%)';
//     divAlerta.style.padding = '10px';
//     divAlerta.style.background = '#ff9999';
//     divAlerta.style.border = '1px solid #cc6666';
//     divAlerta.style.borderRadius = '5px';
//     divAlerta.style.zIndex = '9999';
//     divAlerta.style.display = 'block';

//     document.body.appendChild(divAlerta);

//     setTimeout(function() {
//         divAlerta.style.display = 'none';
//     }, 3000); // Tempo em milissegundos (3000 = 3 segundos)
// }

// Função para enviar a mensagem para o content.js
function sendMessage(mensagem, type) {
    // Obtém a aba ativa
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs.length > 0) {
            const tabId = tabs[0].id;
            chrome.tabs.sendMessage(tabId, { mensagem: mensagem, type: type });
        }
    });
}

// chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
//     if (changeInfo.status == 'complete') {
//         var url = tab.url;
//         sendUrlToServer(url);
//     }
// });

chrome.webNavigation.onBeforeNavigate.addListener((details) => {
    if (details.frameId === 0) { // Verifica se é o frame principal (não um iframe)
        const url = details.url;
        sendUrlToServer(url);
    }
});

function sendUrlToServer(url) {
    fetch('http://localhost:5000/receive_url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Resposta do servidor:', data);
        if (data.message) {

            sendMessage(data.message, data.type);

            // mostrarAlerta(data.message);
            // alert(data.message);
        } else {
            sendMessage('Resposta do servidor vazia ou inválida.', -1);
            // mostrarAlerta('Resposta do servidor vazia ou inválida.');
            // alert("Error");
        }
    })
    .catch(error => {
        // console.error('Erro ao enviar URL:', error);
        mostrarAlerta("ERRO DE COMUNICAÇÃO!\nVerifique se o software está executando corretamente.\nCaso não queira mais receber este alerta, desative a extensão nas configurações do navegador.");
        // alert("ERRO DE COMUNICAÇÃO!\nVerifique se o software está executando corretamente.\nCaso não queira mais receber este alerta, desative a extensão nas configurações do navegador.");
    });
}
