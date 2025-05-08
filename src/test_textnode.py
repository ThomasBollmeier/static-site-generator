import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("bold text", TextType.BOLD)
        node2 = TextNode("italic", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_not_eq2(self):
        node = TextNode("some link", TextType.LINK)
        node2 = TextNode("some link", TextType.LINK, "http://bollmeier.de")
        self.assertNotEqual(node, node2)

    def test_eq2(self):
        node = TextNode("some image", TextType.IMAGE, "pic.png")
        node2 = TextNode("some image", TextType.IMAGE, "pic.png")
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
