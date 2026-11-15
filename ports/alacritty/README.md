# Verdigris for Alacritty

`verdigris-limestone.toml` (light) and `verdigris-slate.toml` (dark), for
Alacritty 0.13 and later.

## Install

```sh
mkdir -p ~/.config/alacritty/themes
cp verdigris-*.toml ~/.config/alacritty/themes/
```

Then import one flavour in `~/.config/alacritty/alacritty.toml`:

```toml
[general]
import = ["~/.config/alacritty/themes/verdigris-slate.toml"]
```

On Alacritty 0.13, `import` is a top-level key and not under `[general]`.
