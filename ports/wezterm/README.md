# Verdigris for WezTerm

`verdigris-limestone.toml` (light) and `verdigris-slate.toml` (dark).

## Install

```sh
mkdir -p ~/.config/wezterm/colors
cp verdigris-*.toml ~/.config/wezterm/colors/
```

Then in `~/.config/wezterm/wezterm.lua`, follow the system appearance:

```lua
local wezterm = require "wezterm"
local config = wezterm.config_builder()

local function scheme()
  if wezterm.gui and wezterm.gui.get_appearance():find "Dark" then
    return "Verdigris Slate"
  end
  return "Verdigris Limestone"
end

config.color_scheme = scheme()
return config
```

Or pin one flavour with `config.color_scheme = "Verdigris Slate"`.
