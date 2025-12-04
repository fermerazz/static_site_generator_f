from textnode import TextNode, TextType

def main():
    node = TextNode("Hello darkness my old friend", TextType.TEXT, "https://www.boot.dev")
    print(node)

main()