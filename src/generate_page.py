import os
from pathlib import Path
from markdown_blocks import markdown_to_HTMLNode

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("Title not found")

def generate_pages_recursive(dir_path_content, template_path, dst_dir_path):
    for filename in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, filename)
        dst_path = os.path.join(dst_dir_path, filename)
        if os.path.isfile(src_path):
            dst_path = Path(dst_path).with_suffix(".html")
            generate_page(src_path, template_path, dst_path)
        else:
            generate_pages_recursive(src_path, template_path, dst_path)

def generate_page(src_path, template_path, dst_path):
    with open(src_path, "r") as src_file:
        markdown_content = src_file.read()

    with open(template_path, "r") as template_file:
        template = template_file.read()
        template_file.close()

    node = markdown_to_HTMLNode(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dst_dir_path = os.path.dirname(dst_path)
    if dst_dir_path != "":
        os.makedirs(dst_dir_path, exist_ok=True)
    to_file = open(dst_path, "w")
    to_file.write(template)
