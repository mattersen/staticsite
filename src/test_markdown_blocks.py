import unittest

from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):

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

    def test_markdown_to_blocks_plus_whitespace(self):
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

    def test_block_to_block_type_heading_one(self):
        md = "# this is a heading"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_block_type_heading_six(self):
        md = "###### this is a heading"
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.HEADING, block_type)

    def test_block_to_block_type_code(self):
        md = """```this is a test for code blocks
and some more text on a second line,
now a third line
```"""
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.CODE, block_type)

    def test_block_to_block_type_quote(self):
        md = """>this is a test for code blocks
>and some more text on a second line,
>now a third line
> four quoted lines!"""
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.QUOTE, block_type)

    def test_block_to_block_type_unordered_list(self):
        md = """- this is a test for code blocks
- and some more text on a second line,
- now a third line
- """
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)

    def test_block_to_block_type_ordered_list(self):
        md = """1. this is a test for code blocks
2. and some more text on a second line,
3. now a third line
4. x"""
        block_type = block_to_block_type(md)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)

def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )