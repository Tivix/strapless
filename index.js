var path = require('path');
var http = require('http');
var https = require('https');
var fs = require('fs');
var express = require('express');
var exphbs = require('express-handlebars');
var less = require('less');
var app = express();
var html_dir = path.join(__dirname, 'source/');
var demo_file_path = path.join(__dirname, 'source/less/index.less');
var strapless_file_path = path.join(__dirname, 'source/less/strapless/strapless.less');
var css_file_path = path.join(__dirname, 'source/less/strapless/strapless-css.less');

app.engine('handlebars', exphbs());
app.set('view engine', 'handlebars');
app.set('views', html_dir);

var generateStyles = function(baseColor, filepath) {
    return new Promise(function(resolve, reject) {
        var options = {
            filename: filepath,
            sourceMap: {
                sourceMapFileInline: true
            }
        };
        fs.readFile(filepath, "utf8", function(err, data) {
            if (err) throw err;
            var baseColorString = '@base-color: #' + baseColor + ';';
            data = data + baseColorString;
            var options = {
                filename: filepath
            };
            less.render(data, options)
                .then(function(output) {
                    resolve(output.css);
                }, function(error) {
                    throw err;
                });
        });
    });
}

app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.get('/:baseColor?', function(req, res) {
    var baseColor = req.params.baseColor;
    if (!baseColor) {
        res.render('index', {
            styles: '',
            static_css: true
        });
        // If there's no base color specified in the url,
        // just send the static html pointing to the compiled css
        // res.sendFile(path.join(__dirname, '/index.html'));
    } else {
        var validHex = /^(?:[0-9a-f]{3}){1,2}$/i.test(baseColor);
        if (validHex) {
            // If the url includes a base color, generate the css,
            // use the handlebars template, and render the css in the <style> tag
            generateStyles(baseColor, demo_file_path).then(function(css){
                res.render('index', {
                    styles: css,
                    static_css: false
                });
            });
        } else {
            res.render('index', {
                styles: '',
                static_css: true,
                invalid_hex: true
            });
        }
    }
});

// app.get('/download/:baseColor', function(req, res) {
//     generateStyles(req.params.baseColor, strapless_file_path).then(function(css){
//         res.header("Content-Disposition", "attachment;filename=Library#" + req.params.baseColor + ".css");
//         res.header("Content-type", "text/css");
//         res.send(css);
//     })
// });

app.get('/democss/:baseColor', function(req, res) {
    generateStyles(req.params.baseColor, demo_file_path).then(function(css){
        res.header("Content-Disposition", "attachment;filename=DEMOCSS_#" + req.params.baseColor + ".css");
        res.header("Content-type", "text/css");
        res.send(css);
    })
});

app.get('/css-version/:baseColor', function(req, res) {
    generateStyles(req.params.baseColor, css_file_path).then(function(css){
        res.header("Content-Disposition", "attachment;filename=Strapless_#" + req.params.baseColor + ".css");
        res.header("Content-type", "text/css");
        res.send(css);
    })
});

app.use(express.static(path.join(__dirname, 'public', 'static')));

var sslOptions = {
  key: fs.readFileSync('key.pem'),
  cert: fs.readFileSync('cert.pem'),
  passphrase: 'strapless',
};

https.createServer(sslOptions, app).listen(8443)
