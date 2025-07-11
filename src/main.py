from tkinter import Tk
from ui import ui

window: Tk | None = None


def main():
    global window
    window = Tk()
    window.title("Floor Browse")
    window.geometry("850x480")

    ui(window)

    window.mainloop()


if __name__ == "__main__":
    main()
