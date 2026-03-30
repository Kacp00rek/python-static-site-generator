from textnode import *
from leafnode import LeafNode
import os
import shutil

PUBLIC = "public"
STATIC = "static"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
           return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})

def copy_files() -> None:
    if os.path.exists(PUBLIC):
        print(f"Cleaning directory: {PUBLIC}")
        shutil.rmtree(PUBLIC)
    os.mkdir(PUBLIC)

    def copy_log(src, dst):
        if src != f"{STATIC}/.gitkeep":
            print(f"Copying: {src} -> {dst}")
            shutil.copy(src, dst)

    shutil.copytree(STATIC, PUBLIC, dirs_exist_ok=True, copy_function=copy_log)

def main() -> None:
    copy_files()

if __name__ == "__main__":
    main()
