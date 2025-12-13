from enum import Enum

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in blocks:
        clean_block = block.strip()
        lines = clean_block.split("\n")
        stripped_lines = [line.strip() for line in lines]
        clean_block = "\n".join(stripped_lines)
        if clean_block != "":
            clean_blocks.append(clean_block)
    return clean_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")
    first_line = lines[0]
    #Code 
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    #Heading 
    count = 0
    for ch in first_line:
        if ch == "#":
            count += 1
        else:
            break
    if (
        1 <= count <= 6
        and len(first_line) > count
        and first_line[count] == " "
    ):
        return BlockType.HEADING
    #Quotes
    all_quote = True
    for line in lines:
        if not line.startswith(">"):
            all_quote = False
            break
    if all_quote:
        return BlockType.QUOTE
    #Unordered List
    all_unordered = True
    for line in lines:
        if not line.startswith("- "):
            all_unordered = False
            break
    if all_unordered:
        return BlockType.UNORDERED_LIST
    #Ordered List
    all_ordered = True
    expected = 1
    for line in lines:
        if ". " not in line:
            all_ordered = False
            break
        num_str, rest = line.split(". ", 1)
        if not num_str.isdigit():
            all_ordered = False
            break
        if int(num_str) != expected:
            all_ordered = False
            break
        expected += 1
    if all_ordered:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

    
