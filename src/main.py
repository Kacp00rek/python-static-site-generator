from textnode import *
from leafnode import LeafNode
from markdown_to_html import markdown_to_html_node
import os
import shutil
import sys

PUBLIC = "docs"
STATIC = "static"
CONTENT = "content"
TEMPLATE_PATH = "template.html"

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
        if os.path.basename(src) != ".gitkeep":
            print(f"Copying: {src} -> {dst}")
            shutil.copy(src, dst)

    shutil.copytree(STATIC, PUBLIC, dirs_exist_ok=True, copy_function=copy_log)

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")

    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            return line[1:].strip()

    raise ValueError("There is no h1 header")

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        from_content = file.read()
    with open(template_path, "r") as file:
        template_content = file.read()

    html_node = markdown_to_html_node(from_content)
    html_content = html_node.to_html()
    title = extract_title(from_content)

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_content)
    template_content = template_content.replace("href=\"/", f"href=\"{basepath}")
    template_content = template_content.replace("src=\"/", f"src=\"{basepath}")

    folder_path = os.path.dirname(dest_path)
    if folder_path:
        os.makedirs(folder_path, exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(template_content)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str) -> None:
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                rel_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, rel_path)
                dest_path = dest_path.replace(".md", ".html")
                generate_page(from_path, template_path, dest_path, basepath)

def main(basepath: str) -> None:
    copy_files()
    generate_pages_recursive(CONTENT, TEMPLATE_PATH, PUBLIC, basepath)

if __name__ == "__main__":
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    main(basepath)
