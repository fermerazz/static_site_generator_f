import re
from textnode import TextNode, TextType

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            if not delimiter:
                raise Exception("Invalid markdown syntax")
            else:
                parts = node.text.split(delimiter)
                if len(parts) % 2 == 0:
                    raise Exception("Invalid markdown syntax: unclosed delimiter")

                for i, part in enumerate(parts):
                    if part == "":
                        continue
                    if i % 2 == 0:
                        new_nodes.append(TextNode(part, TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(part, text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
         if node.text_type != TextType.TEXT:
            new_nodes.append(node)
         elif node.text_type == TextType.TEXT:
            text = node.text
            images = extract_markdown_images(text)
            if not images:
                new_nodes.append(node)
                continue
            for alt, url in images:
                sections = text.split(f"![{alt}]({url})", 1)
                before = sections[0]
                after = sections[1]
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                text = after
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
         if node.text_type != TextType.TEXT:
            new_nodes.append(node)
         elif node.text_type == TextType.TEXT:
            text = node.text
            links = extract_markdown_links(text)
            if not links:
                new_nodes.append(node)
                continue
            for anchor, url in links:
                sections = text.split(f"[{anchor}]({url})", 1)
                before = sections[0]
                after = sections[1]
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(anchor, TextType.LINK, url))
                text = after
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text,TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes