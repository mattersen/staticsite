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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        image_tuples = extract_markdown_images(node.text)
        # If there are no images, return this node and continue
        if not image_tuples:
            new_nodes.append(node)
            continue
        working_text = node.text
        for tuple in image_tuples:
            formatted_link_text = f"![{tuple[0]}]({tuple[1]})"
            sections = working_text.split(formatted_link_text, 1)
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(tuple[0], TextType.IMAGE, tuple[1]))
            working_text = sections[1]
        if len(working_text) > 0:
            new_nodes.append(TextNode(working_text, TextType.TEXT))
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        link_tuples = extract_markdown_links(node.text)
        # If there are no images, return this node and continue
        if not link_tuples:
            new_nodes.append(node)
            continue
        working_text = node.text
        for tuple in link_tuples:
            formatted_link_text = f"[{tuple[0]}]({tuple[1]})"
            sections = working_text.split(formatted_link_text, 1)
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(tuple[0], TextType.LINK, tuple[1]))
            working_text = sections[1]
        if len(working_text) > 0:
            new_nodes.append(TextNode(working_text, TextType.TEXT))
    return new_nodes