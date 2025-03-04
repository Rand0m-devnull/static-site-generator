import re
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    if delimiter == "":
            return old_nodes   
      
    for node in old_nodes:
        # If node is not NORMAL type, add it unchanged
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue   
        
        # Check for matching delimiters
        # Even indexes (0, 2, 4) always will be NORMAL text
        # Odd indexes (1, 3, 5) always will be special TextType (italic/bold/code)
        parts_nodes = []

        text = node.text
        parts = text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Matching delimiter pair not found for {delimiter}")
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                parts_nodes.append(TextNode(parts[i], TextType.NORMAL))
            else:
                parts_nodes.append(TextNode(parts[i], text_type))

        new_nodes.extend(parts_nodes)
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
       
    for node in old_nodes:
        node_text = node.text
        parts_nodes = []

        matches = extract_markdown_images(node_text)
        if not matches:
            new_nodes.append(node)
            continue
        for i in range(len(matches)):
            if matches[i] == "":
                continue
            image_alt = matches[i][0]
            image_url = matches[i][1]
           
            sections = node_text.split(f"![{image_alt}]({image_url})", 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image not closed properly")
            if sections[0] != "":
                parts_nodes.append(TextNode(sections[0], TextType.NORMAL))
            
            parts_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
           
            node_text = sections[1]
        
        if node_text != "":
            parts_nodes.append(TextNode(node_text, TextType.NORMAL))
        
        new_nodes.extend(parts_nodes)
    return new_nodes     
        
def split_nodes_link(old_nodes):
    new_nodes = []
       
    for node in old_nodes:
        node_text = node.text
        parts_nodes = []

        matches = extract_markdown_links(node_text)
        if not matches:
            new_nodes.append(node)
            continue
        for i in range(len(matches)):
            if matches[i] == "":
                continue
            anchor = matches[i][0]
            link_url = matches[i][1]
           
            sections = node_text.split(f"[{anchor}]({link_url})", 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link not closed properly")
            if sections[0] != "":
                parts_nodes.append(TextNode(sections[0], TextType.NORMAL))
            
            parts_nodes.append(TextNode(anchor, TextType.LINK, link_url))
           
            node_text = sections[1]
        
        if node_text != "":
            parts_nodes.append(TextNode(node_text, TextType.NORMAL))
       
        new_nodes.extend(parts_nodes)
    return new_nodes

def text_to_textnodes(text):    
    nodes = [TextNode(text, TextType.NORMAL, None)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes) 
   
    return nodes
