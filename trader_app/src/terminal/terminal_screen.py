import tkinter as tk
import subprocess
import ctypes

BACKGROUND = "#1e1e3f"
HEADER_BG = "#2c2c5f"
TEXT_COLOR = "#ffffff"
BUTTON_COLOR = "#e0e0e0"
BORDER_RADIUS = 20

def set_rounded(root, radius=BORDER_RADIUS):
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    region = ctypes.windll.gdi32.CreateRoundRectRgn(
        0, 0, root.winfo_width()+1, root.winfo_height()+1, radius, radius
    )
    ctypes.windll.user32.SetWindowRgn(hwnd, region, True)

class RoundedTerminal:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.width, self.height = 750, 450
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.configure(bg=BACKGROUND)
        self.is_maximized = False

        self.header = tk.Frame(root, bg=HEADER_BG, height=30)
        self.header.pack(fill=tk.X)
        self.header.bind("<B1-Motion>", self.move_window)

        tk.Button(self.header, text="✕", bg=HEADER_BG, fg=BUTTON_COLOR,
                  bd=0, command=self.root.destroy).pack(side=tk.RIGHT, padx=5)
        tk.Button(self.header, text="━", bg=HEADER_BG, fg=BUTTON_COLOR,
                  bd=0, command=self.minimize).pack(side=tk.RIGHT)
        tk.Button(self.header, text="⬜", bg=HEADER_BG, fg=BUTTON_COLOR,
                  bd=0, command=self.toggle_maximize).pack(side=tk.RIGHT)

        self.terminal = tk.Text(root, wrap="word", bg=BACKGROUND, fg=TEXT_COLOR,
                                insertbackground=TEXT_COLOR, font=("Consolas", 11),
                                bd=0, relief="flat")
        self.terminal.pack(expand=True, fill=tk.BOTH, padx=10, pady=(5,10))
        self.terminal.focus_set()

        self.insert_text("Terminal iniciado. Digite seus comandos...\n> ")
        self.prompt_index = self.terminal.index("insert")

        self.terminal.bind("<Return>", self.on_enter)
        self.terminal.bind("<BackSpace>", self.on_backspace)
        self.terminal.bind("<Key>", self.on_key)
        self.terminal.bind("<MouseWheel>", self.on_mousewheel)
        self.terminal.bind("<Button-4>", self.on_mousewheel)
        self.terminal.bind("<Button-5>", self.on_mousewheel)

        self.root.after(10, lambda: set_rounded(self.root, BORDER_RADIUS))

    def insert_text(self, text):
        self.terminal.insert("end", text)
        self.terminal.see("end")

    def on_key(self, event):
        insert_index = self.terminal.index("insert")
        if self.terminal.compare(insert_index, "<", self.prompt_index):
            self.terminal.mark_set("insert", self.prompt_index)

    def on_backspace(self, event):
        if self.terminal.compare("insert", "<=", self.prompt_index):
            return "break"

    def on_enter(self, event):
        line = self.terminal.get(self.prompt_index, "end").strip()
        self.insert_text("\n")
        if line:
            self.run_command(line)
        self.insert_text("> ")
        self.prompt_index = self.terminal.index("insert")
        return "break"

    def run_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output_text = result.stdout + result.stderr
        except Exception as e:
            output_text = str(e)
        self.insert_text(output_text)

    def on_mousewheel(self, event):
        if hasattr(event, "delta"):
            self.terminal.yview_scroll(-int(event.delta/120), "units")
        elif event.num == 4:
            self.terminal.yview_scroll(-1, "units")
        elif event.num == 5:
            self.terminal.yview_scroll(1, "units")

    def move_window(self, event):
        self.root.geometry(f'+{event.x_root}+{event.y_root}')

    def minimize(self):
        self.root.iconify()

    def toggle_maximize(self):
        if self.is_maximized:
            self.root.geometry(f"{self.width}x{self.height}")
        else:
            self.root.state("zoomed")
        self.is_maximized = not self.is_maximized
