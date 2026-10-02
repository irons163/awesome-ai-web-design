"""Small standard-library HTML tree for adapting saved public snapshots."""
from html import escape
from html.parser import HTMLParser

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link',
        'meta', 'param', 'source', 'track', 'wbr'}


class Node:
    def __init__(self, tag='', attrs=None, text=None):
        self.tag, self.attrs, self.text = tag, dict(attrs or []), text
        self.children = []

    def walk(self):
        yield self
        for child in self.children:
            yield from child.walk()

    def find(self, predicate):
        return next((node for node in self.walk() if predicate(node)), None)

    def render(self):
        if self.text is not None:
            return self.text
        children = ''.join(child.render() for child in self.children)
        if not self.tag:
            return children
        attrs = ''.join(' ' + key + ('' if value is None else
                        '="' + escape(str(value), quote=True) + '"')
                        for key, value in self.attrs.items())
        opening = '<' + self.tag + attrs + '>'
        return opening if self.tag in VOID else opening + children + '</' + self.tag + '>'


class Tree(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.root = Node()
        self.stack = [self.root]
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Node(tag, attrs))

    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                self.stack = self.stack[:i]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(Node(text=data))

    def handle_entityref(self, name):
        self.handle_data('&' + name + ';')

    def handle_charref(self, name):
        self.handle_data('&#' + name + ';')

    def handle_comment(self, data):
        self.handle_data('<!--' + data + '-->')


def fragment(source):
    return Tree(source).root.children
