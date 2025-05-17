from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    regex_heading = re.compile(r"^#{1,6}\s")

    if regex_heading.match(block):
        return BlockType.HEADING

    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE

    if every_line(block, lambda s, _: s.startswith(">")):
        return BlockType.QUOTE

    if every_line(block, lambda s, _: s.startswith("- ")):
        return BlockType.UNORDERED_LIST

    if every_line(block, is_ordered_item):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def every_line(block, pred):
    for idx, line in enumerate(block.split("\n")):
        if not pred(line, idx):
            return False
    return True

def is_ordered_item(item, idx):
    regex = re.compile(r"^(\d+)\.\s")
    m = regex.match(item)
    if not m:
        return False
    actual_num = int(m.group(1))
    return actual_num == idx + 1
