from textnode import TextType

class HTMLNode:
    
    def __init__(self, 
            tag=None, 
            value=None, 
            children=None, 
            props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""
        ret = ""
        for key, value in self.props.items():
            ret += f" {key}=\"{value}\""
        return ret

    def __repr__(self):
        ret = "HTMLNode:\n"
        if self.tag:
            ret += f"\ttag={self.tag}\n"
        if self.value:
            ret += f"\tvalue={self.value}\n"
        if self.children:
            ret += f"\tchildren:\n"
            for child in self.children:
                ret += child.__repr__()
        if self.props:
            ret += f"\tprops:\n"
            for key, value in self.props.items():
                ret += f"\t\t{key}={value}\n"
        return ret

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
       if self.value is None:
           raise ValueError
       if self.tag is None:
           return f"{self.value}"
       props = self.props_to_html()
       if self.tag == "img":
           # img tags are self-closing
           return f"<{self.tag}{props}>"
       else:
           return f"<{self.tag}{props}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag must not be empty")
        if not self.children:
            raise ValueError("children must be specified")
        ret = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            ret += child.to_html()
        ret += f"</{self.tag}>"
        return ret
    

def text_node_to_html_node(text_node):
    tt = text_node.text_type
    if tt == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif tt == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif tt == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif tt == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif tt == TextType.LINK:
        return LeafNode("a", text_node.text, { "href": text_node.url })
    elif tt == TextType.IMAGE:
        return LeafNode("img", "", { "src": text_node.url,
                                     "alt": text_node.text })
    else:
        raise ValueError("Unsupported text type")
            
