from htmlnode import HTMLNode
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
    if re.search(r"^#{1,6}\s", block):
        return BlockType.HEADING
    if re.search(r"^`{3}\n", block) and re.search(r"\n`{3}$", block):
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

def make_html_node(block):
    block_type = block_to_block_type(block)
    match(block_type):
        case BlockType.HEADING:
            pass
        case BlockType.CODE:
            pass
        case BlockType.QUOTE:
            pass
        case BlockType.ULIST:
            pass
        case BlockType.OLIST:
            pass
        case BlockType.PARAGRAPH:
            pass

def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    for block in blocks:
        make_html_node(block)

