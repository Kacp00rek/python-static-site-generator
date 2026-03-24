from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("Parent must have a tag")
        if not self.children:
            raise ValueError("Parent must have children")

        openning = f"<{self.tag}{self.props_to_html()}>"
        closing = f"</{self.tag}>"
        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        return f"{openning}{children_html}{closing}"

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
