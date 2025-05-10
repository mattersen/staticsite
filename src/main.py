from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_blocks import markdown_to_blocks
from inline_markdown import *


def main():

	
	markdown = """\n\n
hello


world
\n\n"""
	
	print(markdown_to_blocks(markdown))

main()
