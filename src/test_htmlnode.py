import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):

    def test_with_tag(self):
        node = HTMLNode(tag="h1", value="Title")
        self.assertTrue(node.children is None)

    def test_with_children(self):
        node = HTMLNode(tag="ul",
                children=[
                    HTMLNode("li", "first"),
                    HTMLNode("li", "second")
                    ])
        self.assertTrue(len(node.children) == 2)

    def test_with_props(self):
        node = HTMLNode(tag="a", 
                value="some link",
                props={
                    "href": "http://bollmeier.de"
                })
        actual = node.props_to_html()
        expected = ' href="http://bollmeier.de"'
        self.assertEqual(actual, expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_raw(self):
        node = LeafNode(None, "some text")
        self.assertEqual(node.to_html(), "some text")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()
