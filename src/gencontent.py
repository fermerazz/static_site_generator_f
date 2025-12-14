import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node 
from htmlnode import HTMLNode
from inline_markdown import extract_title

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        from_contents = f.read()
    with open(template_path, "r") as f:
        temp_contents = f.read()

    #from_contents is the markdown file
    html_contents = markdown_to_html_node(from_contents).to_html()
    title = extract_title(from_contents)

    if basepath == "/":
        href_base = "/"
    else:
        href_base = basepath.rstrip("/")
        href_base = href_base + "/"

    temp_contents = temp_contents.replace("{{ Title }}", title)
    temp_contents = temp_contents.replace("{{ Content }}", html_contents)
    temp_contents = temp_contents.replace('href="/', f'href="{href_base}')
    temp_contents = temp_contents.replace('src="/', f'src="{href_base}')

    dir_path = os.path.dirname(dest_path)
    if dir_path != "":
        os.makedirs(dir_path, exist_ok=True)
        
    with open(dest_path, "w") as f:
        f.write(temp_contents)

def generate_pages_recursively(basepath, dir_path_content, template_path, dest_dir_path):
    
    for name in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, name)
        dest_path = os.path.join(dest_dir_path, name)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(basepath, from_path, template_path, dest_path)
        else:
            generate_pages_recursively(basepath, from_path, template_path, dest_path)