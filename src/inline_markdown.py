import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise Exception("no matching delimiter")
        for i in range(len(split_node)):
            if split_node[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split_node[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_node[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"[^!]\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        if "![" not in node.text:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        node_text = node.text
        for image_alt, image_link in images:
            split = node_text.split(f"![{image_alt}]({image_link})", 1)
            node_text = split[1]
            text_node = TextNode(split[0], TextType.TEXT)
            image_node = TextNode(image_alt, TextType.IMAGE, image_link)
            if text_node.text != "":
                new_nodes.append(text_node)
            if image_node.text != "":
                new_nodes.append(image_node)
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        if " [" not in node.text:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        node_text = node.text
        for link_alt, link_link in links:
            split = node_text.split(f"[{link_alt}]({link_link})", 1)
            node_text = split[1]
            text_node = TextNode(split[0], TextType.TEXT)
            link_node = TextNode(link_alt, TextType.LINK, link_link)
            if text_node.text != "":
                new_nodes.append(text_node)
            if link_node.text != "":
                new_nodes.append(link_node)
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    bold_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    italic_bold_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    code_italic_bold_nodes = split_nodes_delimiter(italic_bold_nodes, "`", TextType.CODE)
    link_code_italic_bold_nodes = split_nodes_link(code_italic_bold_nodes)
    image_link_code_italic_bold_nodes = split_nodes_image(link_code_italic_bold_nodes)
    return image_link_code_italic_bold_nodes

