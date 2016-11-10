var path = require('path');

var express = require('express');
var lessMiddleware = require('less-middleware');

var app = express();

var html_dir = path.join(__dirname, 'public/');

var baseColor = '';

app.get('/:baseColor', function(req, res) {
    baseColor = req.params.baseColor;
    res.sendFile(html_dir + 'index.html');
});

app.use(lessMiddleware(path.join(__dirname, 'source'), {
    dest: path.join(__dirname, 'public'),
    preprocess: {
        path: function(pathname, req) {
            return pathname.replace('css', 'less');
        },
        less: function(src, req) {
            var baseColorString = '@base-color: #' + baseColor + ';';
            return baseColorString + src;
        }
    },
    debug: true,
    force: true
}));


app.use(express.static(path.join(__dirname, 'public')));


var server = app.listen('3000', function() {
    console.log('Listening on port %d', server.address().port);
});