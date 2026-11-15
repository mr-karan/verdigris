# Verdigris for Ghostty

`verdigris-limestone` (light) and `verdigris-slate` (dark).

## Install

```sh
mkdir -p ~/.config/ghostty/themes
cp verdigris-limestone verdigris-slate ~/.config/ghostty/themes/
```

Then in `~/.config/ghostty/config`, follow the system appearance:

```
theme = light:verdigris-limestone,dark:verdigris-slate
```

Or pin one flavour with `theme = verdigris-slate`. Reload the config to apply.

## Optional

Ghostty 1.3 and later can colour search matches. These lines are not in the
theme files, so older versions load them without an error. Add them to your
config and swap the values for the flavour you use (Slate shown):

```
search-background = #523a24
search-foreground = #dde3df
search-selected-background = #d9a377
search-selected-foreground = #151a19
```
