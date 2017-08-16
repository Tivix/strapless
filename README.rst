# Strapless

## Basic setup
---------

Make sure you've got [Less](http://lesscss.org/) up and running before starting with Strapless.

Use Strapless as the base of your project by renaming **strapless.less** into **[your project name here].less**. Or **index.less**. Or whatever you want. It's up to you. Strapless is intended as a starting point for your project's CSS/Less.

To add your own CSS rules, simply insert your own Less after the core Strapless library files. You can also edit the Strapless library directly, just remember anything included as a _(reference)_ in **strapless.less** doesn't output CSS directly, and editing library files might make it harder to update Strapless in the future. If you find yourself overwriting too many rules for a particular element, you can start from scratch by commenting it out in **strapless.less**.

### settings.less

Project settings are defined here. Edit them here or redefine them later and let lazy loading do its thing.

### mixins.less

Strapless has a few mixins for determining text contrast. They're all determined to do the same thing: Make text and background colors work together to achieve target contrast ratios.

### .contrast-text-against(@background)

Figures out whether it's more appropriate to shade or tint, then shades or tints.

### .tint-text-against(@background)

Adds white until a contrast ratio of 9 is met.

### .shade-text-against(@background)

Adds black until a contrast ratio of 4.5 is met.

### .invert-text-against(@background)

Uses white text and darkens the background (if needed) to meet a contrast ratio of 4.5.

### .color-text(@color, @background)

Darkens given color for text until it meets a contrast ratio of 4.5 against the background.

Strapless also has a few mixins for determining values and setting them to variables. This breaks lazy loading, meaning the variables set aren't available to the interpreter before they're set. Feel free to view this as a restriction or an advantage.

### .set-contrast-ratio(@a, @b)

Sets the contrast ratio between two colors to `@contrast-ratio`. See [the official page](https://www.w3.org/TR/UNDERSTANDING-WCAG20/visual-audio-contrast-contrast.html) for more on that. TL;DR: Strapless mixins all meet the AA-level requirements, and can be tweaked to meet AAA-level too.

### .set-distance(@a, @b)

Sets @distance to the distance between two colors (the two arguments, both needed) in RGB space.

### .set-closer-farther(@compare, @c1, @c2)

Assigns the closer of c1 and c2 to @closer, and the farther of the two to farther. Both are compared to @compare in RGB space.

### .set-tone(@color)

Strapless adds either white or black to meet contrast goals. This mixin decides which is appropriate for a given color. Default tone values can be changed to enhance certain color schemes, but doing so may result in unmet contrast goals.











=========
Dev setup
=========

Node/Express version
---------

From the home directory:

- ``npm install``
- ``node server.js``
- Visit localhost:3000 in your browser

On load, the page will use the static, compiled index.css file in ``public/static/css``. 

On-the-fly scheme changes, either from the colorpicker form or by using a hex value in the url (e.g., ``localhost:3000/CADFE6``), will use the index.less file in ``source/less``. 

---

Strapless is a color-changing CSS boilerplate for HTML elements, and a powerful LessCSS library for colors and patterns.