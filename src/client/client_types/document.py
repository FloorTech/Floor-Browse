from typing import TypedDict, List, Optional, Union
from bs4 import BeautifulSoup, Tag, NavigableString


class ElementNode(TypedDict, total=False):
    type: str
    attributes: Optional[dict[str, str]]
    text: Optional[str]
    children: Optional[List["ElementNode"]]


class Document:
    raw = ""
    tree: ElementNode = {}

    def __init__(self, raw: str):
        self.raw = raw

    def parse(self):
        soup = BeautifulSoup(self.raw, "html.parser")

        def walk(node: Union[Tag, NavigableString]) -> Optional[ElementNode]:
            if isinstance(node, NavigableString):
                text = node.strip()
                return {"type": "text", "text": text} if text else None

            children: list[ElementNode] = []
            text_content = ""

            for child in node.children:
                if isinstance(child, NavigableString):
                    stripped = child.strip()

                    if stripped:
                        text_content += stripped + " "
                elif isinstance(child, Tag):
                    parsed = walk(child)

                    if parsed:
                        children.append(parsed)

            element: ElementNode = {"type": node.name}
            element["attributes"] = node.attrs

            if text_content.strip():
                element["text"] = text_content.strip()
            if children:
                element["children"] = children

            return element

        body = soup.body or soup
        self.tree = walk(body) or {}

        return self
