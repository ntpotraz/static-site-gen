import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    
    def test_print_htmlnode(self):
        test = HTMLNode("p", "Test content", {"href": "google.com", "target": "_blank"})
        self.assertEqual(test.__repr__(), "HTMLNode(p, Test content, {'href': 'google.com', 'target': '_blank'}, None)")

    def test_props_to_html(self):
        test = HTMLNode("p", "Test content", None, {"href": "google.com", "target": "_blank"})
        self.assertEqual(test.props_to_html(), ' href="google.com" target="_blank"')

    def test_eq(self):
        test = HTMLNode("p", "Test content", None, {"href": "google.com", "target": "_blank"})
        test2 = HTMLNode("p", "Test content", None, {"href": "google.com", "target": "_blank"})
        self.assertEqual(test, test2)
