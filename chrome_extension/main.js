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

function cleanStyles(html) {
    // Remove all SPAN tags
    html = html.replace(/<\/?SPAN[^>]*>/gi, "" );
    // Remove all A tags
    html = html.replace(/<\/?A[^>]*>/gi, "" );
    // Remove all font tags
    html = html.replace(/<\/?font[^>]*>/gi, "" );
    // Remove all u tags
    html = html.replace(/<\/?u[^>]*>/gi, "" );
    html = html.replace(/<\/?section[^>]*>/gi, "");
    // Remove onmouseover attributes
    html = html.replace(/<(\w[^>]*) onmouseover=([^ |>]*)([^>]*)/gi, "<$1$3");
    // Remove onmouseout attributes
    html = html.replace(/<(\w[^>]*) onmouseout=([^ |>]*)([^>]*)/gi, "<$1$3");

    // Remove Class attributes
    html = html.replace(/<(\w[^>]*) class=([^ |>]*)([^>]*)/gi, "<$1$3");
    // Remove Face attributes
    html = html.replace(/<(\w[^>]*) face=([^ |>]*)([^>]*)/gi, "<$1$3");
    // Remove Size attributes
    html = html.replace(/<(\w[^>]*) size=([^ |>]*)([^>]*)/gi, "<$1$3");
    // Remove X:num attributes
    html = html.replace(/<(\w[^>]*) x:num=([^ |>]*)([^>]*)/gi, "<$1$3");
    // Remove Width attributes
    html = html.replace(/<(\w[^>]*) width=([^ |>]*)([^>]*)/gi, "<$1$3");
    // Remove Height attributes
    html = html.replace(/<(\w[^>]*) height=([^ |>]*)([^>]*)/gi, "<$1$3");
    // Remove Class attributes
    html = html.replace(/<(\w[^>]*) class=([^ |>]*)([^>]*)/gi, "<$1$3");
    // Remove Style attributes
    html = html.replace(/<(\w[^>]*) style="([^"]*)"([^>]*)/gi, "<$1$3");
    // Remove Lang attributes
    html = html.replace(/<(\w[^>]*) lang=([^ |>]*)([^>]*)/gi, "<$1$3");
    // Remove XML elements and declarations
    html = html.replace(/<\\?\?xml[^>]*>/gi, "");
    // Remove Tags with XML namespace declarations: <o:p></o:p>
    html = html.replace(/<\/?\w+:[^>]*>/gi, "");
    // Replace the &nbsp;
    html = html.replace(/&nbsp;/gi, " " );

    // // Transform <P> to <DIV>
    // let re = new RegExp("(<P)([^>]*>.*?)(<\/P>)","gi"); // Different because of a IE 5.0 error
    // html = html.replace( re, "<p$2</p>" );

    html=html.replace(/ x:num/g,"");

    html = html.replace(/<p>[<br>|<br/>| ]*<\/p>/gi, "");

    return html;
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
        let function_text = request.text;
        for (let i = 0; i < 10; i ++) {
          function_text = cleanStyles(function_text);
        }
        function_text = function_text.replace(/"/g, "\\\"")
          .replace(/'/g, "\\\'")
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
