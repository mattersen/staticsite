import re

from enum import Enum

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    text_blocks = markdown.split('\n\n')
    for text_block in text_blocks:
        stripped_block = text_block.strip()
        if len(stripped_block) == 0:
            continue
        else:
            blocks.append(stripped_block)    
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
    i = 1
    split_block = block.split("\n")
    for line in split_block:
        if not line.startswith(f"{i}. "):
            return False
        i += 1
    return True 