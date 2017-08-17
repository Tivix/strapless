'use strict';

var Promise = global.Promise || require('promise');

var path = require('path');
var http = require('http');
var fs = require('fs');
var less = require('less');
var express = require('express'),
    exphbs  = require('express-handlebars/'), // "express-handlebars"
    helpers = require('./lib/helpers');

var app = express();


// var html_dir = path.join(__dirname, 'views/');
var demo_file_path = path.join(__dirname, 'source/less/index.less');
var strapless_file_path = path.join(__dirname, 'source/less/strapless/strapless.less');
var css_file_path = path.join(__dirname, 'source/less/strapless-css.less');

// Create `ExpressHandlebars` instance with a default layout.
var hbs = exphbs.create({
    defaultLayout: 'main',
    helpers      : helpers,

    // Uses multiple partials dirs, templates in "shared/templates/" are shared
    // with the client-side of the app (see below).
    partialsDir: [
        'shared/templates/',
        'views/partials/'
    ]
});

// Register `hbs` as our view engine using its bound `engine()` function.
app.engine('handlebars', hbs.engine);
app.set('view engine', 'handlebars');

// CORS
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

// Middleware to expose the app's shared templates to the client-side of the app
// for pages which need them.
function exposeTemplates(req, res, next) {
    // Uses the `ExpressHandlebars` instance to get the get the **precompiled**
    // templates which will be shared with the client-side of the app.
    hbs.getTemplates('shared/templates/', {
        cache      : app.enabled('view cache'),
        precompiled: true
    }).then(function (templates) {
        // RegExp to remove the ".handlebars" extension from the template names.
        var extRegex = new RegExp(hbs.extname + '$');

        // Creates an array of templates which are exposed via
        // `res.locals.templates`.
        templates = Object.keys(templates).map(function (name) {
            return {
                name    : name.replace(extRegex, ''),
                template: templates[name]
            };
        });

        // Exposes the templates during view rendering.
        if (templates.length) {
            res.locals.templates = templates;
        }

        setImmediate(next);
    })
    .catch(next);
}

app.get('/', function (req, res) {
    res.render('home', {
        title: 'Home',
        styles: '',
        static_css: true
    });
});

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

app.use(express.static(path.join(__dirname, 'public')));

app.listen(8000, function () {
    console.log('Strapless listening on: 8000');
});
