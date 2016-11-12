var path = require('path');
var fs = require('fs');
var express = require('express');
var exphbs = require('express-handlebars');
var less = require('less');
var app = express();
var html_dir = path.join(__dirname, 'source/');
var less_file_path = path.join(__dirname, 'source/less/index.less');

app.engine('handlebars', exphbs());
app.set('view engine', 'handlebars');
app.set('views', html_dir);

app.locals.baseColor = '003366';

var generateStyles = function(baseColor) {
    console.log('generate styles');
    return new Promise(function(resolve, reject) {
        if (!baseColor) {
            baseColor = app.locals.baseColor;
        }
        var options = {
            filename: less_file_path,
            sourceMap: {
                sourceMapFileInline: true
            }
        };
        fs.readFile(less_file_path, "utf8", function(err, data) {
            if (err) throw err;
            var baseColorString = '@base-color: #' + baseColor + ';';
            data = baseColorString + data;
            var options = {
                filename: less_file_path
            };
            console.log(options);
            less.render(data, options)
                .then(function(output) {
                    resolve(output.css);
                }, function(error) {
                    throw err;
                });
        });
    });
}
app.get('/:baseColor?', function(req, res) {
    console.log('has base color?')
    var baseColor = req.params.baseColor;
    console.log(baseColor);
    if (!baseColor) {
        console.log('no base color')
        res.render('index', {
            styles: '',
            static_css: true
        });
        // If there's no base color specified in the url,
        // just send the static html pointing to the compiled css
        // res.sendFile(path.join(__dirname, '/index.html'));
    } else {
        console.log('has base color')
        // If the url includes a base color, generate the css,
        // use the handlebars template, and render the css in the <style> tag
        generateStyles(baseColor).then(function(css){
            res.render('index', {
                styles: css,
                static_css: false
            });
        });
    }
});

app.get('/less/:baseColor', function(req, res) {
    console.log('ajax get');
    generateStyles(req.params.baseColor).then(function(css){
        res.send(css);
    })
});


app.use(express.static(path.join(__dirname, 'public', 'static')));

var server = app.listen('3000', function() {
    console.log('Listening on port %d', server.address().port);
});