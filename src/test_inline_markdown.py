import unittest, re

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestTextNode(unittest.TestCase):
    maxDiff = None

    def test_split_nodes_delimiter_italic_start(self):
        node = TextNode("*This is a NEW text with* ITALIC text amigo", TextType.NORMAL)
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is a NEW text with", TextType.ITALIC, None),
            TextNode(" ITALIC text amigo", TextType.NORMAL, None)
            ]
        self.assertEqual(result, expected)
  
    def test_split_nodes_delimiter_italic_middle(self):
        node = TextNode("This is a NEW text with *ITALIC text* amigo", TextType.NORMAL)
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is a NEW text with ", TextType.NORMAL, None), 
            TextNode("ITALIC text", TextType.ITALIC, None), 
            TextNode(" amigo", TextType.NORMAL, None)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_italic_end(self):
        node = TextNode("This is a NEW text with ITALIC text *amigo*", TextType.NORMAL)
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is a NEW text with ITALIC text ", TextType.NORMAL, None),
            TextNode("amigo", TextType.ITALIC, None)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_bold_start(self): 
        node = TextNode("**This is a text with** BOLD text amigo", TextType.NORMAL)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is a text with", TextType.BOLD, None),
            TextNode(" BOLD text amigo", TextType.NORMAL, None)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_bold_middle(self):
        node = TextNode("This is a text with **BOLD text** amigo", TextType.NORMAL)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is a text with ", TextType.NORMAL, None), 
            TextNode("BOLD text", TextType.BOLD, None), 
            TextNode(" amigo", TextType.NORMAL, None)
        ]
        self.assertEqual(result, expected)
   
    def test_split_nodes_delimiter_bold_end(self):       
        node = TextNode("This is a text with BOLD text **AMIGO**", TextType.NORMAL)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is a text with BOLD text ", TextType.NORMAL, None),
            TextNode("AMIGO", TextType.BOLD, None)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_no_delimiter(self):       
        node = TextNode("This is a text without delimiters", TextType.NORMAL)
        result = split_nodes_delimiter([node], "", TextType.NORMAL)
        expected = [
            TextNode("This is a text without delimiters", TextType.NORMAL, None)
        ]
        self.assertEqual(result, expected)
    
    def test_split_nodes_delimiter_italic_delimiter_twice(self):       
        node = TextNode("This is a *text with* 2 italic *text parts*", TextType.NORMAL)
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is a ", TextType.NORMAL, None),
            TextNode("text with", TextType.ITALIC, None),
            TextNode(" 2 italic ", TextType.NORMAL, None),
            TextNode("text parts", TextType.ITALIC, None)
        ]
        self.assertEqual(result, expected)
    
    def test_split_nodes_delimiter_unmatched(self):
        node = TextNode("This is *italic but not closed", TextType.NORMAL)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.ITALIC)
        
    def test_split_nodes_delimiter_multiple_nodes(self):
        node1 = TextNode("Normal text", TextType.NORMAL)
        node2 = TextNode("*Italic text*", TextType.NORMAL)
        node3 = TextNode("More normal", TextType.NORMAL)
        result = split_nodes_delimiter([node1, node2, node3], "*", TextType.ITALIC)
        expected = [
            TextNode("Normal text", TextType.NORMAL),
            TextNode("Italic text", TextType.ITALIC),
            TextNode("More normal", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is `code` text", TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_empty_edges(self):
        node = TextNode("**bold** text **bold2**", TextType.NORMAL)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" text ", TextType.NORMAL),
            TextNode("bold2", TextType.BOLD)
        ]
        self.assertEqual(result, expected)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        matches = extract_markdown_images(text)
        expected = [('rick roll', 'https://i.imgur.com/aKaOqIh.gif')]
        self.assertEqual(matches, expected)

    def test_extract_markdown_images_no_match(self):
        text = "This is text without images"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [])

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        expected = [('to boot dev', 'https://www.boot.dev')]
        self.assertEqual(matches, expected)

    def test_extract_markdown_links_no_match(self):
        text = "This is text without link"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        expected = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            expected,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [link image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        expected = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "link image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            expected,
        )

    def test_split_image_one(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.NORMAL,
        )
        expected = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            expected
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

if __name__ == "__main__":
    unittest.main()

   