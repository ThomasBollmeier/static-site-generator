import unittest

from generator import *


class TestTextNode(unittest.TestCase):

    def test_extract_title(self):
        md = "# This is a title\nThis is a paragraph"
        title = extract_title(md)
        self.assertEqual(title, "This is a title")

if __name__ == "__main__":
    unittest.main()
