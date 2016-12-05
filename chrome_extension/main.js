/**
 * Created by yuriel on 12/5/16.
 */

function detectArticleViewer() {
    return null != document.getElementById("article-viewer")
}

function detectUEditor() {
    return typeof id_content !== 'undefined'
}

function getHTML() {
    return document.getElementById('article-viewer')
        .getElementsByTagName('iframe')[0]
        .contentDocument
        .getElementsByTagName('body')[0]
        .innerHTML
}

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (!detectArticleViewer()) return;
    if (request.action == "get_article")
        sendResponse({article: getHTML()});
});

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (!detectUEditor()) return;
    if (request.action == "fill") {
        // UE.getEditor('id_content').setContent(request.text);
        function_text = request.text.replace(/\"/g, "\\\"")
            .replace(/\'/g, "\\\'")
            .replace(/\n/g, '\\n');
        var injectedCode = 'UE.getEditor(\'id_content\').setContent(\'' + function_text + '\')';
        var script = document.createElement('script');
        script.textContent = injectedCode;
        (document.head || document.documentElement).appendChild(script);
        script.parentNode.removeChild(script);
    }
});