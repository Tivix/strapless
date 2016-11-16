var Strapless = (function() {

    function _generateFavicon() {
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
    }

    function _getLessFile(baseColor) {
        return new Promise(function(resolve, reject) {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/less/' + baseColor);
            xhr.onload = function() {
                if (this.status >= 200 && this.status < 300) {
                    var response = {
                        'baseColor': baseColor,
                        'styles': xhr.response
                    };
                    resolve(response);
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
            if (sheet.title === unique_title) {
                return sheet;
            }
        }
    }

    function deleteStyleSheets() {
        for (var i = 0; i < document.styleSheets.length; i++) {
            document.head.removeChild(document.styleSheets[i].ownerNode);
        }
    }

    function setOverlayColor(overlay, baseColor) {
        overlay.getElementsByTagName("circle")[0].setAttribute('stroke', '#' + baseColor);
    }

    function _getCSSFile() {
        var baseColor = document.getElementById('seed_color').value;
        var validHex = /^(?:[0-9a-f]{3}){1,2}$/i.test(baseColor);
        if (validHex) {
            location.href='/download/' + baseColor;
        } else {
            window.alert('Invalid hex color value entered.');
        }
    }

    function _updateScheme() {
        var baseColor = document.getElementById('seed_color').value;
        var styleBlock = document.getElementById('style_block');
        var validHex = /^(?:[0-9a-f]{3}){1,2}$/i.test(baseColor);
        if (validHex) {
            var overlay = document.getElementById('loading_overlay');
            setOverlayColor(overlay, baseColor);
            overlay.style.display = 'block';
            _getLessFile(baseColor)
                .then(function(response) {
                    deleteStyleSheets();
                    var css = response.styles,
                        head = document.head || document.getElementsByTagName('head')[0],
                        style = document.createElement('style');

                    style.type = 'text/css';
                    if (style.styleSheet) {
                        style.styleSheet.cssText = css;
                    } else {
                        style.appendChild(document.createTextNode(css));
                    }
                    history.pushState({
                        'baseColor': response.baseColor
                    }, '', '/' + baseColor);
                    head.appendChild(style);
                    overlay.style.display = 'none';
                    _generateFavicon();
                })
                .catch(function(err) {
                    console.error(err);
                });
        } else {
            window.alert('Invalid hex color value entered.');
        }
    }

    return {
        updateScheme: function() {
            _updateScheme();
        },
        downloadCSS: function() {
            _getCSSFile();
        },
        generateFavicon: function() {
            _generateFavicon();
        }
    };
})();