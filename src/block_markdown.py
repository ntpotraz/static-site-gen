from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node
from inline_markdown import text_to_textnodes
from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph",
    HEADING = "heading",
    CODE = "code",
    QUOTE = "quote",
    ULIST = "unordered_list",
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filteredblocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filteredblocks.append(block)
    return filteredblocks

def block_to_block_type(block):
    print(f"{type(block)} block: {block}")
    if re.search(r"^#{1,6}\s", block):
        return BlockType.HEADING
    if re.search(r"^\n?```\n?", block) and re.search(r"\n?```$", block):
        return BlockType.CODE
    if re.search(r"^>", block):
        lines = block.split("\n")
        if len(lines) == 1:
            return BlockType.QUOTE
        for line in lines:
            if not re.search(r"^>", line):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if re.search(r"^-\s", block):
        lines = block.split("\n")
        if len(lines) == 1:
            return BlockType.ULIST
        for line in lines:
            if not re.search(r"^-\s", block):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if re.search(r"^\d+\.", block):
        lines = block.split("\n")
        if len(lines) == 1:
            return BlockType.OLIST
        for line in lines:
            if not re.search(r"^\d+\.", line):
                return BlockType.PARAGRAPH
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def create_html_nodes(content):
    text_nodes = text_to_textnodes(content)
    html_nodes = []
    for text_node in text_nodes:
        node = text_node_to_html_node(text_node)
        html_nodes.append(node)
    return html_nodes

def create_heading_html(block):
    value = block.count("#")
    content = block.replace("#", "").strip()
    html_nodes = create_html_nodes(content)
    return ParentNode(f"h{value}", html_nodes)

def create_code_html(block):
    print("IN CODE")
    open, value, close = block.split("```")
    code = LeafNode("code", value.lstrip())
    return ParentNode("pre", [code])

def create_quote_html(block):
    quoteless = re.split(r"\n>", block)
    quoteless[0] = quoteless[0].replace(" ", "", 1)[1:]
    nodes = []
    for section in quoteless:
        html_node = create_html_nodes(section)
        nodes.extend(html_node)
    return ParentNode("blockquote", nodes)

def create_ul_html(block):
    sections = block.split("\n- ")
    sections[0] = sections[0][2:]
    list_nodes = []
    for section in sections:
        text_node = create_html_nodes(section)
        list_node =  ParentNode("li", text_node)
        list_nodes.append(list_node)
    return ParentNode("ul", list_nodes)

def create_ol_html(block):
    sections = re.split(r"\n\d\.\s", block)
    sections[0] = sections[0][3:]
    list_nodes = []
    for section in sections:
        text_node = create_html_nodes(section)
        list_node =  ParentNode("li", text_node)
        list_nodes.append(list_node)
    return ParentNode("ol", list_nodes)

def create_p_html(block):
    content = block.replace("\n", " ")
    html_nodes = create_html_nodes(content)
    return ParentNode(f"p", html_nodes)


def make_html_node(block):
    block_type = block_to_block_type(block)
    match(block_type):
        case BlockType.HEADING:
            return create_heading_html(block)
        case BlockType.CODE:
            return create_code_html(block)
        case BlockType.QUOTE:
            return create_quote_html(block)
        case BlockType.ULIST:
            return create_ul_html(block)
        case BlockType.OLIST:
            return create_ol_html(block)
    return create_p_html(block)

def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    #print(f"blocks {blocks}")
    nodes = []
    for block in blocks:
        nodes.append(make_html_node(block))
    return ParentNode("div", nodes)

