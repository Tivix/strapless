Strapless
=========

Basic setup
---------

Make sure you've got Less (http://lesscss.org/) up and running before starting with Strapless. Basic understanding of Less scope, Less importing and, well, just Less in general is recommended.

Use Strapless as the base of your project by renaming **strapless.less** into **[your project name here].less**. Or **index.less**. Or whatever you want. It's up to you. Strapless is intended as a starting point for your project's CSS/Less.

To add your own CSS rules, simply insert your own Less after the core Strapless library files. You can also edit the Strapless library directly, just remember anything included as a *(reference)* in **strapless.less** doesn't output CSS directly, and editing library files might make it harder to update Strapless in the future. If you find yourself overwriting too many rules for a particular element, you can start from scratch by commenting it out in **strapless.less**.

Strapless is really opinionated in its approach. It's okay if you comment a few things out. We won't be offended.

Everything that's included
---------

Here's what's included:

`settings.less`
Project settings are defined here. Edit them here or redefine them later and let lazy loading do its thing.

`mixins.less`
Strapless has a few mixins for determining text contrast. They're all determined to do the same thing: Make text and background colors work together to achieve target contrast ratios.

- `.contrast-text-against(@background)`
Figures out whether it's more appropriate to shade or tint, then shades or tints.

- `.tint-text-against(@background)`
Adds white until a contrast ratio of 9 is met.

- `.shade-text-against(@background)`
Adds black until a contrast ratio of 4.5 is met.

- `.invert-text-against(@background)`
Uses white text and darkens the background (if needed) to meet a contrast ratio of 4.5.

- `.color-text(@color, @background)`
Darkens given color for text until it meets a contrast ratio of 4.5 against the background.

- `.set-contrast-ratio(@a, @b)`
Sets the contrast ratio between two colors to `@contrast-ratio`. See [the official page](https://www.w3.org/TR/UNDERSTANDING-WCAG20/visual-audio-contrast-contrast.html) for more on that. TL;DR: Strapless mixins all meet the AA-level requirements, and can be tweaked to meet AAA-level too.

- `.set-distance(@a, @b)`
Sets `@distance` to the distance between two colors (the two arguments, both needed) in RGB space.

- `.set-closer-farther(@compare, @c1, @c2)`
Assigns the closer of `@c1` and `@c2` to @closer, and the farther of the two to farther. Both are compared to @compare in RGB space.

- `.set-tone(@color)`
Strapless adds either white or black to meet contrast goals. This mixin decides which is appropriate for a given color and sets it to @tone. Default tone values can be changed to enhance certain color schemes, but doing so may result in unmet contrast goals.

- `.set-average(@colors)`
Averages a list of colors. Works a lot like Less's `average()`, except it takes any number of colors.

- `.colorize(@color)`
Sets the background to @color and picks an appropriate text color.

`colors.less`
Generates all of Strapless's color variables. These are documented in `settings.less` in variable name lists. (Strapless uses variable name lists because variable names sometimes end up as CSS classes.)

`patterns.less`
Contains mixins for generating patterns.

`targets.less`
Ruleset mixins for different targets, including responsiveness targets.

`elements/`
The elements folder contains Less for HTML elements. Each file is named for its element, while `etc.less` is a catch-all for rules too small for their own file.

`utilities.less`
CSS class utilities.