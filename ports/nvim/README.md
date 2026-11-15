# Verdigris for Neovim

One colorscheme, `verdigris`, for Neovim 0.9 and later. It follows
`background`: light loads Limestone, dark loads Slate.

It covers the editor, legacy syntax groups, treesitter captures, LSP semantic
tokens and diagnostics, and these plugins: gitsigns, telescope, fzf-lua,
snacks, nvim-cmp, blink.cmp, indent-blankline, mini.nvim, neo-tree, nvim-tree,
which-key, lazy, mason, flash, leap, trouble, noice, nvim-notify,
treesitter-context, rainbow-delimiters, render-markdown, nvim-dap and copilot.
A lualine theme is included.

## Install

With lazy.nvim. The colorscheme lives in a subdirectory, so add it to the
runtime path:

```lua
{
  "mr-karan/verdigris",
  lazy = false,
  priority = 1000,
  config = function(plugin)
    vim.opt.rtp:append(plugin.dir .. "/ports/nvim")
    vim.cmd.colorscheme("verdigris")
  end,
}
```

Without a plugin manager:

```sh
mkdir -p ~/.config/nvim/colors ~/.config/nvim/lua/lualine/themes
cp colors/verdigris.lua ~/.config/nvim/colors/
cp lua/lualine/themes/verdigris.lua ~/.config/nvim/lua/lualine/themes/
```

Then in `init.lua`:

```lua
vim.cmd.colorscheme("verdigris")
```

For lualine, set `options = { theme = "verdigris" }`.
