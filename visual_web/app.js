var express = require('express');
var path = require('path');
var proxy = require('express-http-proxy');

var app = express();
var APP_PORT = 3030;

app.get('/index', function(req, res) {
    res.sendFile(path.join(__dirname, '/src/template/index.html'))
})

app.use(express.static('src'));

app.get('/papers/*', proxy('localhost:9200'));

app.post('/papers/*', proxy('localhost:9200'));

app.listen(APP_PORT);

module.exports = app;
