from enum import Enum
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"


def markdown_to_blocks(markdown):
    # Split into lines
    lines = markdown.split('\n')
    
    # Process lines into blocks
    blocks = []
    current_block = []
    
    for line in lines:
        if line.strip() == '':
            # Empty line - if we have content in current_block, add it to blocks
            if current_block:
                blocks.append('\n'.join(current_block))
                current_block = []
        else:
            # Non-empty line - add to current block
            current_block.append(line.strip())
    
    # Don't forget the last block if there is one
    if current_block:
        blocks.append('\n'.join(current_block))
    
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if (block.startswith("# ") or
        block.startswith("## ") or
        block.startswith("### ") or
        block.startswith("#### ") or
        block.startswith("##### ") or
        block.startswith("###### ")
        ):
        return BlockType.heading   
    
    # quote - ALL lines must start with >
    all_lines_are_quotes = all(line.startswith(">") for line in lines)
    if all_lines_are_quotes:
        return BlockType.quote
    
    # unordered list
    all_lines_are_unordered = all(line.startswith("- ") for line in lines)
    if all_lines_are_unordered:
        return BlockType.unordered_list
    
    # ordered list
    is_ordered_list = True
    for i, line in enumerate(lines):
        expected_start = f"{i+1}. "
        if not line.startswith(expected_start):
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ordered_list
    
    # code
    if block.startswith("```") and block.endswith("```"):
        return BlockType.code
    
    # paragraph
    return BlockType.paragraph

def markdown_to_html_node(markdown):
    # converts a full markdown document into a single parent HTMLNode. 
    # That one parent HTMLNode should (obviously) contain many child HTMLNode objects representing the nested elements.
    blocks = markdown_to_blocks(markdown)
    child_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        
        match block_type:
            case BlockType.heading:
                child_nodes.append(header_to_html(block))
            case BlockType.code:
                child_nodes.append(code_to_html(block))
            case BlockType.quote:
                child_nodes.append(quote_to_html(block))
            case BlockType.unordered_list:
                child_nodes.append(unordered_list_to_html(block))
            case BlockType.ordered_list:
                child_nodes.append(ordered_list_to_html(block))
            case BlockType.paragraph:
                child_nodes.append(paragraph_to_html(block))
            case _:
                raise ValueError("Invalid block type")
    return ParentNode(tag="div", children=child_nodes)
        
def get_header_tag(block):
    if block.startswith("######"):
        return 6, "h6"
    elif block.startswith("#####"):
        return 5, "h5"
    elif block.startswith("####"):
        return 4, "h4"
    elif block.startswith("###"):
        return 3, "h3"
    elif block.startswith("##"):
        return 2, "h2"
    if block.startswith("#"):
        return 1, "h1"  
    else:
        raise ValueError("Too many # for a heading section / heading section doesn't exist")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    child_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        child_nodes.append(html_node)
    return child_nodes

def paragraph_to_html(block):
    child_nodes = text_to_children(" ".join(block.split("\n")))
    return ParentNode(tag="p", children=child_nodes)

def code_to_html(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    lines = block.split("\n")
    code_text = "\n".join(lines[1:-1]) + "\n"
   
    text_node = TextNode(code_text, TextType.NORMAL)
    code_node = text_node_to_html_node(text_node)
    return ParentNode(tag="pre", children=[ParentNode(tag="code", children=[code_node])])

def quote_to_html(block):
    lines = block.split("\n")
    stripped_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        stripped_lines.append(line.lstrip(">").strip())
    text = " ".join(line.strip() for line in stripped_lines).replace("  ", " ")
    child_nodes = text_to_children(text)
    return ParentNode(tag="blockquote", children=child_nodes)

def header_to_html(block):
    header_level, tag = get_header_tag(block)
    child_nodes = text_to_children(block[header_level+1:])
    return ParentNode(tag=tag, children=child_nodes)

def ordered_list_to_html(block):
    olist_items = block.split("\n")
    html_items = []
    for item in olist_items:
        text = item[3:]
        child_nodes = text_to_children(text)
        html_items.append(ParentNode(tag="li", children=child_nodes))
    return ParentNode(tag="ol", children=html_items)

def unordered_list_to_html(block):
    ulist_items = block.split("\n")
    html_items = []
    for item in ulist_items:
        text = item[2:]
        child_nodes = text_to_children(text)
        html_items.append(ParentNode(tag="li", children=child_nodes))
    return ParentNode(tag="ul", children=html_items)
