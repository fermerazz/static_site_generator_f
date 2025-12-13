from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

def test_split_bold():
    node = TextNode("Hello **world**!", TextType.TEXT)
    result = split_nodes_delimiter([node], "**", TextType.BOLD)
    assert len(result) == 3
    assert result[0].text == "Hello "
    assert result[0].text_type == TextType.TEXT
    assert result[1].text == "world"
    assert result[1].text_type == TextType.BOLD
    assert result[2].text == "!"
    assert result[2].text_type == TextType.TEXT
    print("test_split_bold passed")

def test_split_code():
    node = TextNode("Use `print()`.", TextType.TEXT)
    result = split_nodes_delimiter([node], "`", TextType.CODE)
    assert len(result) == 3
    assert result[1].text == "print()"
    assert result[1].text_type == TextType.CODE
    print("test_split_code passed")

def test_no_delimiters():
    node = TextNode("No special here.", TextType.TEXT)
    result = split_nodes_delimiter([node], "**", TextType.BOLD)
    assert len(result) == 1
    assert result[0].text == "No special here."
    assert result[0].text_type == TextType.TEXT
    print("test_no_delimiters passed")

def test_unclosed_delimiter():
    node = TextNode("Oops **not closed", TextType.TEXT)
    try:
        split_nodes_delimiter([node], "**", TextType.BOLD)
    except Exception as e:
        assert "unclosed delimiter" in str(e)
        print("test_unclosed_delimiter passed")
    else:
        print("test_unclosed_delimiter failed")

test_split_bold()
test_split_code()
test_no_delimiters()
test_unclosed_delimiter()