from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_blocks import markdown_to_html_node
from inline_markdown import *

def main():
	md = """
```
here is some code

and some more


after some blank spaces
```
"""

	node = markdown_to_html_node(md)
	html = node.to_html()
	print(html)

	with open("example.html", "w") as file:
		file.write(html)

main()
