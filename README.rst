=========
Dev setup
=========

Node/Express version
---------

From the home directory:

- ``npm install``
- ``node index.js``
- Visit localhost:3000 in your browser

On load, the page will use the static, compiled index.css file in ``public/static/css``. 

On-the-fly scheme changes, either from the colorpicker form or by using a hex value in the url (e.g., ``localhost:3000/CADFE6``), will use the index.less file in ``source/less``. 

---

Strapless is a color-changing CSS boilerplate for HTML elements, and a powerful LessCSS library for colors and patterns.