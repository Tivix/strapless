var path = require('path');
var http = require('http');
var fs = require('fs');
var express = require('express');
var exphbs = require('express-handlebars');
var less = require('less');
var app = express();
var html_dir = path.join(__dirname, 'views/');
var demo_file_path = path.join(__dirname, 'source/less/index.less');
var strapless_file_path = path.join(__dirname, 'source/less/strapless/strapless.less');
var css_file_path = path.join(__dirname, 'source/less/strapless/strapless-css.less');

var hbs = exphbs.create({
    // Specify helpers which are only registered on this instance.
    helpers: {
        foo: function () { return 'FOO!'; },
        bar: function () { return 'BAR!'; }
    }
});

app.engine('handlebars', hbs.engine);
app.set('view engine', 'handlebars');

app.get('/', function (req, res, next) {
    res.render('home', {
        showTitle: true,

        // Override `foo` helper only for this rendering.
        helpers: {
            foo: function () { return 'foo.'; }
        }
    });
});

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
        res.render('home', {
            styles: '',
            static_css: true
        });
    } else {
        var validHex = /^(?:[0-9a-f]{3}){1,2}$/i.test(baseColor);
        if (validHex) {
            // If the url includes a base color, generate the css,
            // use the handlebars template, and render the css in the <style> tag
            generateStyles(baseColor, demo_file_path).then(function(css){
                res.render('home', {
                    styles: css,
                    static_css: false
                });
            });
        } else {
            res.render('home', {
                styles: '',
                static_css: true,
                invalid_hex: true
            });
        }
    }
});

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

http.createServer(app).listen(8000);
