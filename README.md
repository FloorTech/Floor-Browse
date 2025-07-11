# 🌀 Floor Browse - Browse the Floor-Wide Web

**Floor Browse** is a fully custom, cross-platform Python-based web browser built with [Tkinter](https://docs.python.org/3/library/tkinter.html), a simplified custom markup language (`.tkml`), and Lua scripting for page logic.

Built by FloorTech and powered by a re-imagined version of the web.

---

### 🔃 User-Friendly Installation

**Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/FloorTech/Floor-Browse/main/installer/linux.sh | bash
```

**MacOS:**
```diff
- Official builds for MacOS are not available yet
+ You can build from the source
```

**Windows:**
```diff
- Official builds for Windows are not available yet
+ You can build from the source
```

---

## 📦 Features

- ⚡ **Fast Python runtime** using [Nuitka](https://nuitka.net/) for native binary compilation
- 🧩 **Custom Markup Language (`.tkml`)** with HTML-like syntax
- 🔧 **Dynamic Lua scripting** for real-time page interactivity
- 🪟 **Simple, embeddable GUI** using `tkinter`
- 🎨 **Lightweight styling** via tag attributes like `font-size`, `font-style`, and `foreground`
- 🧠 **Built-in standard library for Lua** to manipulate parsed DOM-like structure and more

---

## 🛠️ Getting Started

### 🔧 Prerequisites

- Python 3.12+
- [Tkinter](https://tkdocs.com/tutorial/install.html) for UI (usually comes pre-installed)
- [Nuitka](https://nuitka.net/) if compiling to binary
- [Lupa](https://pypi.org/project/lupa/) for Lua support
- `bs4` for _TKML_ support
- `requests` for page visiting support

### 🔃 Installation

Clone the repo:

```bash
git clone https://github.com/FloorTech/Floor-Browse.git
cd Floor-Browse
python3 -m venv venv
source venv/bin/activate  # Or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 🚀 Running the Browser

Run in development mode:

```bash
chmod +x ./dev.sh
./dev.sh
```

Or compile to a standalone binary using Nuitka:

```bash
chmod +x ./build.sh
./build.sh
```

---

## ✨ Writing `.tkml` Files

Configure your server to serve `.tkml` files using the `text/tkml` MIME type.

Read the [TKML Documentation](#-tkml-documentation-tkinter-markup-language) below.

---

## 🔧 Built-in Lua Standard Library

| Function                            | Description                                                                  |
| ----------------------------------- | ---------------------------------------------------------------------------- |
| `std.print(str)`                    | Logs text to console with timestamp                                          |
| `std.get(id)`                       | Finds and returns a node by its `id` attribute                               |
| `std.set_attr(std.get, key, value)` | Sets the attribute of an element and re-renders (e.g. foreground, font-size) |
| `std.set_prop(std.get, key, value)` | Sets the property of an element and re-renders (e.g. text, children)         |

---

## 📁 Project Structure

```
src/
├── client/              # Network / page visiting logic (including AST parser)
├── runtime/             # Lua runtime and bindings (including standard library)
├── ui.py                # UI setup and rendering
├── main.py              # Entry point
```

---

## 🧠 Philosophy

> "I created the site, the browser, AND the WWW redo. I. Am. Sigma."  
> — Floor Mann

This browser rethinks the web, stripping out excess and focusing on performance, simplicity, and power through Python and Lua.

---

## 🔐 License

[MIT License © FloorTech](LICENSE)

---

## 📘 TKML Documentation **_(Tkinter Markup Language)_**

**TKML** is a lightweight HTML-like markup language designed for use in the Floor Browse engine. It supports styled UI components and embedded Lua scripting to bring dynamic interactivity to your pages.

---

### 🧩 Syntax Overview

```html
<label>
  <label id="hello" font-size="2" font-style="bold" foreground="red"
    >HELO SIGMA</label
  >
  <label>I. Am. Floor. Mann.</label>
  <label>I created this site, the browser, AND the WWW redo.</label>
  <label>I. Am. Sigma.</label>

  <script lang="lua">
    local helloLabel = std.get("hello")
    std.print(helloLabel.text)
  </script>
  <script url="example.com/index.lua" lang="lua"></script>
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
- Lua has access to a built-in **standard library**, which is shown [here](#-built-in-lua-standard-library).

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
