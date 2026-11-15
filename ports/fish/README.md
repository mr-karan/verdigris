# Verdigris for fish

`verdigris.theme` colours the command line: commands, arguments, strings,
errors, autosuggestions and the completion pager. It holds both flavours, and
fish picks Limestone or Slate to match the terminal background. Tested
with fish 4.9; older versions without `[light]` and `[dark]` theme sections
cannot read it.

## Install

```fish
mkdir -p ~/.config/fish/themes
cp verdigris.theme ~/.config/fish/themes/
fish_config theme choose verdigris
```
