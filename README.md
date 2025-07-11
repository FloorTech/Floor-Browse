# 🌀 Floor Browse - Browse the Floor-Wide Web

**Floor Browse** is a fully custom, cross-platform Python-based web browser built with [Tkinter](https://docs.python.org/3/library/tkinter.html), a simplified custom markup language (`.tkml`), and Lua scripting for page logic.

Built by FloorTech and powered by a re-imagined version of the web.

## 📘 TKML Documentation ***(Tkinter Markup Language)***

**TKML** is a lightweight HTML-like markup language designed for use in the Floor Browse engine. It supports styled UI components and embedded Lua scripting to bring dynamic interactivity to your pages.

---

### 🧩 Syntax Overview

```html
<label>
    <label id="hello" font-size="2" font-style="bold" foreground="red">HELO SIGMA</label>
    <label>I. Am. Floor. Mann.</label>
    <label>I created this site, the browser, AND the WWW redo.</label>
    <label>I. Am. Sigma.</label>

    <script lang="lua">
        local helloLabel = std.get("hello")
        std.print(helloLabel.text)
    </script>
</label>
```

---

### 📏 Sizing System

Any numeric value related to size (such as `font-size`) is **automatically scaled by the base font size of 16px**.  
This means:

- `font-size="1"` → `16px`
- `font-size="2"` → `32px`
- `font-size="0.75"` → `12px`

This system is equivalent to using **`rem` units**, and provides consistent scaling across the UI.

---

### 🧠 Lua Integration

TKML uses [Lua](https://lua.org) to define **page-specific interactivity**.

- All `<script lang="lua">` blocks are executed after the markup is parsed.
- Lua has access to a built-in **standard library**, including:

| Function        | Description                                      |
|----------------|--------------------------------------------------|
| `std.print(text)` | Prints to the developer log console             |
| `std.get(id)`     | Retrieves an element node by its `id` attribute |

Example:

```lua
local title = std.get("hello")
std.print(title.text)
```

---

### 📦 Root Wrapping Requirement

All `.tkml` files **must start with a single root element**, typically a `<label>` or another container element that supports children.

This design is intentional:

- Allows the renderer to treat each page as **one unified element**
- Avoids ambiguity in rendering multiple root elements
- Helps the engine detect that the file is a `.tkml` document

🗣 **Deal with it.**

---

### ✅ Example: Complete `.tkml` Document

```html
<label>
    <label id="msg" font-style="italic" foreground="blue">Hello, TKML!</label>
    <script lang="lua">
        local el = std.get("msg")
        std.print("User message: " .. el.text)
    </script>
</label>
```

---

### 📄 File Format

- File extension: `.tkml`
- Text format: UTF-8 encoded
- Parsed into an **AST** that reflects the structure and properties of all elements and text nodes.

---

### 🔒 Security Note

Lua scripts run in a **sandboxed environment**. You should still avoid running untrusted `.tkml` files from unknown sources.
