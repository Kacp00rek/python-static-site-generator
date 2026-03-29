from blocks import markdown_to_blocks, block_to_block_type, BlockType
from inline import text_to_textnodes
from textnode import TextNode, TextType
from leafnode import LeafNode
from htmlnode import HTMLNode
from parentnode import ParentNode

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)

    nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        tag = None
        children = None
        match block_type:
            case BlockType.HEADING:
                space = block.find(' ')
                tag = f"h{space}"
                block = block[space+1:]
                children = text_to_children(block)
            case BlockType.QUOTE:
                tag = "blockquote"
                lines = block.split("\n")
                lines = [line[2:] for line in lines]
                block = "\n".join(lines)
                children = text_to_children(block)
            case BlockType.UNORDERED_LIST:
                tag = "ul"
                lines = block.split("\n")
                lines = [line[2:] for line in lines]
                children = [ParentNode(tag="li", children=text_to_children(line)) for line in lines]
            case BlockType.ORDERED_LIST:
                tag = "ol"
                lines = block.split("\n")
                lines = [line.split(". ", 1)[1] for line in lines]
                children = [ParentNode(tag="li", children=text_to_children(line)) for line in lines]
            case BlockType.CODE:
                tag = "pre"
                block = block[4:-3]
                children = [ParentNode(tag="code", children=[ParentNode(tag=None, value=block)])]
            case BlockType.PARAGRAPH:
                tag = "p"
                children = text_to_children(block)

        nodes.append(ParentNode(tag=tag, children=children))

    return ParentNode(tag="div", children=nodes)

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    return html_nodes

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
