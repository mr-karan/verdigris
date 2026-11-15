# Verdigris for Windows Terminal

`verdigris.json` holds two colour schemes: "Verdigris Limestone" (light) and
"Verdigris Slate" (dark).

## Install

As a fragment, with no edit to your settings:

```powershell
$dir = "$env:LOCALAPPDATA\Microsoft\Windows Terminal\Fragments\verdigris"
New-Item -ItemType Directory -Force $dir | Out-Null
Copy-Item verdigris.json $dir
```

Restart Windows Terminal. Or copy the two objects under `schemes` into the
`schemes` array of your `settings.json`.

Then pick the schemes in a profile or in `profiles.defaults`:

```json
"colorScheme": { "light": "Verdigris Limestone", "dark": "Verdigris Slate" }
```
