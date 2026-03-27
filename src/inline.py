from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_parts = node.text.split(delimiter)
        if len(split_parts) % 2 == 0:
            raise ValueError(f"A matching closing delimiter ({delimiter}) was not found")
        for i in range(len(split_parts)):
            if split_parts[i]:
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_parts[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_parts[i], text_type))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        images = extract_markdown_images(node_text)
        for image in images:
            sections = node_text.split(f"![{image[0]}]({image[1]})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            node_text = sections[1]

        if node_text:
            new_nodes.append(TextNode(node_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        node_text = node.text
        links = extract_markdown_links(node_text)
        for link in links:
            sections = node_text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            node_text = sections[1]

        if node_text:
            new_nodes.append(TextNode(node_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNodes]:
    nodes = [TextNode(text, TextType.TEXT)]
    delimiters = [("**", TextType.BOLD), ("`", TextType.CODE), ("_", TextType.ITALIC)]
    for delimiter, text_type in delimiters:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    regex = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(regex, text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(regex, text)
