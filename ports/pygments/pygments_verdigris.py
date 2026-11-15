"""Verdigris for Pygments. Generated from palette.json: edit that, then run build.py.

https://github.com/mr-karan/verdigris
"""

from pygments.style import Style
from pygments.token import (
    Comment, Error, Generic, Keyword, Name, Number, Operator, Punctuation, String, Token, Whitespace,
)

class VerdigrisLimestoneStyle(Style):
    """Verdigris Limestone: the light flavour."""

    name = "verdigris-limestone"
    background_color = "#f3f3ee"
    highlight_color = "#ecede7"
    line_number_color = "#6f7975"
    line_number_background_color = "#f3f3ee"
    line_number_special_color = "#252d2a"
    line_number_special_background_color = "#ecede7"
    styles = {
        Token: "#252d2a",
        Whitespace: "#b7bbb1",
        Error: "#a8423f",
        Generic.Deleted: "#a8423f",
        Generic.Inserted: "#496c35",
        Generic.Error: "#a8423f",
        Generic.Traceback: "#a8423f",
        Generic.Prompt: "#6f7975",
        Generic.Output: "#5c6763",
        Generic.Emph: "italic #252d2a",
        Generic.Strong: "bold #1e2523",
        Generic.EmphStrong: "bold italic #1e2523",
        Comment: "italic #6f7975",
        Comment.Preproc: "noitalic #785480",
        Comment.PreprocFile: "noitalic #496c35",
        Keyword: "noitalic #2c6e64",
        Keyword.Constant: "noitalic #8f5226",
        Keyword.Type: "noitalic #76611b",
        Operator: "noitalic #5c6763",
        Operator.Word: "noitalic #2c6e64",
        Punctuation: "noitalic #5c6763",
        Name: "noitalic #252d2a",
        Name.Function: "noitalic #3d628a",
        Name.Function.Magic: "noitalic #3d628a",
        Name.Builtin: "noitalic #3d628a",
        Name.Builtin.Pseudo: "italic #785480",
        Name.Class: "noitalic #76611b",
        Name.Exception: "noitalic #76611b",
        Name.Decorator: "noitalic #785480",
        Name.Constant: "noitalic #8f5226",
        Name.Namespace: "noitalic #252d2a",
        Name.Tag: "noitalic #2c6e64",
        Name.Attribute: "noitalic #76611b",
        Name.Label: "noitalic #785480",
        Name.Entity: "noitalic #8f5226",
        Name.Property: "noitalic #252d2a",
        Name.Variable.Magic: "italic #785480",
        String: "noitalic #496c35",
        String.Doc: "italic #6f7975",
        String.Escape: "noitalic #76611b",
        String.Interpol: "noitalic #76611b",
        String.Regex: "noitalic #76611b",
        String.Symbol: "noitalic #8f5226",
        Number: "noitalic #8f5226",
        Generic.Heading: "bold noitalic #2c6e64",
        Generic.Subheading: "bold noitalic #2c6e64",
    }


class VerdigrisSlateStyle(Style):
    """Verdigris Slate: the dark flavour."""

    name = "verdigris-slate"
    background_color = "#151a19"
    highlight_color = "#1b2120"
    line_number_color = "#75827d"
    line_number_background_color = "#151a19"
    line_number_special_color = "#d0d7d3"
    line_number_special_background_color = "#1b2120"
    styles = {
        Token: "#d0d7d3",
        Whitespace: "#3a4543",
        Error: "#e38d86",
        Generic.Deleted: "#e38d86",
        Generic.Inserted: "#a3c18d",
        Generic.Error: "#e38d86",
        Generic.Traceback: "#e38d86",
        Generic.Prompt: "#75827d",
        Generic.Output: "#8e9a96",
        Generic.Emph: "italic #d0d7d3",
        Generic.Strong: "bold #dde3df",
        Generic.EmphStrong: "bold italic #dde3df",
        Comment: "italic #75827d",
        Comment.Preproc: "noitalic #c0a1c9",
        Comment.PreprocFile: "noitalic #a3c18d",
        Keyword: "noitalic #82c3b4",
        Keyword.Constant: "noitalic #d9a377",
        Keyword.Type: "noitalic #cabf7f",
        Operator: "noitalic #8e9a96",
        Operator.Word: "noitalic #82c3b4",
        Punctuation: "noitalic #8e9a96",
        Name: "noitalic #d0d7d3",
        Name.Function: "noitalic #8fb2d8",
        Name.Function.Magic: "noitalic #8fb2d8",
        Name.Builtin: "noitalic #8fb2d8",
        Name.Builtin.Pseudo: "italic #c0a1c9",
        Name.Class: "noitalic #cabf7f",
        Name.Exception: "noitalic #cabf7f",
        Name.Decorator: "noitalic #c0a1c9",
        Name.Constant: "noitalic #d9a377",
        Name.Namespace: "noitalic #d0d7d3",
        Name.Tag: "noitalic #82c3b4",
        Name.Attribute: "noitalic #cabf7f",
        Name.Label: "noitalic #c0a1c9",
        Name.Entity: "noitalic #d9a377",
        Name.Property: "noitalic #d0d7d3",
        Name.Variable.Magic: "italic #c0a1c9",
        String: "noitalic #a3c18d",
        String.Doc: "italic #75827d",
        String.Escape: "noitalic #cabf7f",
        String.Interpol: "noitalic #cabf7f",
        String.Regex: "noitalic #cabf7f",
        String.Symbol: "noitalic #d9a377",
        Number: "noitalic #d9a377",
        Generic.Heading: "bold noitalic #82c3b4",
        Generic.Subheading: "bold noitalic #82c3b4",
    }
