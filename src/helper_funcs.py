import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []           
        split_text_list = node.text.split(delimiter)
        if len(split_text_list) % 2 == 0:
            raise ValueError("Invalid markdown. One or more closing text delimiter(s) is missing.")
        for i in range(0, len(split_text_list)):
            if split_text_list[i] == "":
                continue
            if i % 2 == 0:                
                split_nodes.append(TextNode(split_text_list[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(split_text_list[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r'!\[([^\[\]]*)\]\(([^\(\)]*)\)', text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)', text)
    return matches