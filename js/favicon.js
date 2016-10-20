(function() {
    var canvas = document.createElement('canvas'),
        ctx,
        link = document.getElementById('favicon'),
        colorbox = document.getElementById('get_color1');

    if (canvas.getContext) {
        canvas.height = canvas.width = 16;
        ctx = canvas.getContext('2d');
        var fillcolor = window.getComputedStyle(colorbox).color;
        ctx.fillStyle = fillcolor;
        ctx.fillRect(0, 0, 16, 16);

        link.href = canvas.toDataURL('image/png');
    }
})();