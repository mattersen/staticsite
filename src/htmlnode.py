
class HTMLNode:
	def __init__(self, tag=None, value=None, children=None, props=None):
		# String representing the HTML tag name (e.g. "p", "a", "h1")
		self.tag = tag
		# String representing the value of the above tag (e.g. the text inside paragraph) 
		self.value = value
		# List of HTMLNode objects representing the children of this node.
		self.children = children
		# Dictionary of key-value pairs representing the attributes of the HTML tag (e.g. a link <a> tag might have {"href": "https://www.google.com"}
		self.props = props

	def to_html(self):
		raise NotImplementedError

	def props_to_html(self):
		concat_string = ""
		if self.props:
			for key, value in self.props.items():
				concat_string += f' {key}="{value}"'
			return concat_string
		return ""

	def __repr__(self):
		return f'HTMLNode(tag="{self.tag}", value="{self.value}", children="{self.children}", props="{self.props}")'

class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__(tag, value, None, props)
						
	def to_html(self):
		if self.value is None:
			raise ValueError("invalid HTML: no value")
		if self.tag is None:
			return f'{self.value}'
		return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
	
	def __repr__(self):
		return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		if self.tag is None:
			raise ValueError("invalid HTML: no tag")
		if self.children is None:
			raise ValueError("invalid HTML: no children")
		children = ""
		for child in self.children:
			children += child.to_html()
		return f'<{self.tag}{self.props_to_html()}>{children}</{self.tag}>'
