import unittest

from block_markdown import *


class TestTextNode(unittest.TestCase):
    maxDiff = None

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
            md = """
    This is **bolded** paragraph




    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
    
    def test_block_to_block_types_headings(self):
        md = '''
        # This is a heading 1
        ## This is a heading 2
        ### This is a heading 3
        #### This is a heading 4
        ##### This is a heading 5
        ###### This is a heading 6
        '''
        blocks = markdown_to_blocks(md)
        for block in blocks:
            result = block_to_block_type(block)
            self.assertEqual(result, BlockType.heading) 

    def test_block_to_block_types_code(self):
        md = '''
        ```
        This is code snippet\nwith more code
        ```
        '''
        blocks = markdown_to_blocks(md)
        for block in blocks:
            result = block_to_block_type(block)
            self.assertEqual(result, BlockType.code) 

    def test_block_to_block_types_unordered_list(self):
        md = '''
        - This is the first list item in a list block\n- This is a list item\n- This is another list item
        '''
        blocks = markdown_to_blocks(md)
        for block in blocks:
            result = block_to_block_type(block)
            self.assertEqual(result, BlockType.unordered_list) 

    def test_block_to_block_types_code_ordered_list(self):
        md = '''
        1. item 1\n2. item 2\n3. item 3 
        '''
        blocks = markdown_to_blocks(md)
        for block in blocks:
            result = block_to_block_type(block)
            self.assertEqual(result, BlockType.ordered_list) 

    def test_block_to_block_types_quote(self):
        md = '''
         > quote text\n> second quote text
        '''
        blocks = markdown_to_blocks(md)
        for block in blocks:
            result = block_to_block_type(block)
            self.assertEqual(result, BlockType.quote)     

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that *should* remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that *should* remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    
if __name__ == "__main__":
    unittest.main()

   