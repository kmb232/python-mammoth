from parsimonious.grammar import Grammar

from .. import html_paths


def read_html_path(string):
    path_node = _grammar.parse(string)
    return read_html_path_node(path_node)


def read_html_path_node(path_node):
    if path_node.children:
        return _read_html_path_elements_node(path_node.children[0])
    else:
        return html_paths.empty


def _read_html_path_elements_node(path_node):
    elements = [
        _read_element_node(child)
        for child in _repeated_children_with_separator(path_node, has_whitespace=True)
    ]
    return html_paths.path(elements)


def _read_element_node(node):
    tag_names = _read_tag_names_node(node.children[0])
    class_names = _read_class_names_node(node.children[1])
    extra_attributes = _read_extra_attributes_node(node.children[2])
    fresh = _read_fresh_node(node.children[3])
    always_merge = _read_always_merge_node(node.children[4])
    return html_paths.element(tag_names, class_names=class_names,
                              extra_attributes=extra_attributes, fresh=fresh,
                              always_merge=always_merge)


def _read_tag_names_node(node):
    return [
        child.text
        for child in _repeated_children_with_separator(node, has_whitespace=False)
    ]


def _read_class_names_node(class_names_node):
    return [
        _read_class_name_node(node)
        for node in class_names_node.children
    ]


def _read_class_name_node(node):
    return node.children[1].text


def _read_extra_attributes_node(extra_attributes_node):
    if extra_attributes_node.text:
        initial_node = extra_attributes_node.children[0].children[1]
        more_nodes = [n.children[1] for n in
                      extra_attributes_node.children[0].children[2].children]
        return dict(_read_extra_attribute_node(node) for node in
                    [initial_node] + more_nodes)


def _read_extra_attribute_node(node):
    return (node.children[0].text, node.children[2].text)


def _read_fresh_node(node):
    return len(node.children) > 0


def _read_always_merge_node(node):
    return len(node.children) > 0


def _repeated_children_with_separator(node, has_whitespace):
    yield node.children[0]

    if has_whitespace:
        sequence_node_index = 3
    else:
        sequence_node_index = 1

    sequence_node = node.children[1]
    for child in sequence_node.children:
        yield child.children[sequence_node_index]


grammar_text = r"""

html_path = html_path_elements?

html_path_elements = element (whitespace* ">" whitespace* element)*

element = tag_names class_name* attrs? fresh? always_merge?

tag_names = identifier ("|" identifier)*

class_name = "." identifier

attrs = "{" attr_pair comma_attr_pair* "}"

attr_pair = identifier "=" identifier

comma_attr_pair = "," attr_pair

fresh = ":fresh"

always_merge = "!merge"

identifier = ~"[A-Z0-9]+"i

whitespace = ~"\s"*

"""

_grammar = Grammar(grammar_text)
