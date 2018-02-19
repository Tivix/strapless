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
