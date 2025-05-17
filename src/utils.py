from htmlnode import HTMLNode, text_node_to_html_node, LeafNode
from blocktype import block_to_block_type, BlockType
from src.htmlnode import ParentNode
from textnode import TextType, TextNode
import re


def markdown_to_html_node(markdown):
    """
    Convert Markdown text to HTML node.
    """
    children = []
    tags = {
        BlockType.PARAGRAPH: "p",
        BlockType.HEADING: "h1",
        BlockType.CODE: "pre",
        BlockType.QUOTE: "blockquote",
        BlockType.UNORDERED_LIST: "ul",
        BlockType.ORDERED_LIST: "ol",
    }

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.CODE:
            block = block[3:-3].lstrip()
            block_children = [LeafNode("code", block)]
        else:
            block = block.replace("\n", " ")
            block_children = block_to_html_nodes(block)
        children.append(ParentNode(tags[block_type], block_children))

    return ParentNode("div", children)


def block_to_html_nodes(block):
    text_nodes = text_to_textnodes(block)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def markdown_to_blocks(markdown):
    ret = []
    block = ""
    for line in markdown.split("\n"):
        line = line.strip()
        if not line:
            if block:
                ret.append(block)
                block = ""
            continue
        if block:
            block += "\n"
        block += line
    if block:
        ret.append(block)
    return ret


def text_to_textnodes(text):
    ret = [TextNode(text, TextType.TEXT)]
    ret = split_nodes_delimiter(ret, "**", TextType.BOLD)
    ret = split_nodes_delimiter(ret, "_", TextType.ITALIC)
    ret = split_nodes_delimiter(ret, "`", TextType.CODE)
    ret = split_nodes_link(ret)
    ret = split_nodes_image(ret)
    return ret


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    ret = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            ret.append(old_node)
            continue
        parts = old_node.text.split(delimiter)
        for i, part in enumerate(parts):
            if i % 2 == 0:
                ret.append(TextNode(part, TextType.TEXT))
            else:
                ret.append(TextNode(part, text_type))
    return ret


def split_nodes_image(old_nodes):
    ret = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            ret.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        parts = split_images_from_text(old_node.text, images)
        for part in parts:
            if isinstance(part, str):
                ret.append(TextNode(part, TextType.TEXT))
            else:
                ret.append(TextNode(part[0], TextType.IMAGE, part[1]))
    return ret


def split_images_from_text(text, images):
    ret = []
    remaining = text
    for alt, url in images:
        img = f"![{alt}]({url})"
        idx = remaining.find(img)
        if idx == -1:
            continue
        if idx > 0:
            ret.append(remaining[:idx])
        ret.append((alt, url))
        remaining = remaining[idx+len(img):]
    if remaining:
        ret.append(remaining)
    return ret


def split_nodes_link(old_nodes):
    ret = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            ret.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        parts = split_links_from_text(old_node.text, links)
        for part in parts:
            if isinstance(part, str):
                ret.append(TextNode(part, TextType.TEXT))
            else:
                ret.append(TextNode(part[0], TextType.LINK, part[1]))
    return ret


def split_links_from_text(text, links):
    ret = []
    remaining = text
    for txt, url in links:
        link = f"[{txt}]({url})"
        idx = remaining.find(link)
        if idx == -1:
            continue
        if idx > 0:
            ret.append(remaining[:idx])
        ret.append((txt, url))
        remaining = remaining[idx+len(link):]
    if remaining:
        ret.append(remaining)
    return ret


def extract_markdown_images(text):
    pattern = r"!\[([^]]+)\]\(([^)]+)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r"\[([^]]+)\]\(([^)]+)\)"
    return re.findall(pattern, text)
