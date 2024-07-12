import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        else:
            split_parts = old_node.text.split(delimiter)
            if len(split_parts) % 2 == 0:
                raise Exception(f"Unmatched delimiter found in text: {old_node.text}")
            continue
    for i, part in enumerate(split_parts):
                if part:  # Ensure non-empty strings
                    if i % 2 == 0:
                        new_nodes.append(TextNode(part, text_type_text, old_node.url))
                    else:
                        new_nodes.append(TextNode(part, text_type, old_node.url))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        node_text = old_node.text
        images = extract_markdown_images(node_text)
        last_pos = 0

        for desc, url in images:
            pattern = re.escape(f"![{desc}]({url})")
            match = re.search(pattern, node_text[last_pos:])
            if match:
                start, end = match.span()
                # Append text segment before the image, if any
                if last_pos < last_pos + start:
                    new_nodes.append(TextNode(node_text[last_pos:last_pos + start], text_type_text))
                # Append the image node
                new_nodes.append(TextNode(desc, text_type_image, url))
                last_pos += end

    # Append any remaining text after the last image
        if last_pos < len(node_text):
            new_nodes.append(TextNode(node_text[last_pos:], text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        
        node_text = old_node.text
        links = extract_markdown_links(node_text)
        last_pos = 0

        for desc, url in links:
            pattern = re.escape(f"[{desc}]({url})")
            match = re.search(pattern, node_text[last_pos:])
            if match:
                start = match.start() + last_pos
                end = match.end() + last_pos
                if last_pos < start:
                    new_nodes.append(TextNode(node_text[last_pos:start], text_type_text))
                new_nodes.append(TextNode(desc, text_type_link, url))
                last_pos = end

        if last_pos < len(node_text):
            new_nodes.append(TextNode(node_text[last_pos:], text_type_text))
    return new_nodes

def extract_markdown_images(text):
    extracted = re.findall(r"![(.?)]((.?))", text)
    return extracted

def extract_markdown_links(text):
    extracted = re.findall(r"[(.?)]((.?))", text)
    return extracted