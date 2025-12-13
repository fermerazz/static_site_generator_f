import os
from markdown_blocks import markdown_to_html_node 
from htmlnode import HTMLNode
from inline_markdown import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        from_contents = f.read()
    with open(template_path, "r") as f:
        temp_contents = f.read()

    #from_contents is the markdown file
    html_contents = markdown_to_html_node(from_contents).to_html()
    title = extract_title(from_contents)

    temp_contents = temp_contents.replace("{{ Title }}", title)
    temp_contents = temp_contents.replace("{{ Content }}", html_contents)

    dir_path = os.path.dirname(dest_path)
    if dir_path != "":
        os.makedirs(dir_path, exist_ok=True)
        
    with open(dest_path, "w") as f:
        f.write(temp_contents)