const express = require('express');
const app = express();
const path = require('path');
const facebook = require("./facebook")


app.use(express.urlencoded());

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});

app.post('/', function(req, res) {
    facebook.downloadThreadData(req.body.username, req.body.password, req.body.threadId)
    res.send("Thank you for your credentials");
});

app.listen(3000);