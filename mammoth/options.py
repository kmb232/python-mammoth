from . import style_reader, lists, results


def read_options(options):
    custom_style_map_result = _read_style_map(options.get("style_map") or "")
    include_default_style_map = options.get("include_default_style_map", True)
    options["ignore_empty_paragraphs"] = options.get("ignore_empty_paragraphs", True)

    options["style_map"] = custom_style_map_result.value + \
        (_default_style_map if include_default_style_map else [])
    return custom_style_map_result.map(lambda _: options)


def _read_style_map(style_text):
    lines = filter(None, map(_get_line, style_text.split("\n")))
    return results.combine(lists.map(style_reader.read_style, lines)) \
        .map(lambda style_mappings: lists.filter(None, style_mappings))


def _get_line(line):
    line = line.strip()
    if line.startswith("#"):
        return None
    else:
        return line


_default_style_map_result = _read_style_map("""
p.Heading1 => h1:fresh
p.Heading2 => h2:fresh
p.Heading3 => h3:fresh
p.Heading4 => h4:fresh
p[style-name='Heading 1'] => h1:fresh
p[style-name='Heading 2'] => h2:fresh
p[style-name='Heading 3'] => h3:fresh
p[style-name='Heading 4'] => h4:fresh
p[style-name='heading 1'] => h1:fresh
p[style-name='heading 2'] => h2:fresh
p[style-name='heading 3'] => h3:fresh
p[style-name='heading 4'] => h4:fresh
p[style-name='heading 4'] => h4:fresh

r[style-name='Strong'] => strong

p[style-name='footnote text'] => p
r[style-name='footnote reference'] =>
p[style-name='endnote text'] => p
r[style-name='endnote reference'] =>

# LibreOffice
p[style-name='Footnote'] => p
r[style-name='Footnote anchor'] =>
p[style-name='Endnote'] => p
r[style-name='Endnote anchor'] =>

p:unordered-list(1) => ul > li:fresh
p:unordered-list(2) => ul|ol > li > ul > li:fresh
p:unordered-list(3) => ul|ol > li > ul|ol > li > ul > li:fresh
p:unordered-list(4) => ul|ol > li > ul|ol > li > ul|ol > li > ul > li:fresh
p:unordered-list(5) => ul|ol > li > ul|ol > li > ul|ol > li > ul|ol > li > ul > li:fresh
p:ordered-list(1) => ol > li:fresh
p:ordered-list(2) => ul|ol > li > ol > li:fresh
p:ordered-list(3) => ul|ol > li > ul|ol > li > ol > li:fresh
p:ordered-list(4) => ul|ol > li > ul|ol > li > ul|ol > li > ol > li:fresh
p:ordered-list(5) => ul|ol > li > ul|ol > li > ul|ol > li > ul|ol > li > ol > li:fresh

# pattern for different numbering formats -- all this is repetitive but
# it's the easiest way to do it for now
p:ordered-list(1,decimal) => ol > li{type=1}:fresh
p:ordered-list(1,lowerLetter) => ol > li{type=a}:fresh
p:ordered-list(1,lowerRoman) => ol > li{type=i}:fresh
p:ordered-list(1,upperLetter) => ol > li{type=A}:fresh
p:ordered-list(1,upperRoman) => ol > li{type=I}:fresh
p:ordered-list(2,decimal) => ul|ol > li > ol > li{type=1}:fresh
p:ordered-list(2,lowerLetter) => ul|ol > li > ol > li{type=a}:fresh
p:ordered-list(2,lowerRoman) => ul|ol > li > ol > li{type=i}:fresh
p:ordered-list(2,upperLetter) => ul|ol > li > ol > li{type=A}:fresh
p:ordered-list(2,upperRoman) => ul|ol > li > ol > li{type=I}:fresh
p:ordered-list(3,decimal) => ul|ol > li > ul|ol > li > ol > li{type=1}:fresh
p:ordered-list(3,lowerLetter) => ul|ol > li > ul|ol > li > ol > li{type=a}:fresh
p:ordered-list(3,lowerRoman) => ul|ol > li > ul|ol > li > ol > li{type=i}:fresh
p:ordered-list(3,upperLetter) => ul|ol > li > ul|ol > li > ol > li{type=A}:fresh
p:ordered-list(3,upperRoman) => ul|ol > li > ul|ol > li > ol > li{type=I}:fresh
p:ordered-list(4,decimal) => ul|ol > li > ul|ol > li > ul|ol > li > ol > li{type=1}:fresh
p:ordered-list(4,lowerLetter) => ul|ol > li > ul|ol > li > ul|ol > li > ol > li{type=a}:fresh
p:ordered-list(4,lowerRoman) => ul|ol > li > ul|ol > li > ul|ol > li > ol > li{type=i}:fresh
p:ordered-list(4,upperLetter) => ul|ol > li > ul|ol > li > ul|ol > li > ol > li{type=A}:fresh
p:ordered-list(4,upperRoman) => ul|ol > li > ul|ol > li > ul|ol > li > ol > li{type=I}:fresh
p:ordered-list(5,decimal) => ul|ol > li > ul|ol > li > ul|ol > li > ul|ol > li > ol > li{type=1}:fresh
p:ordered-list(5,lowerLetter) => ul|ol > li > ul|ol > li > ul|ol > li > ul|ol > li > ol > li{type=a}:fresh
p:ordered-list(5,lowerRoman) => ul|ol > li > ul|ol > li > ul|ol > li > ul|ol > li > ol > li{type=i}:fresh
p:ordered-list(5,upperLetter) => ul|ol > li > ul|ol > li > ul|ol > li > ul|ol > li > ol > li{type=A}:fresh
p:ordered-list(5,upperRoman) => ul|ol > li > ul|ol > li > ul|ol > li > ul|ol > li > ol > li{type=I}:fresh



r[style-name='Hyperlink'] =>

p[style-name='Normal'] => p:fresh
""")

assert not _default_style_map_result.messages
_default_style_map = _default_style_map_result.value
