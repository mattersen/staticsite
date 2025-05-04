from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from helper_funcs import *


def main():

	
	sample_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

	
	print(text_to_textnodes(sample_text))

main()
