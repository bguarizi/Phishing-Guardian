chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.url) {
        alert("URL atual: " + message.url);
    }
});
