/**
 * Created by yuriel on 12/5/16.
 */

var TARGET_URL = 'http://www.chunyuyisheng.com/cyadmin/news/healthnews/add/';
function openTarget(cb) {
    chrome.tabs.create({ url: TARGET_URL }, function(tab) {
        listener = function(tabId, info) {
            if(tab.id == tabId && info.status == "complete") {
                cb(tab);
            }
            chrome.tabs.onUpdated.removeListener(listener);
        };
        chrome.tabs.onUpdated.addListener(listener);
    });
}

chrome.browserAction.onClicked.addListener(function() {
    chrome.tabs.query({active:true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {action: "get_article"}, function(response) {
            // alert(response.article);
            if ('article' in response) {
                openTarget(function (tab) {
                    chrome.tabs.sendMessage(tab.id, {action: "fill", text: response.article}, function (response) {
                        alert(response.status);
                    });
                });
            }
        });
    });
});