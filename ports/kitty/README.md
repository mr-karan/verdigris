# Verdigris for kitty

`verdigris-limestone.conf` (light) and `verdigris-slate.conf` (dark).

## Install

Follow the system appearance (kitty 0.38 and later):

```sh
cp verdigris-limestone.conf ~/.config/kitty/light-theme.auto.conf
cp verdigris-slate.conf ~/.config/kitty/dark-theme.auto.conf
```

Or pin one flavour:

```sh
mkdir -p ~/.config/kitty/themes
cp verdigris-*.conf ~/.config/kitty/themes/
echo "include themes/verdigris-slate.conf" >> ~/.config/kitty/kitty.conf
```

Files in `~/.config/kitty/themes/` also show up in `kitten themes` as
"Verdigris Limestone" and "Verdigris Slate".
