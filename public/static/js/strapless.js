var Strapless = (function() {

    function _generateFavicon() {
        console.log('generate fav');
        var canvas = document.createElement('canvas');
        var ctx;
        var link = document.getElementById('favicon');
        var colorbox1 = document.getElementById('get_color1');
        var colorbox2 = document.getElementById('get_color2');
        var colorbox3 = document.getElementById('get_color3');
        var colorbox4 = document.getElementById('get_color4');

        if (canvas.getContext) {
            canvas.height = canvas.width = 16;
            ctx = canvas.getContext('2d');
            var fillcolor1 = window.getComputedStyle(colorbox1).color;
            var fillcolor2 = window.getComputedStyle(colorbox2).color;
            var fillcolor3 = window.getComputedStyle(colorbox3).color;
            var fillcolor4 = window.getComputedStyle(colorbox4).color;

            ctx.fillStyle = fillcolor1;
            ctx.fillRect(1, 1, 7, 7);

            ctx.fillStyle = fillcolor2;
            ctx.fillRect(9, 9, 15, 15);

            ctx.fillStyle = fillcolor3;
            ctx.fillRect(9, 1, 15, 7);

            ctx.fillStyle = fillcolor4;
            ctx.fillRect(1, 9, 7, 15);

            link.href = canvas.toDataURL('image/png');
        }
    };

    function _getLessFile(baseColor) {
        return new Promise(function(resolve, reject) {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/less/' + baseColor);
            xhr.onload = function() {
                if (this.status >= 200 && this.status < 300) {
                    resolve(xhr.response);
                } else {
                    reject({
                        status: this.status,
                        statusText: xhr.statusText
                    });
                }
            };
            xhr.onerror = function() {
                reject({
                    status: this.status,
                    statusText: xhr.statusText
                });
            };
            xhr.send();
        });
    }

    function getStyleSheet(unique_title) {
        for (var i = 0; i < document.styleSheets.length; i++) {
            var sheet = document.styleSheets[i];
            if (sheet.title == unique_title) {
                return sheet;
            }
        }
    }

    function deleteStyleSheets() {
        for (var i = 0; i < document.styleSheets.length; i++) {
            document.head.removeChild(document.styleSheets[i].ownerNode)
        }
    }

    function _updateScheme() {
        var styleBlock = document.getElementById('style_block');
        var baseColor = document.getElementById('seed_color').value;
        var overlay = document.getElementById('loading_overlay');
        overlay.style.display = 'block';
        _getLessFile(baseColor)
            .then(function(result) {
                deleteStyleSheets();
                var css = result,
                    head = document.head || document.getElementsByTagName('head')[0],
                    style = document.createElement('style');

                style.type = 'text/css';
                if (style.styleSheet) {
                    style.styleSheet.cssText = css;
                } else {
                    style.appendChild(document.createTextNode(css));
                }

                head.appendChild(style);
                overlay.style.display = 'none';
            })
            .catch(function(err) {
                console.error(err);
            });
    }

    return {
        updateScheme: function() {
            _updateScheme();
        },
        generateFavicon: function() {
            _generateFavicon();
        }
    };
})();


// var less_link = document.getElementById('less_link');
// var new_href = less_link.href.split('/').slice(0, 4).join('/') + '/' + seed_color;
// less_link.href = new_href;

// var writeLessFiles = function() {
//     return new Promise(function(resolve, reject) {

//         var less_css = document.createElement('link');
//         less_css.id = 'less_css';
//         less_css.rel = 'stylesheet/less';
//         less_css.type = 'text/css';
//         less_css.href = '/less/index.less' + '?v=' + Date.now();
//         document.head.appendChild(less_css);

//         var less_js = document.createElement('script');
//         less_js.id = 'less_js';
//         less_js.type = 'text/javascript';
//         less_js.src = '/js/dev/less.min.js';
//         less_js.onload = function() {
//             resolve();
//         }
//         document.head.appendChild(less_js);

//     });
// }

// var updateScheme = function() {
//     event.preventDefault();

//     var seed_color = '#' + document.getElementById('seed_color').value;

//     // gotta be a better way to handle this
//     if (!document.getElementById('less_js')) {
//         writeLessFiles().then(function() {
//             less.modifyVars({
//                 '@base-color': seed_color
//             });
//             less.pageLoadFinished.then(function(){
//                 generateFavicon();
//             });
//         });
//     } else {
//         less.modifyVars({
//             '@base-color': seed_color
//         });
//         less.pageLoadFinished.then(function(){
//             generateFavicon();
//         });
//     }

//     return false;
// };



//// IDEA GRAVEYARD
//
//              .--. .-,       .-..-.__
//            .'(`.-` \_.-'-./`  |\_( "\__
//         __.>\ ';  _;---,._|   / __/`'--)
//        /.--.  : |/' _.--.<|  /  | |
//    _..-'    `\     /' /`  /_/ _/_/
//     >_.-``-. `Y  /' _;---.`|/))))
//    '` .-''. \|:  \.'   __, .-'"`
//     .'--._ `-:  \/:  /'  '.\             _|_
//         /.'`\ :;   /'      `-           `-|-`
//        -`    |     |                      |
//              :.; : |                  .-'~^~`-.
//              |:    |                .' _     _ `.
//              |:.   |                | |_) | |_) |
//              :. :  |                | | \ | |   |
//            .jgs. : ;                |           |
//    -."-/\\\/:::.    `\."-._'."-"_\\-|           |///."-
//    " -."-.\\"-."//.-".`-."_\\-.".-\\`=.........=`//-".

// A promise to fetch the contents of index.less and return them
// as a string for manual less.render() compilation

// var getLessFile = function() {
//     return new Promise(function(resolve, reject) {
//         var xhr = new XMLHttpRequest();
//         xhr.open('GET', '/less/index.less');
//         xhr.onload = function() {
//             if (this.status >= 200 && this.status < 300) {
//                 resolve(xhr.response);
//             } else {
//                 reject({
//                     status: this.status,
//                     statusText: xhr.statusText
//                 });
//             }
//         };
//         xhr.onerror = function() {
//             reject({
//                 status: this.status,
//                 statusText: xhr.statusText
//             });
//         };
//         xhr.send();
//     });
// }

// With the above, a function to write compiled css into a <style>
// tag in the head.

// var style_block = document.getElementById('style_block');
// getLessFile()
//     .then(function(result) {
//         var options = {
//             filename: '/less/index.less'
//         };

//         return less.render(result, options);
//     })
//     .then(function(output) {
//         style_block.appendChild(document.createTextNode(output.css));
//         less.modifyVars({'@base-color': '#FF0000'});
//     })
//     .catch(function(err) {
//         console.error(err);
//     });