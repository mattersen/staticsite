import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
	def test_props_to_html_normal_dict(self):
		node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
		expected_result = ' href="https://www.google.com" target="_blank"'
		self.assertEqual(node.props_to_html(), expected_result)

	def test_props_to_html_props_empty(self):
		node = HTMLNode(props={})
		expected_result = ''
		self.assertEqual(node.props_to_html(), expected_result)

	def test_props_to_html_props_keyvalue_none(self):
		node = HTMLNode(props={"href": None})
		expected_result = ' href="None"'
		self.assertEqual(node.props_to_html(), expected_result)

	def test_props_to_html_props_none(self):
		node = HTMLNode(props=None)
		expected_result = ""
		self.assertEqual(node.props_to_html(), expected_result)

class TestLeafNode(unittest.TestCase):
	def test_to_html_props_eq_none(self):
		node = LeafNode("p", "This is a paragraph of text.")
		expected_result = "<p>This is a paragraph of text.</p>"
		self.assertEqual(node.to_html(), expected_result)

	def test_to_html_tag_value_props(self):
		node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
		expected_result = '<a href="https://www.google.com">Click me!</a>'
		self.assertEqual(node.to_html(), expected_result)

	def test_to_html_tag_value_multiprops(self):
		node = LeafNode("a", "Click me!", {"href": "https://www.google.com", "class": "button", "id": "main-link"})
		expected_result = '<a href="https://www.google.com" class="button" id="main-link">Click me!</a>'
		self.assertEqual(node.to_html(), expected_result)

	def test_to_html_tag_eq_none(self):
		node = LeafNode(None, "This is a paragraph of text.")
		expected_result = "This is a paragraph of text."
		self.assertEqual(node.to_html(), expected_result)

	def test_to_html_value_eq_none(self):
		node = LeafNode("p", None, {"href": "https://www.google.com"})
		with self.assertRaises(ValueError):
			node.to_html()

class TestParentNode(unittest.TestCase):
	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

	def test_to_html_with_no_leaf_nodes(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_one_node = ParentNode("one", [grandchild_node])
		child_two_node = ParentNode("two", [grandchild_node])
		child_three_node = ParentNode("three", [grandchild_node])
		parent_node = ParentNode("div", [child_one_node, child_two_node, child_three_node])
		self.assertEqual(parent_node.to_html(), "<div><one><b>grandchild</b></one><two><b>grandchild</b></two><three><b>grandchild</b></three></div>")

	def test_to_html_with_all_leaf_nodes(self):
		parent_node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")])
		self.assertEqual(parent_node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

	def test_to_html_with_tag_eq_none(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode(None, [child_node])
		with self.assertRaises(ValueError):
			parent_node.to_html()

	def test_to_html_with_children_eq_none(self):
		parent_node = ParentNode("div", None)
		with self.assertRaises(ValueError):
			parent_node.to_html()
			

if __name__ == "__main__":
	unittest.main()
