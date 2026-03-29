from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Leaf must have a value")

        openning, closing = "", ""

        if self.tag:
            openning = f"<{self.tag}{self.props_to_html()}>"
            closing = f"</{self.tag}>"

        return f"{openning}{self.value}{closing}"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
