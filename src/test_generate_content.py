import unittest
from generate_content import extract_title


class TestTextNode(unittest.TestCase):
    def test_extract_title(self):
        markdown = """
            # This is a heading
        """
        self.assertEqual(extract_title(markdown), "This is a heading") 

    def test_extract_title_none_heading(self):
        markdown = """
            This is NOT a heading
        """
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertTrue("Too many # for a heading section / heading section doesn't exist" in str(context.exception))

    def test_extract_title_no_h1_heading(self):
        markdown = """
            ## This is a heading but level 2
        """
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()