# Verdigris for VS Code

Two colour themes, "Verdigris Limestone" (light) and "Verdigris Slate" (dark),
with workbench colours, TextMate token colours and semantic token colours.

## Install

The extension is not on the Marketplace yet. Build it from this directory:

```sh
npx @vscode/vsce package
code --install-extension verdigris-0.1.0.vsix
```

Then run **Preferences: Color Theme** and pick a flavour, or follow the system
appearance in `settings.json`:

```json
{
  "window.autoDetectColorScheme": true,
  "workbench.preferredLightColorTheme": "Verdigris Limestone",
  "workbench.preferredDarkColorTheme": "Verdigris Slate"
}
```

The same steps work in forks that load VS Code extensions, such as VSCodium
and Cursor.
