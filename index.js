const request = require('request');
const login = require("facebook-chat-api");
const fs = require('fs');
const json2csv = require('json2csv');
const threadId = 0 //replace this
const email = ""; //replace this
const password = ""; //replace this


function renameEveryone(api){
    api.getThreadInfo(threadId, function(err, info){
        console.log(info);
        if(!err){
            api.getUserInfo(info.participantIDs, function(err, info){
                if(!err){
                    var values = Object.keys(info).map(key => ({key : key, name : info[key].name}));
                    var shuffleService = { 
                        url: "http://localhost:8081/shuffle",
                        method: 'POST', 
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        json : values
                    }
                    
                    request(shuffleService, function(err, res, body) {
                        if (res && (res.statusCode === 200 || res.statusCode === 201)) {
                            var str = "Shuffle!!!!\n\n";
                            for(var i = 0; i < body.length; i++){
                                str += info[body[i][0]].name + " -> " + body[i][1] + "\n";
                            }
                            api.sendMessage(str, threadId);

                            body.forEach(function(xs, i) {
                                setTimeout(function() {
                                    console.log("body: " + JSON.stringify(body));
                                    console.log(xs[1]);
                                    console.log(+(xs[0]));
                                    api.changeNickname(xs[1], threadId, +(xs[0]),function(err){
                                        if(err){
                                            console.log("Error during the renaming of "+ xs[0] + " to " + xs[1]+"\n"+err);
                                        }
                                    });
                                }, (i + 1) * 1000)
                            }, this);
                        }
                        else{
                            console.log("Error!");
                            console.log(res);
                        }
                    });
                }
            });
        }
    });
}


function downloadUntilTime(api, timestamp, callback){
    download(api, function(xs){
        callback(xs.filter(x=>x.timestamp > timestamp));
    },xs => xs.any(x=>x.timestamp < timestamp), 100);
}

function download(api, resultCallback, shouldStop, batchSize){
    (function downloadImpl(lst, timestamp){
        api.getThreadHistory(threadId, batchSize, timestamp, function (err, xs) {
            console.log("downloading...");
            if(err){
                console.log(err);
                console.log(lst);
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

function downloadAllData(api, resultCallback){
    download(api, resultCallback, _ => false, 5000);
}

function listen(api){
    api.listen(function(err, msg){
        console.log(msg);
        if(err || msg.threadID != threadId){
            return;
        }
        console.log("Got message from groupchat")
    });
}

login({email: email, password: password}, function (err, api){
    if(err) return console.log(err);
    renameEveryone(api);
});

