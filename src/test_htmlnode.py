import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_success(self):
        node = HTMLNode(props = {"target" : "_blank"})
        string = node.props_to_html()
        self.assertEqual(string, ' target="_blank"')

    def test_props_to_html_fail(self):
        node = HTMLNode({"target" : "_blank"})
        string = node.props_to_html()
        self.assertNotEqual(string, {"href" : "https://www.bootdev.com"})

    def test_props_to_html_none(self):
        node = HTMLNode()
        string = node.props_to_html()
        self.assertEqual(string, "")

    def test_repr_eq(self):
        node = HTMLNode("p", "paragraph text", None, {"target": "_blank"})
        self.assertEqual(node.__repr__(), "HTMLNode(p, paragraph text, children: None, {'target': '_blank'})")

    def test_value(self):
        node = HTMLNode("p", "paragraph text",)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "paragraph text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_to_html_link(self):
        leaf_node = LeafNode("a", "Click me!", props = {"href" : "https://www.bootdev.com"})
        string = leaf_node.to_html()
        self.assertEqual(string, '<a href="https://www.bootdev.com">Click me!</a>')

    def test_to_html_success(self):
        leaf_node = LeafNode("p", "paragraph text")
        string = leaf_node.to_html()
        self.assertEqual(string, "<p>paragraph text</p>")
                          
    def test_value_required_leaf(self):
        leaf_node = LeafNode("p", None)
        with self.assertRaises(ValueError) as context:
            leaf_node.to_html()
        self.assertTrue("value is required" in str(context.exception))

    def test_tag_none_leaf(self):
        leaf_node = LeafNode(None, "heading #1")
        self.assertEqual(leaf_node.to_html(), "heading #1")

    def test_repr_parent(self):
        child_node1 = LeafNode("b", "Bold text")
        child_node2 = LeafNode(None, "Normal text")
        parent_node = ParentNode("p", [child_node1, child_node2],)
        self.assertEqual(repr(parent_node), "ParentNode(p, children: [LeafNode(b, Bold text, None), LeafNode(None, Normal text, None)], None)")

    def tag_required_parent(self):
        child_node = LeafNode("b", "Bold text")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertTrue("tag is required" in str(context.exception))
    
    def test_children_require_parent(self):
        parent_node = ParentNode("p", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertTrue("children value is required" in str(context.exception))

    def test_to_html_child(self):
        child_node = LeafNode("p", "paragraph text")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><p>paragraph text</p></div>")

    def test_to_html_many_children(self):
        child_node1 = LeafNode("b", "Bold text")
        child_node2 = LeafNode(None, "Normal text")
        child_node3 = LeafNode("i", "italic text")
        child_node4 = LeafNode(None, "Normal text")
        parent_node = ParentNode("p", [child_node1, child_node2, child_node3, child_node4])
        self.assertEqual(parent_node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_grandchild(self):
        grandchild_node = LeafNode("p", "paragraph text")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><p>paragraph text</p></span></div>")

    '''
    def test_parent_value_given(self):
        node = ParentNode("p", value="paragraph text", children=[LeafNode("b", "Bold text")])
        with self.assertRaises(TypeError) as context:
            node.__init__()
        self.assertTrue("ParentNode.__init__() got an unexpected keyword argument 'value'" in str(context.exception))
    '''

if __name__ == "__main__":
    unittest.main()