from textnode import *
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_parts = node.text.split(delimiter)
            if len(split_parts) % 2 == 0:
                raise ValueError(f"A matching closing delimiter ({delimiter}) was not found")
            for i in range(0, len(split_parts)):
                if split_parts[i]:
                    if i % 2 == 0:
                        new_nodes.append(TextNode(split_parts[i], TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(split_parts[i], text_type))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    regex = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(regex, text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(regex, text)
