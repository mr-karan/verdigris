# Verdigris for bat, delta and Sublime Text

`verdigris-limestone.tmTheme` (light) and `verdigris-slate.tmTheme` (dark),
plus `verdigris.gitconfig` with matching delta styles.

## bat

```sh
mkdir -p "$(bat --config-dir)/themes"
cp verdigris-*.tmTheme "$(bat --config-dir)/themes/"
bat cache --build
```

Then follow the terminal's appearance (bat 0.25 and later):

```sh
export BAT_THEME_LIGHT=verdigris-limestone
export BAT_THEME_DARK=verdigris-slate
```

Or pin one flavour with `export BAT_THEME=verdigris-slate`.

## delta

Install the bat themes first: delta reads them from bat's cache. Then in
`~/.gitconfig`:

```ini
[include]
	path = /path/to/verdigris/ports/bat/verdigris.gitconfig
[delta]
	features = verdigris-slate
```

## Sublime Text

Copy the `.tmTheme` files into `Packages/User`, then pick one with
**UI: Select Color Scheme**.
