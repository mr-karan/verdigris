"""Neovim colorscheme (0.9 and later) and a lualine theme.

Highlight groups name palette colours, so one Lua table serves both
flavours: the colorscheme picks the palette from 'background' at load.
"""

from palette import ANSI, mix

FLAGS = ("bold", "italic", "underline", "undercurl", "strikethrough", "reverse", "nocombine")


def groups(syntax: dict) -> list:
    """(section, {group: spec}). A spec names palette colours or links a group."""

    def role(name: str, **extra) -> dict:
        spec = syntax[name]
        return {"fg": spec["color"], **{flag: True for flag in spec.get("style", "").split()}, **extra}

    def link(group: str) -> dict:
        return {"link": group}

    def diagnostic(kind: str, color: str) -> dict:
        return {
            f"Diagnostic{kind}": {"fg": color},
            f"DiagnosticVirtualText{kind}": {"fg": color, "bg": f"{color}_wash"},
            f"DiagnosticUnderline{kind}": {"sp": color, "undercurl": True},
            f"DiagnosticFloating{kind}": link(f"Diagnostic{kind}"),
            f"DiagnosticSign{kind}": link(f"Diagnostic{kind}"),
        }

    kinds = {
        "Function": "azurite", "Method": "azurite", "Constructor": "azurite",
        "Class": "brass", "Struct": "brass", "Interface": "brass", "Enum": "brass",
        "TypeParameter": "brass", "Keyword": "patina", "Operator": "fg_muted",
        "Variable": "fg", "Field": "fg", "Property": "fg", "Constant": "copper",
        "EnumMember": "copper", "Value": "copper", "Unit": "copper", "Snippet": "bornite",
        "Text": "fg_muted", "Module": "fg_muted", "File": "azurite", "Folder": "azurite",
        "Reference": "azurite", "Color": "copper", "Event": "bornite",
    }
    modes = {"Normal": "patina", "Insert": "malachite", "Visual": "bornite",
             "Replace": "cuprite", "Command": "copper", "Other": "azurite"}

    editor = {
        "Normal": {"fg": "fg", "bg": "bg"},
        "NormalNC": {"fg": "fg", "bg": "bg"},
        "NormalFloat": {"fg": "fg", "bg": "bg_raised"},
        "FloatBorder": {"fg": "line_strong", "bg": "bg_raised"},
        "FloatTitle": {"fg": "fg_strong", "bg": "bg_raised", "bold": True},
        "FloatFooter": {"fg": "fg_muted", "bg": "bg_raised"},
        "ColorColumn": {"bg": "fill_soft"},
        "Conceal": {"fg": "fg_subtle"},
        "Cursor": {"fg": "bg", "bg": "patina"},
        "lCursor": link("Cursor"),
        "CursorIM": link("Cursor"),
        "TermCursor": link("Cursor"),
        "CursorLine": {"bg": "fill_soft"},
        "CursorColumn": {"bg": "fill_soft"},
        "CursorLineNr": {"fg": "fg", "bold": True},
        "LineNr": {"fg": "fg_subtle"},
        "SignColumn": {"fg": "fg_subtle", "bg": "bg"},
        "FoldColumn": {"fg": "fg_subtle", "bg": "bg"},
        "Folded": {"fg": "fg_muted", "bg": "fill_soft"},
        "Directory": {"fg": "azurite"},
        "EndOfBuffer": {"fg": "fg_faint"},
        "ErrorMsg": {"fg": "cuprite"},
        "WarningMsg": {"fg": "copper"},
        "ModeMsg": {"fg": "fg_muted"},
        "MoreMsg": {"fg": "patina"},
        "Question": {"fg": "patina"},
        "MsgSeparator": {"fg": "line", "bg": "bg"},
        "IncSearch": {"fg": "bg", "bg": "copper"},
        "CurSearch": {"fg": "bg", "bg": "copper"},
        "Search": {"fg": "fg_strong", "bg": "search"},
        "Substitute": {"fg": "bg", "bg": "cuprite"},
        "MatchParen": {"bg": "selection", "bold": True},
        "NonText": {"fg": "fg_faint"},
        "SpecialKey": {"fg": "fg_faint"},
        "Whitespace": {"fg": "fg_faint"},
        "Pmenu": {"fg": "fg", "bg": "bg_raised"},
        "PmenuSel": {"fg": "fg_strong", "bg": "fill"},
        "PmenuKind": {"fg": "fg_muted", "bg": "bg_raised"},
        "PmenuKindSel": {"fg": "fg_muted", "bg": "fill"},
        "PmenuExtra": {"fg": "fg_subtle", "bg": "bg_raised"},
        "PmenuExtraSel": {"fg": "fg_subtle", "bg": "fill"},
        "PmenuSbar": {"bg": "fill"},
        "PmenuThumb": {"bg": "line_strong"},
        "PmenuMatch": {"fg": "patina", "bold": True},
        "PmenuMatchSel": {"fg": "patina", "bg": "fill", "bold": True},
        "StatusLine": {"fg": "fg", "bg": "bg_dim"},
        "StatusLineNC": {"fg": "fg_subtle", "bg": "bg_dim"},
        "TabLine": {"fg": "fg_subtle", "bg": "bg_dim"},
        "TabLineFill": {"bg": "bg_dim"},
        "TabLineSel": {"fg": "fg_strong", "bg": "bg", "bold": True},
        "WinBar": {"fg": "fg_muted", "bg": "bg"},
        "WinBarNC": {"fg": "fg_subtle", "bg": "bg"},
        "WinSeparator": {"fg": "line"},
        "VertSplit": link("WinSeparator"),
        "Title": {"fg": "patina", "bold": True},
        "Visual": {"bg": "selection"},
        "VisualNOS": {"bg": "fill"},
        "WildMenu": {"fg": "fg_strong", "bg": "fill"},
        "QuickFixLine": {"bg": "fill", "bold": True},
        "SpellBad": {"sp": "cuprite", "undercurl": True},
        "SpellCap": {"sp": "copper", "undercurl": True},
        "SpellLocal": {"sp": "azurite", "undercurl": True},
        "SpellRare": {"sp": "bornite", "undercurl": True},
        "DiffAdd": {"bg": "malachite_wash"},
        "DiffChange": {"bg": "azurite_wash"},
        "DiffDelete": {"fg": "cuprite", "bg": "cuprite_wash"},
        "DiffText": {"bg": "azurite_emphasis"},
        "Added": {"fg": "malachite"},
        "Changed": {"fg": "azurite"},
        "Removed": {"fg": "cuprite"},
        "diffAdded": link("Added"),
        "diffChanged": link("Changed"),
        "diffRemoved": link("Removed"),
        "diffFile": {"fg": "fg_strong", "bold": True},
        "diffLine": {"fg": "bornite"},
        "diffIndexLine": {"fg": "fg_muted"},
    }
    legacy = {
        "Comment": role("comment"),
        "Constant": role("constant"),
        "String": role("string"),
        "Character": role("string"),
        "Number": role("number"),
        "Float": role("number"),
        "Boolean": role("constant"),
        "Identifier": role("variable"),
        "Function": role("function"),
        "Statement": role("keyword"),
        "Conditional": role("keyword"),
        "Repeat": role("keyword"),
        "Label": role("label"),
        "Operator": role("operator"),
        "Keyword": role("keyword"),
        "Exception": role("keyword"),
        "PreProc": role("decorator"),
        "Include": role("keyword"),
        "Define": role("decorator"),
        "Macro": role("decorator"),
        "PreCondit": role("decorator"),
        "Type": role("type"),
        "StorageClass": role("keyword"),
        "Structure": role("keyword"),
        "Typedef": role("type"),
        "Special": role("escape"),
        "SpecialChar": role("escape"),
        "Tag": role("tag"),
        "Delimiter": role("punctuation"),
        "SpecialComment": {"fg": "fg_muted", "italic": True},
        "Debug": {"fg": "copper"},
        "Underlined": role("link"),
        "Ignore": {"fg": "fg_faint"},
        "Error": {"fg": "cuprite"},
        "Todo": {"fg": "copper", "bold": True},
    }
    treesitter = {
        "@variable": role("variable"),
        "@variable.builtin": role("builtin"),
        "@variable.parameter": role("parameter"),
        "@variable.member": role("property"),
        "@constant": role("constant"),
        "@constant.builtin": role("constant"),
        "@constant.macro": role("decorator"),
        "@module": role("namespace"),
        "@module.builtin": role("namespace"),
        "@label": role("label"),
        "@string": role("string"),
        "@string.documentation": role("string"),
        "@string.regexp": role("regex"),
        "@string.escape": role("escape"),
        "@string.special": role("escape"),
        "@string.special.symbol": role("constant"),
        "@string.special.url": role("link"),
        "@string.special.path": role("string"),
        "@character": role("string"),
        "@character.special": role("escape"),
        "@boolean": role("constant"),
        "@number": role("number"),
        "@number.float": role("number"),
        "@type": role("type"),
        "@type.builtin": role("type"),
        "@type.definition": role("type"),
        "@attribute": role("decorator"),
        "@attribute.builtin": role("decorator"),
        "@property": role("property"),
        "@property.json": role("key"),
        "@property.jsonc": role("key"),
        "@property.yaml": role("key"),
        "@property.toml": role("key"),
        "@function": role("function"),
        "@function.builtin": role("function"),
        "@function.call": role("function"),
        "@function.macro": role("decorator"),
        "@function.method": role("function"),
        "@function.method.call": role("function"),
        "@constructor": role("type"),
        "@operator": role("operator"),
        "@keyword": role("keyword"),
        "@keyword.coroutine": role("keyword"),
        "@keyword.function": role("keyword"),
        "@keyword.operator": role("keyword"),
        "@keyword.import": role("keyword"),
        "@keyword.type": role("keyword"),
        "@keyword.modifier": role("keyword"),
        "@keyword.repeat": role("keyword"),
        "@keyword.return": role("keyword"),
        "@keyword.debug": role("keyword"),
        "@keyword.exception": role("keyword"),
        "@keyword.conditional": role("keyword"),
        "@keyword.conditional.ternary": role("operator"),
        "@keyword.directive": role("decorator"),
        "@keyword.directive.define": role("decorator"),
        "@punctuation.delimiter": role("punctuation"),
        "@punctuation.bracket": role("punctuation"),
        "@punctuation.special": role("escape"),
        "@comment": role("comment"),
        "@comment.documentation": role("comment"),
        "@comment.error": {"fg": "cuprite", "bold": True},
        "@comment.warning": {"fg": "copper", "bold": True},
        "@comment.todo": {"fg": "patina", "bold": True},
        "@comment.note": {"fg": "azurite", "bold": True},
        "@markup.strong": {"fg": "fg_strong", "bold": True},
        "@markup.italic": {"italic": True},
        "@markup.strikethrough": {"strikethrough": True},
        "@markup.underline": {"underline": True},
        "@markup.heading": role("heading"),
        "@markup.quote": {"fg": "fg_muted", "italic": True},
        "@markup.math": {"fg": "copper"},
        "@markup.link": role("link"),
        "@markup.link.label": {"fg": "azurite"},
        "@markup.link.url": role("link"),
        "@markup.raw": role("string"),
        "@markup.raw.block": {"fg": "fg"},
        "@markup.list": {"fg": "patina"},
        "@markup.list.checked": {"fg": "malachite"},
        "@markup.list.unchecked": {"fg": "fg_subtle"},
        "@diff.plus": link("Added"),
        "@diff.minus": link("Removed"),
        "@diff.delta": link("Changed"),
        "@tag": role("tag"),
        "@tag.builtin": role("tag"),
        "@tag.attribute": role("attribute"),
        "@tag.delimiter": role("punctuation"),
    }
    lsp = {
        "@lsp.type.class": role("type"),
        "@lsp.type.struct": role("type"),
        "@lsp.type.enum": role("type"),
        "@lsp.type.interface": role("type"),
        "@lsp.type.type": role("type"),
        "@lsp.type.typeParameter": role("type"),
        "@lsp.type.builtinType": role("type"),
        "@lsp.type.enumMember": role("constant"),
        "@lsp.type.function": role("function"),
        "@lsp.type.method": role("function"),
        "@lsp.type.macro": role("decorator"),
        "@lsp.type.decorator": role("decorator"),
        "@lsp.type.namespace": role("namespace"),
        "@lsp.type.parameter": role("parameter"),
        "@lsp.type.property": role("property"),
        "@lsp.type.keyword": role("keyword"),
        "@lsp.type.selfKeyword": role("builtin"),
        "@lsp.type.lifetime": role("label"),
        "@lsp.type.escapeSequence": role("escape"),
        "@lsp.type.formatSpecifier": role("escape"),
        # Treesitter is more precise for these, so the LSP token stays out of the way.
        "@lsp.type.variable": {},
        "@lsp.type.comment": {},
        "@lsp.type.string": {},
        "@lsp.type.number": {},
        "@lsp.type.operator": {},
        "@lsp.mod.deprecated": {"strikethrough": True},
        "@lsp.typemod.function.defaultLibrary": role("function"),
        "@lsp.typemod.variable.defaultLibrary": role("builtin"),
        **diagnostic("Error", "cuprite"),
        **diagnostic("Warn", "copper"),
        **diagnostic("Info", "azurite"),
        **diagnostic("Hint", "patina"),
        **diagnostic("Ok", "malachite"),
        "DiagnosticUnnecessary": {"fg": "fg_subtle"},
        "DiagnosticDeprecated": {"sp": "fg_subtle", "strikethrough": True},
        "LspReferenceText": {"bg": "fill"},
        "LspReferenceRead": {"bg": "fill"},
        "LspReferenceWrite": {"bg": "patina_wash"},
        "LspSignatureActiveParameter": {"fg": "copper", "bold": True},
        "LspInlayHint": {"fg": "fg_subtle", "bg": "fill_soft"},
        "LspCodeLens": {"fg": "fg_subtle"},
        "LspCodeLensSeparator": {"fg": "fg_faint"},
        "LspInfoBorder": link("FloatBorder"),
    }
    plugins = {
        # gitsigns.nvim, mini.diff
        "GitSignsAdd": {"fg": "malachite"},
        "GitSignsChange": {"fg": "azurite"},
        "GitSignsDelete": {"fg": "cuprite"},
        "GitSignsCurrentLineBlame": {"fg": "fg_subtle", "italic": True},
        "MiniDiffSignAdd": link("GitSignsAdd"),
        "MiniDiffSignChange": link("GitSignsChange"),
        "MiniDiffSignDelete": link("GitSignsDelete"),
        # telescope.nvim, fzf-lua, snacks.nvim, mini.pick
        "TelescopeNormal": link("NormalFloat"),
        "TelescopeBorder": link("FloatBorder"),
        "TelescopeTitle": {"fg": "patina", "bold": True},
        "TelescopeSelection": {"fg": "fg_strong", "bg": "fill"},
        "TelescopeSelectionCaret": {"fg": "copper", "bg": "fill"},
        "TelescopeMatching": {"fg": "patina", "bold": True},
        "TelescopePromptPrefix": {"fg": "patina"},
        "FzfLuaNormal": link("NormalFloat"),
        "FzfLuaBorder": link("FloatBorder"),
        "FzfLuaTitle": {"fg": "patina", "bold": True},
        "SnacksPickerMatch": {"fg": "patina", "bold": True},
        "SnacksPickerDir": {"fg": "fg_subtle"},
        "SnacksIndent": {"fg": "line"},
        "SnacksIndentScope": {"fg": "line_strong"},
        "MiniPickMatchCurrent": {"bg": "fill"},
        "MiniPickMatchRanges": {"fg": "patina", "bold": True},
        # nvim-cmp, blink.cmp
        "CmpItemAbbr": {"fg": "fg"},
        "CmpItemAbbrDeprecated": {"fg": "fg_subtle", "strikethrough": True},
        "CmpItemAbbrMatch": {"fg": "patina", "bold": True},
        "CmpItemAbbrMatchFuzzy": {"fg": "patina"},
        "CmpItemMenu": {"fg": "fg_subtle"},
        "CmpItemKind": {"fg": "fg_muted"},
        **{f"CmpItemKind{kind}": {"fg": color} for kind, color in kinds.items()},
        "BlinkCmpMenu": link("Pmenu"),
        "BlinkCmpMenuBorder": link("FloatBorder"),
        "BlinkCmpMenuSelection": link("PmenuSel"),
        "BlinkCmpLabel": {"fg": "fg"},
        "BlinkCmpLabelMatch": {"fg": "patina", "bold": True},
        "BlinkCmpLabelDeprecated": {"fg": "fg_subtle", "strikethrough": True},
        "BlinkCmpLabelDetail": {"fg": "fg_subtle"},
        "BlinkCmpLabelDescription": {"fg": "fg_subtle"},
        "BlinkCmpGhostText": {"fg": "fg_subtle"},
        "BlinkCmpDoc": link("NormalFloat"),
        "BlinkCmpDocBorder": link("FloatBorder"),
        "BlinkCmpKind": {"fg": "fg_muted"},
        **{f"BlinkCmpKind{kind}": {"fg": color} for kind, color in kinds.items()},
        # indent-blankline.nvim, mini.indentscope
        "IblIndent": {"fg": "line"},
        "IblScope": {"fg": "line_strong"},
        "IblWhitespace": {"fg": "line"},
        "MiniIndentscopeSymbol": {"fg": "line_strong"},
        # mini.statusline, mini.tabline, other mini modules
        **{f"MiniStatuslineMode{mode}": {"fg": "bg", "bg": color, "bold": True} for mode, color in modes.items()},
        "MiniStatuslineDevinfo": {"fg": "fg", "bg": "fill"},
        "MiniStatuslineFilename": {"fg": "fg_muted", "bg": "bg_dim"},
        "MiniStatuslineFileinfo": {"fg": "fg", "bg": "fill"},
        "MiniStatuslineInactive": {"fg": "fg_subtle", "bg": "bg_dim"},
        "MiniTablineCurrent": {"fg": "fg_strong", "bg": "bg", "bold": True},
        "MiniTablineVisible": {"fg": "fg", "bg": "bg_dim"},
        "MiniTablineHidden": {"fg": "fg_subtle", "bg": "bg_dim"},
        "MiniTablineModifiedCurrent": {"fg": "copper", "bg": "bg", "bold": True},
        "MiniTablineModifiedVisible": {"fg": "copper", "bg": "bg_dim"},
        "MiniTablineModifiedHidden": {"fg": "copper", "bg": "bg_dim"},
        "MiniTablineFill": {"bg": "bg_dim"},
        "MiniCursorword": {"bg": "fill"},
        "MiniJump": {"fg": "bg", "bg": "copper"},
        # neo-tree.nvim, nvim-tree.lua
        "NeoTreeNormal": {"fg": "fg", "bg": "bg_dim"},
        "NeoTreeNormalNC": {"fg": "fg", "bg": "bg_dim"},
        "NeoTreeWinSeparator": {"fg": "line", "bg": "bg_dim"},
        "NeoTreeCursorLine": {"bg": "fill"},
        "NeoTreeRootName": {"fg": "fg_muted", "bold": True},
        "NeoTreeDirectoryName": {"fg": "fg"},
        "NeoTreeDirectoryIcon": {"fg": "fg_muted"},
        "NeoTreeIndentMarker": {"fg": "line_strong"},
        "NeoTreeGitAdded": {"fg": "malachite"},
        "NeoTreeGitUntracked": {"fg": "malachite"},
        "NeoTreeGitModified": {"fg": "azurite"},
        "NeoTreeGitDeleted": {"fg": "cuprite"},
        "NeoTreeGitConflict": {"fg": "bornite"},
        "NeoTreeGitIgnored": {"fg": "fg_subtle"},
        "NvimTreeNormal": {"fg": "fg", "bg": "bg_dim"},
        "NvimTreeWinSeparator": {"fg": "line", "bg": "bg_dim"},
        "NvimTreeRootFolder": {"fg": "fg_muted", "bold": True},
        "NvimTreeFolderName": {"fg": "fg"},
        "NvimTreeOpenedFolderName": {"fg": "fg_strong"},
        "NvimTreeIndentMarker": {"fg": "line_strong"},
        "NvimTreeSpecialFile": {"fg": "copper"},
        "NvimTreeExecFile": {"fg": "malachite"},
        "NvimTreeGitNew": {"fg": "malachite"},
        "NvimTreeGitDirty": {"fg": "azurite"},
        "NvimTreeGitDeleted": {"fg": "cuprite"},
        # which-key.nvim
        "WhichKey": {"fg": "patina"},
        "WhichKeyGroup": {"fg": "azurite"},
        "WhichKeyDesc": {"fg": "fg"},
        "WhichKeySeparator": {"fg": "fg_subtle"},
        "WhichKeyValue": {"fg": "fg_subtle"},
        "WhichKeyNormal": link("NormalFloat"),
        "WhichKeyBorder": link("FloatBorder"),
        # lazy.nvim, mason.nvim
        "LazyH1": {"fg": "bg", "bg": "patina", "bold": True},
        "LazyButton": {"fg": "fg", "bg": "fill"},
        "LazyButtonActive": {"fg": "bg", "bg": "patina"},
        "LazySpecial": {"fg": "patina"},
        "LazyProgressDone": {"fg": "patina"},
        "LazyProgressTodo": {"fg": "line_strong"},
        "LazyComment": {"fg": "fg_subtle"},
        "LazyDimmed": {"fg": "fg_subtle"},
        "MasonHeader": {"fg": "bg", "bg": "patina", "bold": True},
        "MasonHighlight": {"fg": "patina"},
        "MasonHighlightBlock": {"fg": "bg", "bg": "patina"},
        "MasonHighlightBlockBold": {"fg": "bg", "bg": "patina", "bold": True},
        "MasonMuted": {"fg": "fg_subtle"},
        "MasonMutedBlock": {"fg": "fg", "bg": "fill"},
        # flash.nvim, leap.nvim
        "FlashLabel": {"fg": "bg", "bg": "copper", "bold": True},
        "FlashMatch": {"fg": "fg_strong", "bg": "search"},
        "FlashCurrent": {"fg": "bg", "bg": "patina"},
        "FlashBackdrop": {"fg": "fg_subtle"},
        "LeapLabel": {"fg": "bg", "bg": "copper", "bold": True},
        "LeapBackdrop": {"fg": "fg_subtle"},
        # trouble.nvim, noice.nvim, nvim-notify
        "TroubleNormal": {"fg": "fg", "bg": "bg_dim"},
        "TroubleCount": {"fg": "copper"},
        "TroubleIndent": {"fg": "line_strong"},
        "NoiceCmdlinePopupBorder": link("FloatBorder"),
        "NoiceCmdlinePopupTitle": {"fg": "patina", "bold": True},
        "NoiceCmdlineIcon": {"fg": "patina"},
        **{f"Notify{level}{part}": {"fg": color}
           for level, color in (("ERROR", "cuprite"), ("WARN", "copper"), ("INFO", "azurite"),
                                ("DEBUG", "fg_subtle"), ("TRACE", "bornite"))
           for part in ("Border", "Icon", "Title")},
        # nvim-treesitter-context, rainbow-delimiters.nvim, render-markdown.nvim
        "TreesitterContext": {"bg": "bg_dim"},
        "TreesitterContextLineNumber": {"fg": "fg_subtle", "bg": "bg_dim"},
        "TreesitterContextBottom": {"sp": "line", "underline": True},
        "RainbowDelimiterCyan": {"fg": "patina"},
        "RainbowDelimiterOrange": {"fg": "copper"},
        "RainbowDelimiterBlue": {"fg": "azurite"},
        "RainbowDelimiterYellow": {"fg": "brass"},
        "RainbowDelimiterViolet": {"fg": "bornite"},
        "RainbowDelimiterGreen": {"fg": "malachite"},
        "RainbowDelimiterRed": {"fg": "cuprite"},
        "RenderMarkdownCode": {"bg": "bg_dim"},
        "RenderMarkdownCodeInline": {"bg": "fill"},
        # nvim-dap, copilot
        "DapBreakpoint": {"fg": "cuprite"},
        "DapLogPoint": {"fg": "azurite"},
        "DapStopped": {"fg": "malachite"},
        "CopilotSuggestion": {"fg": "fg_subtle", "italic": True},
        "CopilotAnnotation": {"fg": "fg_subtle"},
    }
    return [
        ("Editor", editor), ("Syntax", legacy), ("Treesitter", treesitter),
        ("LSP and diagnostics", lsp), ("Plugins", plugins),
    ]


def lua_key(name: str) -> str:
    return name if name.isidentifier() else f'["{name}"]'


def lua_spec(spec: dict, colors: set) -> str:
    parts = []
    for key, value in spec.items():
        if key in ("fg", "bg", "sp"):
            assert value in colors, f"unknown colour '{value}'"
            parts.append(f"{key} = c.{value}")
        elif key == "link":
            parts.append(f'link = "{value}"')
        else:
            assert key in FLAGS and value is True, f"unknown highlight attribute '{key}'"
            parts.append(f"{key} = true")
    return "{ " + ", ".join(parts) + " }" if parts else "{}"


def palette_lua(palette) -> str:
    lines = ["local palettes = {"]
    for flavour in (palette.light, palette.dark):
        colors = dict(flavour.colors)
        colors["azurite_emphasis"] = mix(flavour["azurite_wash"], flavour["azurite"], 0.22)
        lines.append(f"  {flavour.appearance} = {{")
        lines += [f'    {name} = "{value}",' for name, value in colors.items()]
        lines.append("  },")
    lines.append("}")
    return "\n".join(lines)


def header(palette, what: str) -> str:
    return f"-- {palette.name} {what}. Generated from palette.json: edit that, then run build.py.\n-- {palette.homepage}\n"


def colorscheme(palette) -> str:
    colors = set(palette.light.colors) | {"azurite_emphasis"}
    body = []
    for section, table in groups(palette.roles["syntax"]):
        body.append(f"  -- {section}")
        body += [f"  {lua_key(name)} = {lua_spec(spec, colors)}," for name, spec in table.items()]
    terminal = [
        f"vim.g.terminal_color_{index} = c.{palette.roles['ansi'][name]}" for index, name in enumerate(ANSI)
    ]
    return "\n".join([
        header(palette, "for Neovim"),
        palette_lua(palette),
        "",
        'if vim.g.colors_name then',
        '  vim.cmd("highlight clear")',
        "end",
        'vim.g.colors_name = "verdigris"',
        "",
        'local c = palettes[vim.o.background == "light" and "light" or "dark"]',
        "",
        "local groups = {",
        *body,
        "}",
        "",
        "for name, spec in pairs(groups) do",
        "  vim.api.nvim_set_hl(0, name, spec)",
        "end",
        "",
        *terminal,
        "",
    ])


def lualine(palette) -> str:
    return "\n".join([
        header(palette, "for lualine.nvim"),
        palette_lua(palette),
        "",
        'local c = palettes[vim.o.background == "light" and "light" or "dark"]',
        "",
        "local function mode(color)",
        '  return { a = { fg = c.bg, bg = color, gui = "bold" } }',
        "end",
        "",
        "return {",
        "  normal = {",
        '    a = { fg = c.bg, bg = c.patina, gui = "bold" },',
        "    b = { fg = c.fg, bg = c.fill },",
        "    c = { fg = c.fg_muted, bg = c.bg_dim },",
        "  },",
        "  insert = mode(c.malachite),",
        "  visual = mode(c.bornite),",
        "  replace = mode(c.cuprite),",
        "  command = mode(c.copper),",
        "  terminal = mode(c.azurite),",
        "  inactive = {",
        "    a = { fg = c.fg_subtle, bg = c.bg_dim },",
        "    b = { fg = c.fg_subtle, bg = c.bg_dim },",
        "    c = { fg = c.fg_subtle, bg = c.bg_dim },",
        "  },",
        "}",
        "",
    ])


def render(palette) -> dict:
    return {
        "colors/verdigris.lua": colorscheme(palette),
        "lua/lualine/themes/verdigris.lua": lualine(palette),
    }
