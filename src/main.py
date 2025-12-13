from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType
from copystatic import copy_static


        
def main():
    node = TextNode("Hello darkness my old friend", TextType.TEXT, "https://www.boot.dev")
    print(node)

main()