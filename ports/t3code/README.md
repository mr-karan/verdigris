# Verdigris for T3 Code

`verdigris.json` is one theme with a light base (Limestone) and a dark variant
(Slate), so it follows the app's appearance setting. It also sets Inter for
prose and Commit Mono for code, when those fonts are installed.

## Install

```sh
t3 theme set verdigris.json
```

T3 copies the file into `~/.t3/userdata/themes/`. Go back to the default with
`t3 theme set t3-chat`.

## Notes

`build.py` holds the theme CSS and the colours only T3's chrome needs, and
takes every other colour from `palette.json`. It checks the result against
T3's limits: 61 roles per mode, `#rrggbb` colours, CSS of at most 20,000
characters with no remote `url()`, and a file of at most 32 KB.
