from typing import Any
import json
import requests
import tkinter as tk
import settings
from lupa import LuaRuntime
from client.visit import visit_page
from client.client_types.document import ElementNode
import runtime.lua_standard_lib as lua_standard_lib


page_body: tk.Frame | None = None
saved_tree: ElementNode = {}
rendered_widgets: dict[str, tk.Widget] = {}


def clone_widget(widget: tk.Widget) -> tk.Widget:
    cls = widget.__class__
    parent = widget.master

    config = {key: widget.cget(key) for key in widget.keys()}
    new_widget = cls(parent, **config)
    pack_info = widget.pack_info() if widget.winfo_manager() == "pack" else None

    if pack_info:
        new_widget.pack(**pack_info)

    grid_info = widget.grid_info() if widget.winfo_manager() == "grid" else None

    if grid_info:
        new_widget.grid(**grid_info)

    return new_widget


def open_devtools(tree: ElementNode):
    devtools = tk.Toplevel()
    devtools.title("Dev Tools - Document Tree")
    devtools.geometry("850x480")

    text_area = tk.Text(
        devtools, wrap="word", bg="#111", fg="#0f0", insertbackground="#0f0"
    )
    text_area.pack(fill=tk.BOTH, expand=True)

    tree_string = json.dumps(tree, indent=2)
    text_area.insert("1.0", tree_string)
    text_area.config(state=tk.DISABLED)


def render_elementnode(parent: tk.Widget, node: ElementNode, lua_runtime: LuaRuntime):
    node_type = node.get("type")
    continue_render = True

    match node_type:
        case "[document]":
            children = node.get("children") or []
            render_elementnode(parent, children[0], lua_runtime)
            continue_render = False
        case "label":
            text = node.get("text") or ""
            attrs = node.get("attributes") or {}
            label = tk.Label(
                parent,
                text=text,
                anchor="w",
                justify="left",
                font=(
                    attrs.get("font-family") or "Arial",
                    int(float(attrs.get("font-size") or "1") * settings.BASE_FONT_SIZE),
                    attrs.get("font-style") or "normal",
                ),
                foreground=(attrs.get("foreground") or settings.FOREGROUND_COLOR),
                background=(attrs.get("background") or settings.BACKGROUND_COLOR),
            )
            label.pack(padx=10, pady=10, fill=tk.X)
            element_id = attrs.get("id")

            if element_id:
                rendered_widgets[element_id] = label
        case "script":
            text = node.get("text") or ""
            attrs = node.get("attributes") or {}

            if attrs.get("url") is not None:
                req_url = attrs.get("url", "")

                if not req_url.startswith("http"):
                    req_url = f"http://{req_url}"

                req = requests.get(req_url)
                text = req.text

            if attrs.get("lang") == "lua":
                try:
                    lua_runtime.execute(text)
                except Exception as error:
                    print("Could not finish executing lua script(s)!", error)
        case _:
            new_node = node.copy()
            new_node["type"] = "label"
            render_elementnode(parent, new_node, lua_runtime)
            continue_render = False

    if continue_render and node.get("children"):
        children = node.get("children") or []

        for child in children:
            render_elementnode(parent, child, lua_runtime)


def visit(url_bar: tk.Entry):
    global saved_tree
    entered_url = url_bar.get()

    if not entered_url.startswith("http"):
        entered_url = "http://" + entered_url

    url_bar.delete(0, tk.END)
    url_bar.insert(0, entered_url)
    tree = visit_page(entered_url).tree
    saved_tree = tree

    if page_body:
        for widget in page_body.winfo_children():
            widget.destroy()

        lua_standard_lib.setup(page_body, saved_tree, render_elementnode)
        lua_runtime = LuaRuntime()

        def std_set_attr(element: ElementNode, key: str, value: str) -> None:
            attrs = element.setdefault("attributes", {}) or {}
            attrs[key] = value
            element_id = attrs.get("id")

            if element_id:
                old_widget = rendered_widgets.get(element_id)

                if not old_widget:
                    return

                parent = old_widget.master
                siblings = parent.pack_slaves()
                index = siblings.index(old_widget)

                cls = old_widget.__class__
                config = {key: old_widget.cget(key) for key in old_widget.keys()}
                new_widget = cls(parent, **config)

                old_widget.destroy()

                if index < len(siblings) - 1:
                    new_widget.pack(
                        before=siblings[index + 1], padx=10, pady=10, fill=tk.X
                    )
                else:
                    new_widget.pack(padx=10, pady=10, fill=tk.X)

                render_elementnode(new_widget, element, lua_runtime)
                rendered_widgets[element_id] = new_widget

        def std_set_prop(element: ElementNode, key: str, value: Any) -> None:
            element[key] = value
            attrs = element.get("attributes", {}) or {}
            element_id = attrs.get("id")

            if element_id:
                old_widget = rendered_widgets.get(element_id)

                if not old_widget:
                    return

                parent = old_widget.master
                siblings = parent.pack_slaves()
                index = siblings.index(old_widget)

                cls = old_widget.__class__
                config = {key: old_widget.cget(key) for key in old_widget.keys()}
                new_widget = cls(parent, **config)

                old_widget.destroy()

                if index < len(siblings) - 1:
                    new_widget.pack(
                        before=siblings[index + 1], padx=10, pady=10, fill=tk.X
                    )
                else:
                    new_widget.pack(padx=10, pady=10, fill=tk.X)

                render_elementnode(new_widget, element, lua_runtime)
                rendered_widgets[element_id] = new_widget

        lua_globals = lua_runtime.globals()
        lua_globals.std = {  # type: ignore
            "print": lua_standard_lib.std_print,
            "get": lua_standard_lib.std_get,
            "set_attr": std_set_attr,
            "set_prop": std_set_prop,
        }

        render_elementnode(page_body, tree, lua_runtime)
        page_body.focus()


def url_box(window: tk.Tk):
    url_box = tk.Frame(window, height=30, background="#ccc")
    url_box.pack(padx=10, pady=5, fill=tk.X)

    url_bar = tk.Entry(url_box)
    url_bar.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
    url_bar.bind("<KeyRelease-Return>", lambda event: visit(url_bar))
    url_bar.focus()

    visit_btn = tk.Button(url_box, text="Visit", command=lambda: visit(url_bar))
    visit_btn.grid(row=0, column=1, sticky="nsew")

    url_box.grid_columnconfigure(0, weight=1)


def body(window: tk.Tk):
    global page_body
    page_body = tk.Frame(window, background=settings.BACKGROUND_COLOR)
    page_body.pack(fill=tk.BOTH, expand=True)


def ui(window: tk.Tk):
    url_box(window)
    body(window)
    window.bind("<F12>", lambda event: open_devtools(saved_tree))
