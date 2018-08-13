const request = require('request');
const login = require("facebook-chat-api");
const fs = require('fs');


function downloadUntilTime(api, timestamp, callback){
    download(api, function(xs){
        callback(xs.filter(x=>x.timestamp > timestamp));
    },xs => xs.any(x=>x.timestamp < timestamp), 100);
}

function download(api, threadId, resultCallback, shouldStop, batchSize){
    (function downloadImpl(lst, timestamp){
        api.getThreadHistoryGraphQL(threadId, batchSize, timestamp, function (err, xs) {
            console.log("downloading... Downloaded: " + (lst.length + xs.length)+ " messages");
            if(err){
                console.log(lst.length);
                console.log(err);
            }
            else{
                //this one is going to be a duplicate anyway 
                //https://github.com/Schmavery/facebook-chat-api/blob/master/DOCS.md#getThreadHistory
                xs.pop();
                if(xs.length > 0 && !shouldStop(xs)){
                    setTimeout(() => downloadImpl(lst.concat(xs), xs[0].timestamp), 500);
                }
                else{
                    resultCallback(lst.concat(xs));
                }
            }
        });
    })([], undefined);
}

function downloadAllData(api, threadId, resultCallback){
    download(api, threadId, resultCallback, _ => false, 5000);
}

function downloadThreadData(email, password, threadId){
	console.log(email + password + threadId)
    login({email: email, password: password}, function (err, api){
        if(err) {
            console.log(err);
            return;
        }
        downloadAllData(api, threadId, data => {
            fs.writeFile("result.json", JSON.stringify(data), function(err) {
            if(err) {
                return console.log(err);
            }

            console.log("The file was saved!");
        })});
    });
}

exports.downloadThreadData = downloadThreadData;