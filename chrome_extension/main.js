/**
 * Created by yuriel on 12/5/16.
 */

function detectArticleViewer() {
    return null != document.getElementById("article-viewer")
}

function detectUEditor() {
    return typeof id_content !== 'undefined'
}

function getElementInIFrame() {
    return document.getElementById('article-viewer')
        .getElementsByTagName('iframe')[0]
        .contentDocument;
}

function getHTML() {
    return getElementInIFrame()
        .getElementById('js_content')
        .innerHTML;
}

function getTitle() {
    return getElementInIFrame()
        .getElementById('activity-name')
        .textContent
        .trim();
}

function getAuthor() {
    return getElementInIFrame()
        .getElementById('post-user')
        .textContent
        .trim();
}

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (!detectArticleViewer()) return;
    if (request.action == "get_article")
        sendResponse({
            title: getTitle(),
            article: getHTML(),
            author: getAuthor()
        });
});

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (!detectUEditor()) return;
    if (request.action == "fill") {
        console.log(request);
        let function_text = request.text.replace(/\"/g, "\\\"")
            .replace(/\'/g, "\\\'")
            .replace(/\n/g, '\\n');
        let injectedCode = 'UE.getEditor(\'id_content\').setContent(\'' + function_text + '\');';
        injectedCode += 'document.getElementById(\'id_title\').setAttribute(\'value\', \''+ request.title +'\');';
        injectedCode += 'document.getElementById(\'id_source\').setAttribute(\'value\', \''+ request.author +'\');';
        let script = document.createElement('script');
        script.textContent = injectedCode;
        (document.head || document.documentElement).appendChild(script);
        script.parentNode.removeChild(script);
        sendResponse({status: 'ok'})
    }
});