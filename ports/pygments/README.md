# Verdigris for Pygments

Two styles, `verdigris-limestone` (light) and `verdigris-slate` (dark).

## Install

```sh
pip install "git+https://github.com/mr-karan/verdigris#subdirectory=ports/pygments"
```

The package registers both styles, so they work by name:

```sh
pygmentize -O style=verdigris-slate -f terminal16m example.py
```

```python
from pygments.formatters import HtmlFormatter

formatter = HtmlFormatter(style="verdigris-limestone")
```

Without installing, put `pygments_verdigris.py` on your path and pass the
class: `HtmlFormatter(style=pygments_verdigris.VerdigrisSlateStyle)`.
