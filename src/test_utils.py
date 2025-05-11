import unittest

from textnode import TextNode, TextType
from utils import split_nodes_delimiter, extract_markdown_images


class TestUtils(unittest.TestCase):

    def test_split(self):
        node = TextNode("This is text with a `code block` word",
                        TextType.TEXT)
        actual = split_nodes_delimiter([node],
                                       "`",
                                       TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(actual, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([
            ("image", "https://i.imgur.com/zjjcJKZ.png")
        ], matches)

        
if __name__ == "__main__":
    unittest.main()
