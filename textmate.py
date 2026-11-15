"""TextMate scopes for the syntax roles, shared by the ports that speak them
(VS Code, and the .tmTheme used by bat, delta and Sublime Text).

Later rules win over earlier ones of the same specificity, so the general
rule for a scope family comes before its exceptions.
"""

from palette import Flavour, Style

# (label, scopes, syntax role)
ROLE_RULES = [
    ("Variable", ["variable", "variable.other"], "variable"),
    ("Parameter", ["variable.parameter"], "parameter"),
    ("Property", [
        "variable.other.property", "variable.other.object.property", "variable.other.member",
        "support.variable.property", "meta.object-literal.key", "variable.other.field",
    ], "property"),
    ("Namespace", [
        "entity.name.namespace", "entity.name.module", "entity.name.package",
        "entity.name.type.module", "entity.name.scope-resolution", "support.other.namespace",
    ], "namespace"),
    ("Comment", ["comment", "punctuation.definition.comment", "string.comment"], "comment"),
    ("Punctuation", [
        "punctuation", "meta.brace", "punctuation.separator", "punctuation.terminator",
        "punctuation.section", "punctuation.accessor", "punctuation.definition.tag",
        "punctuation.definition.parameters", "punctuation.definition.block",
    ], "punctuation"),
    ("Operator", ["keyword.operator", "punctuation.definition.keyword"], "operator"),
    ("Keyword", [
        "keyword", "keyword.control", "keyword.other", "keyword.declaration", "storage",
        "storage.type", "storage.modifier", "keyword.operator.new", "keyword.operator.expression",
        "keyword.operator.logical.python", "keyword.operator.word", "keyword.operator.wordlike",
        "keyword.operator.delete", "keyword.operator.typeof", "keyword.operator.instanceof",
        "keyword.operator.sizeof", "keyword.operator.cast", "keyword.operator.alignof",
    ], "keyword"),
    ("Function", [
        "entity.name.function", "support.function", "variable.function", "entity.name.method",
        "meta.function-call entity.name.function", "meta.function-call.generic",
        "entity.name.command", "support.function.builtin",
    ], "function"),
    ("Type", [
        "entity.name.type", "entity.name.class", "entity.name.struct", "entity.name.enum",
        "entity.name.interface", "entity.name.trait", "entity.name.union",
        "entity.other.inherited-class", "support.type", "support.class",
        "storage.type.numeric", "storage.type.string", "storage.type.boolean",
        "storage.type.primitive", "storage.type.built-in", "storage.type.byte",
        "storage.type.rune", "storage.type.uintptr", "storage.type.error",
        "storage.type.java", "storage.type.cs", "storage.type.generic",
        "storage.type.go", "storage.type.c", "storage.type.c++",
    ], "type"),
    ("String", [
        "string", "string.quoted", "string.template", "string.unquoted",
        "punctuation.definition.string", "markup.raw", "markup.inline.raw",
    ], "string"),
    ("Escape", [
        "constant.character.escape", "constant.other.placeholder",
        "punctuation.definition.template-expression", "punctuation.section.embedded",
        "punctuation.section.interpolation", "constant.character.format",
    ], "escape"),
    ("Regex", [
        "string.regexp", "string.regexp punctuation", "string.regexp keyword",
        "string.regexp constant.other.character-class", "string.regexp constant.character",
    ], "regex"),
    ("Number", ["constant.numeric", "keyword.other.unit"], "number"),
    ("Constant", [
        "constant.language", "constant.other", "constant.character", "support.constant",
        "variable.other.enummember", "constant.other.caps", "entity.name.constant",
    ], "constant"),
    ("Key", [
        "support.type.property-name", "entity.name.tag.yaml", "entity.name.tag.toml",
        "support.type.property-name.toml", "keyword.other.definition.ini",
        "meta.property-name", "support.type.vendored.property-name",
    ], "key"),
    ("Tag", ["entity.name.tag", "support.class.component"], "tag"),
    ("Attribute", [
        "entity.other.attribute-name", "entity.other.attribute-name.class",
        "entity.other.attribute-name.id", "entity.other.attribute-name.pseudo-class",
    ], "attribute"),
    ("Decorator", [
        "meta.decorator", "entity.name.function.decorator", "punctuation.decorator",
        "punctuation.definition.decorator", "storage.type.annotation",
        "punctuation.definition.annotation", "meta.attribute", "meta.annotation",
        "entity.name.function.macro", "support.function.macro", "support.macro",
        "entity.name.function.preprocessor", "meta.preprocessor", "keyword.control.directive",
        "keyword.control.import.include", "punctuation.definition.directive",
    ], "decorator"),
    ("Language variable", ["variable.language", "variable.language.this", "variable.language.self"], "builtin"),
    ("Label", [
        "entity.name.label", "storage.modifier.lifetime", "entity.name.lifetime",
        "punctuation.definition.lifetime", "entity.name.type.lifetime",
    ], "label"),
    ("Heading", [
        "markup.heading", "entity.name.section", "punctuation.definition.heading",
        "markup.heading entity.name",
    ], "heading"),
    ("Link", ["markup.underline.link", "string.other.link", "meta.link", "constant.other.reference.link"], "link"),
]

# (label, scopes, palette colour, style flags)
COLOR_RULES = [
    ("Bold", ["markup.bold"], "fg_strong", {"bold": True}),
    ("Italic", ["markup.italic"], "fg", {"italic": True}),
    ("Quote", ["markup.quote"], "fg_muted", {"italic": True}),
    ("List marker", ["markup.list punctuation.definition.list", "punctuation.definition.list.begin"], "patina", {}),
    ("Inserted", ["markup.inserted", "punctuation.definition.inserted"], "malachite", {}),
    ("Deleted", ["markup.deleted", "punctuation.definition.deleted"], "cuprite", {}),
    ("Changed", ["markup.changed", "punctuation.definition.changed"], "azurite", {}),
    ("Diff header", ["meta.diff.header", "meta.diff.index", "punctuation.definition.from-file", "punctuation.definition.to-file"], "fg_muted", {}),
    ("Diff range", ["meta.diff.range", "punctuation.definition.range"], "bornite", {}),
    ("Invalid", ["invalid", "invalid.illegal"], "cuprite", {}),
    ("Deprecated", ["invalid.deprecated"], "copper", {"italic": True}),
]


def rules(flavour: Flavour) -> list:
    """(label, scopes, Style) for one flavour, in override order."""
    resolved = [(label, scopes, flavour.syntax[role]) for label, scopes, role in ROLE_RULES]
    resolved += [
        (label, scopes, Style(flavour[color], **flags)) for label, scopes, color, flags in COLOR_RULES
    ]
    return resolved


def font_style(style: Style) -> str:
    return " ".join(name for name in ("italic", "bold", "underline") if getattr(style, name))
