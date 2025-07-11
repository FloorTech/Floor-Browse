from typing import Callable
import tkinter as tk
from datetime import datetime
from lupa import LuaRuntime
from client.client_types.document import ElementNode

type RenderElementNode = Callable[[tk.Frame, ElementNode, LuaRuntime], None]

page_body: tk.Frame | None = None
saved_tree: ElementNode = {}
render_elementnode: RenderElementNode | None = None


def setup(
    SET_page_body: tk.Frame,
    SET_saved_tree: ElementNode,
    SET_render_elementnode: RenderElementNode,
):
    global page_body, saved_tree, render_elementnode
    page_body = SET_page_body
    saved_tree = SET_saved_tree
    render_elementnode = SET_render_elementnode


def std_print(text: str):
    now = datetime.now()
    print(f"[{now}] {text}")


def std_get(id: str) -> ElementNode:
    if not saved_tree:
        return {}

    def walk(node: ElementNode) -> ElementNode:
        attrs = node.get("attributes") or {}

        if attrs.get("id") == id:
            return node

        children = node.get("children") or []

        for child in children:
            found = walk(child)

            if found:
                return found

        return {}

    return walk(saved_tree)
