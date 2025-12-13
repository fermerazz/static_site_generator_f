import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("image", "hello I am an image", None, {"href": "https://www.google.com",
                                                               "target": "_blank"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "text", None, None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", "text", None, {})
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode("a", "link", None, {"href": "https://www.google.com"})
        result =node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com"')
    
    def test_repr(self):
        node = HTMLNode("p", "Hello world", None, {"class": "greeting"})
        result = repr(node)
        expected = "HTMLNode(tag=p, value=Hello world, children=None, props={'class': 'greeting'})"
        self.assertEqual(result, expected)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode( "a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_no_children(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode("span", None)
            parent_node.to_html()

    def test_to_html_no_tag(self):
        with self.assertRaises(ValueError):
            child_node = LeafNode("span", "child")
            parent_node = ParentNode(None, [child_node])
            parent_node.to_html()

    def test_to_html_parent_inside_parent(self):
        child_node = LeafNode("span", "child")
        parent_leaf_node = ParentNode("p", [child_node])
        parent_node = ParentNode("div", [parent_leaf_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p><span>child</span></p></div>"
        )