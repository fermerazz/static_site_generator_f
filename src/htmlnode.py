
class HTMLNode:
    def __init__(self, tag=None, value=None, children= None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        lst = ''.join([f' {key}="{value}"'for key, value in self.props.items()])
        return lst
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    

class LeafNode(HTMLNode):  
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        
        props_str = ""
        if self.props:
            props_str = "".join(
                f' {key}="{value}"'for key, value in self.props.items()
            )
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Must have a tag value")
        if self.children == None:
            raise ValueError("Parent node must have at least one children")
        
        str_to_return = ""
        for children in self.children:
            to_html_str = children.to_html()
            str_to_return += to_html_str

        if self.props:
            return f"<{self.tag} {self.props_to_html()}>{str_to_return}</{self.tag}>"
        else:
            return f"<{self.tag}>{str_to_return}</{self.tag}>"