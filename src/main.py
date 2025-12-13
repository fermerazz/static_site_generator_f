from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

def text_to_children(text):
    nodes = text_to_textnodes(text)
    converted_nodes = []
    for node in nodes:
        converted_nodes.append(text_node_to_html_node(node))
    return converted_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            lines = block.split("\n")
            paragraph_text = " ".join(lines)
            p_children = text_to_children(paragraph_text)
            p_node = ParentNode("p", p_children)
            children.append(p_node)
        if block_type == BlockType.HEADING:
            level = 0
            for ch in block:
                if ch == "#":
                    level += 1
                else:
                    break
            if level + 1 >= len(block):
                raise ValueError(f"invalid heading level: {level}")
            heading_text = block[level + 1:]
            h_children = text_to_children(heading_text)
            h_node = ParentNode(f"h{level}", h_children)
            children.append(h_node)
        if block_type == BlockType.CODE:
            if not block.startswith("```") or not block.endswith("```"):
                raise ValueError("invalid code block")
            text = block[4:-3]
            raw_text_node = TextNode(text, TextType.TEXT)
            child = text_node_to_html_node(raw_text_node)
            code_node = ParentNode("code", [child])
            pre_node = ParentNode("pre", [code_node])
            children.append(pre_node)
        if block_type == BlockType.UNORDERED_LIST:
            items = block.split("\n")
            li_nodes = []
            for item in items:
                text = item[2:]
                li_children = text_to_children(text)
                li_nodes.append(ParentNode("li", li_children))
            ul_node = ParentNode("ul", li_nodes)
            children.append(ul_node)
        if block_type == BlockType.ORDERED_LIST:
            items = block.split("\n")
            li_nodes = []
            for item in items:
                text = item[3:]
                li_children = text_to_children(text)
                li_nodes.append(ParentNode("li", li_children))
            ol_node = ParentNode("ol", li_nodes)
            children.append(ol_node)
        if block_type == BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                if not line.startswith(">"):
                    raise ValueError("invalid quote block")
                new_lines.append(line.lstrip(">").strip())
            content = " ".join(new_lines)
            q_children = text_to_children(content)
            q_node = ParentNode("blockquote", q_children)
            children.append(q_node)
    return ParentNode("div", children)
        
def main():
    node = TextNode("Hello darkness my old friend", TextType.TEXT, "https://www.boot.dev")
    print(node)

main()