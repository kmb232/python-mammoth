import cobble

from . import html


def path(elements):
    return HtmlPath(elements)


def element(names, class_names=None, extra_attributes=None, fresh=None):
    if class_names is None:
        class_names = []
    if extra_attributes is None:
        extra_attributes = {}
    if fresh is None:
        fresh = False
    return HtmlPathElement(names, class_names, extra_attributes, fresh)


@cobble.data
class HtmlPath(object):
    elements = cobble.field()

    def wrap(self, nodes):
        for element in reversed(self.elements):
            nodes = element.wrap(nodes)

        return nodes

@cobble.data
class HtmlPathElement(object):
    names = cobble.field()
    class_names = cobble.field()
    extra_attributes = cobble.field()
    fresh = cobble.field()

    def wrap(self, nodes):
        if self.class_names:
            attributes = {"class": " ".join(self.class_names)}
        else:
            attributes = {}
        if self.extra_attributes:
            attributes.update(extra_attributes)
        element = html.element(
            self.names,
            attributes,
            nodes,
            collapsible=not self.fresh)
        return [element]

empty = path([])
