import unittest
from textnode import TextNode, TextType
from helper_funcs import *


class TestHelperFuncs(unittest.TestCase):
    def test_split_nodes_bold(self):
        node = TextNode("**This** is text with a **bold** word and also another **bolded Word** in the text.", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            split_nodes, 
            [
                TextNode("This", TextType.BOLD), 
                TextNode(" is text with a ", TextType.TEXT), 
                TextNode("bold", TextType.BOLD), 
                TextNode(" word and also another ", TextType.TEXT), 
                TextNode("bolded Word", TextType.BOLD), 
                TextNode(" in the text.", TextType.TEXT)
            ]
        ) 
    
    def test_split_nodes_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        split_nodes = (split_nodes_delimiter([node], "`", TextType.CODE))
        self.assertListEqual(
            split_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ]
        )
        
    def test_split_nodes_italic(self):
        node = TextNode("This _is text_ with an _italic block_", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            split_nodes,
            [
                TextNode("This ", TextType.TEXT),
                TextNode("is text", TextType.ITALIC), 
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC)
            ]
        )

    def test_split_nodes_bold_and_italic(self):    
        node = TextNode("This is **bold text** with an _italic block_.", TextType.TEXT)
        split_nodes = (split_nodes_delimiter([node], "**", TextType.BOLD))
        split_nodes = (split_nodes_delimiter(split_nodes, "_", TextType.ITALIC))
        self.assertListEqual(
            split_nodes,
            [
                TextNode("This is ", TextType.TEXT), 
                TextNode("bold text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(".", TextType.TEXT)
            ]
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ('to boot dev', 'https://www.boot.dev'), 
                ('to youtube', 'https://www.youtube.com/@bootdotdev')
            ], 
            matches
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_empty_alt_text(self):
        node = TextNode(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_empty_image_url(self):
        node = TextNode(
            "This is text with an ![image]() and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, ""),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link text](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links_empty_alt_text(self):
        node = TextNode(
            "This is text with an [](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links_empty_links_url(self):
        node = TextNode(
            "This is text with an [link]() and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, ""),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_text_to_text_nodes(self):
        node = TextNode(
            "This is **text** with an _italic_ word and a `code block` "
            "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)", TextType.TEXT,
        )
        new_nodes = text_to_textnodes(node.text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    if __name__ == "__main__":
        unittest.main()