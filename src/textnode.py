from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
	TEXT = "normal"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"

class TextNode:
	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, other):
		if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
			return True
		return False
	

	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

	def text_node_to_html_node(self):
		if self.text_type == TextType.TEXT:
			return LeafNode(None, self.text, None)
		if self.text_type == TextType.BOLD:
			return LeafNode("b", self.text, None)
		if self.text_type == TextType.ITALIC:
			return LeafNode("i", self.text, None)
		if self.text_type == TextType.CODE:
			return LeafNode("code", self.text, None)
		if self.text_type == TextType.LINK:
			return LeafNode("a", self.text, {"href": self.url})
		if self.text_type == TextType.IMAGE:
			return LeafNode("img", "", {"src": self.url, "alt": self.text})
		raise Exception("Invalid text type.")