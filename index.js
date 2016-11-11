var path = require('path');
var fs = require('fs');
var express = require('express');
// var lessMiddleware = require('less-middleware');
var less = require('less');
var app = express();

var html_dir = path.join(__dirname, 'source/');

app.locals.baseColor = '003366';

app.get('/', function(req, res) {
    // var baseColor = req.params.baseColor;
    // if(!baseColor){
    //     baseColor = app.locals.baseColor;
    // }
    res.sendFile(html_dir + 'index.html');
});

app.get('/less/:baseColor?', function(req, res) {
    var file_path = path.join(__dirname, 'source/less/index.less');
    var baseColor = req.params.baseColor;
    if(!baseColor){
        baseColor = app.locals.baseColor;
    }
    fs.readFile(file_path, "utf8", function(err, data) {
        if (err) throw err;
        var options = {
            filename: file_path,
            sourceMap: {
                sourceMapFileInline: true
            }
        };
        var baseColorString = '@base-color: #' + baseColor + ';';
        data = baseColorString + data;
        less.render(data, options, function(error, output){
            res.header("Content-type", "text/css");
            res.send(output.css);
        });
    });
});


app.use(express.static(path.join(__dirname, 'public', 'static')));

var server = app.listen('3000', function() {
    console.log('Listening on port %d', server.address().port);
});
