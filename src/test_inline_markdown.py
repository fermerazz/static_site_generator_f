import unittest
from textnode import TextType, TextNode
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, extract_title
from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node


class TestInlineMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_multiple_img(self):
        matches = extract_markdown_images(
            "Here's ![img1](url1) and ![img2](url2)"
        )
        self.assertListEqual([("img1", "url1"), ("img2", "url2")], matches)

    def test_extract_markdown_images_no_img(self):
        matches = extract_markdown_images(
            "Just plain text with no images"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty_alt(self):
        matches = extract_markdown_images(
            "An image with no alt: ![](https://example.com/pic.png)"
        )
        self.assertListEqual([("", "https://example.com/pic.png")], matches)

    def test_extract_makrdown_links(self):
        matches = extract_markdown_links(
        "This is a text with a link [to the best coding platform](https://www.boot.dev)"
        )
        self.assertListEqual([("to the best coding platform", "https://www.boot.dev")], matches)

    def test_extract_makrdown_links_multiple(self):
        matches = extract_markdown_links(
            "Link [one](url1) and [two](url2)"
        )
        self.assertListEqual([("one", "url1"), ("two", "url2")], matches)
    
    def test_extract_makrdown_links_no_links(self):
        matches = extract_markdown_links(
            "No links at all"
        )
        self.assertListEqual([], matches)

    def test_extract_makrdown_links_mix(self):
        matches = extract_markdown_links(
            "A link [click here](https://url.com) and an image ![pic](https://img.jpg)"
        )
        self.assertListEqual([("click here", "https://url.com")], matches)
    
    def test_extract_markdown_links_empty_anchor(self):
        matches = extract_markdown_links(
           "[](https://example.com)" 
        )
        self.assertListEqual([("", "https://example.com")], matches)
                            
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
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_image_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual([node], result)

    def test_split_image_only_image(self):
        node = TextNode("![alt](http://example.com/img.png)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("alt", TextType.IMAGE, "http://example.com/img.png")],
            result,
        )
    def test_split_image_at_start(self):
        node = TextNode(
            "![alt](http://example.com/img.png) then text",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("alt", TextType.IMAGE, "http://example.com/img.png"),
                TextNode(" then text", TextType.TEXT),
            ],
            result,
        )
    def test_split_link_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual([node], result)
    
    def test_split_link_single(self):
        node = TextNode(
            "Go to [Boot.dev](https://www.boot.dev) now",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" now", TextType.TEXT),
            ],
            result,
        )
    def test_split_link_multiple(self):
        node = TextNode(
            "Links: [One](http://one.com) and [Two](http://two.com)",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Links: ", TextType.TEXT),
                TextNode("One", TextType.LINK, "http://one.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("Two", TextType.LINK, "http://two.com"),
            ],
            result,
        )
    def test_text_to_textnode(self):
        text = "Hello world!"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("Hello world!", TextType.TEXT)
            ],
            result
        )
    def test_text_to_textnode_bold(self):
        text = "this is **bold** text"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT)
            ],
            result
        )
    def test_text_to_textnode_mix(self):
        text = "this is _italic_ and `code`"
        result = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE)
            ],
            result
            )
class TestBlockMarkdown(unittest.TestCase):

        def test_markdown_to_blocks(self):
            md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
        def test_block_to_block_type_paragraph(self):
            block = "This is just a paragraph"
            self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        def test_block_to_block_type_heading(self):
            block = "## A heading"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        def test_block_to_block_type_code(self):
            block = "```This is code```"
            self.assertEqual(block_to_block_type(block), BlockType.CODE)

        def test_block_to_block_type_quote(self):
            block = "> This is a quote\n> This is another quote"
            self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        def test_block_to_block_type_ordered(self):
            block = "1. Hello\n2. World"
            self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        def test_paragraphs(self):
            md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )

        def test_codeblock(self):
            md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(
                html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            )
        def test_extract_title(self):
            md = "# This is an h1 title"
            self.assertEqual(extract_title(md), "This is an h1 title")
        
        def test_extract_title_no_title(self):
            md = "This is just plain text"
            self.assertRaises(Exception,extract_title, md)