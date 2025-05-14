import re

from enum import Enum
from textnode import TextNode, TextType
from inline_markdown import text_to_textnodes
from htmlnode import HTMLNode, ParentNode

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    in_code_block = False
    lines = markdown.split("\n")
    temp_block = []
    for line in lines:
        # This is specific to code blocks
        if line == "```":
            temp_block.append(line)
            if not in_code_block:
                in_code_block = True
            else:
                blocks.append("\n".join(temp_block).strip())
                in_code_block = False
                temp_block = []
            continue
        # This is all of the other types of blocks
        if line or in_code_block:
            temp_block.append(line)
        if not line and not in_code_block and len(temp_block) > 0:
            blocks.append("\n".join(temp_block).strip())
            temp_block = []
    if len(temp_block) > 0:
        temp_var = "\n".join(temp_block).strip()
        if temp_var:
            blocks.append(temp_var)
    # text_blocks = markdown.split('\n\n')
    # for text_block in text_blocks:
    #     stripped_block = text_block.strip()
    #     if len(stripped_block) == 0:
    #         continue
    #     else:
    #         blocks.append(stripped_block)    
    return blocks

def block_to_block_type(block):
    if re.findall(r'^#{1,6}\s.+$', block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE    
    if detect_first_char(block, ">"):
        return BlockType.QUOTE
    if detect_first_char(block, "- "):
        return BlockType.UNORDERED_LIST
    if detect_ordered_list(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def detect_first_char(block, prefix):
    split_block = block.split("\n")
    for line in split_block:
        if not line.startswith(prefix):
            return False
    return True

def detect_ordered_list(block):
    split_block = block.split("\n")
    for line in split_block:
        clean = line.strip()
        if not re.match(r'^\d+\.\s', clean):
            return False
    return True

def html_node_from_block_type(text_block, block_type):
    if block_type == BlockType.PARAGRAPH:
        return ParentNode("p", text_to_textnodes(text_block))
    if block_type == BlockType.HEADING:
        num_hashes = count_header_hashes(text_block)
        remove_hashes = text_block[num_hashes:]
        return ParentNode(f"h{num_hashes}", text_to_textnodes(remove_hashes.lstrip()))
    if block_type == BlockType.QUOTE:
        removed_quote_prefixes = remove_quote_prefixes(text_block)
        return ParentNode("blockquote", text_to_textnodes(removed_quote_prefixes))
    if block_type == BlockType.UNORDERED_LIST:
        return ParentNode("ul", remove_unordered_list_prefixes(text_block))
    if block_type == BlockType.ORDERED_LIST:
        return ParentNode("ol", remove_ordered_list_prefixes(text_block))
    if block_type == BlockType.CODE:
        code_node = TextNode(remove_code_prefixes(text_block), TextType.CODE)
        leaf_node = code_node.text_node_to_html_node()
        return ParentNode("pre", [leaf_node])
    raise Exception("This is not a valid block type.")

def remove_code_prefixes(text_block):
    code_only = []
    lines = text_block.split("\n")
    for line in lines:
        if line.strip() == "```":
            continue
        else:
            code_only.append(line)
    return "\n".join(code_only)

def remove_quote_prefixes(text_block):
    lines = text_block.split("\n")
    cleaned = [line.lstrip(">").lstrip() for line in lines]
    return "\n".join(cleaned)

def remove_ordered_list_prefixes(text_block):
    cleaned_list = []
    nodes = []
    lines = text_block.split("\n")
    for line in lines:
        clean = re.sub(r'^\d+\.\s*', "", line)
        cleaned_list.append(clean)
    for clean_line in cleaned_list:
        nodes.append(ParentNode("li", text_to_textnodes(clean_line)))
    return nodes

def remove_unordered_list_prefixes(text_block):
    nodes = []
    lines = text_block.split("\n")
    cleaned = [line.lstrip("-* ") for line in lines]
    for line in cleaned:
        nodes.append(ParentNode("li", text_to_textnodes(line)))
    return nodes
    
def count_header_hashes(text_block):
    count = 0
    if text_block == "":
        return 0
    if text_block[0] != "#":
        return 0    
    for char in text_block:
        if char == "#":
            count += 1
        else:
            break
    return count

def markdown_to_html_node(markdown):
    text_blocks = markdown_to_blocks(markdown)
    all_html_blocks = []
    for text_block in text_blocks:
        block_type = block_to_block_type(text_block)
        html_node = html_node_from_block_type(text_block, block_type)
        all_html_blocks.append(html_node)
    return ParentNode("div", all_html_blocks)