import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os

class GuiLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visible Typing Logger — Consent Demo")
        self.log_events = []  # store (timestamp, event_type, char_or_keysym)
        self.setup_ui()

    def setup_ui(self):
        frm = ttk.Frame(self.root, padding=12)
        frm.pack(fill="both", expand=True)

        notice = ("This demo records keys only while this window is focused.\n"
                  "It does not run in background or capture system-wide keystrokes.")
        ttk.Label(frm, text=notice, wraplength=600).pack(anchor="w", pady=(0,8))

        controls = ttk.Frame(frm)
        controls.pack(fill="x", pady=(0,8))

        ttk.Label(controls, text="Log filename:").pack(side="left")
        self.filename_var = tk.StringVar(value="consensual_gui_log.txt")
        ttk.Entry(controls, textvariable=self.filename_var, width=30).pack(side="left", padx=6)
        ttk.Button(controls, text="Save Log...", command=self.save_log_dialog).pack(side="right")

        # Text widget that receives focus and text
        self.text = tk.Text(frm, height=12, wrap="word")
        self.text.pack(fill="both", expand=True)
        self.text.insert("end", "Type here (window must be focused). Press Ctrl+S to save.\n")
        self.text.focus_set()

        # Bind key events for logging
        # <KeyPress> gives event.char and event.keysym
        self.text.bind("<KeyPress>", self.on_keypress)
        # Bind Ctrl+S to save quickly
        self.root.bind_all("<Control-s>", self.on_ctrl_s)

        # bottom buttons
        btn_frame = ttk.Frame(frm)
        btn_frame.pack(fill="x", pady=(8,0))
        ttk.Button(btn_frame, text="Clear", command=self.clear).pack(side="left")
        ttk.Button(btn_frame, text="Save to file", command=self.save_log).pack(side="right")

    def on_keypress(self, event):
        # Only log when text widget/window is focused — binding on widget ensures that.
        ts = datetime.now().isoformat()
        char = event.char if event.char else ""
        key = event.keysym
        # store event: timestamp, key, char
        self.log_events.append((ts, key, char))
        # Optionally show a short indicator in the window (already showing typed text)
        return None  # let Text widget also process the key

    def format_log(self):
        lines = []
        for ts, key, char in self.log_events:
            # prefer visible char if printable, else show keysym
            display = char if char and not char.isspace() else key
            lines.append(f"{ts}\t{key}\t{repr(char)}\t{display}")
        return "\n".join(lines)

    def get_default_path(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = self.filename_var.get() or "consensual_gui_log.txt"
        base, ext = os.path.splitext(default_name)
        if not ext:
            ext = ".txt"
        fname = f"{base}_{ts}{ext}"
        return os.path.join(os.getcwd(), fname)

    def save_log_dialog(self):
        default = self.get_default_path()
        path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=os.path.basename(default))
        if path:
            self._write_log(path)
            messagebox.showinfo("Saved", f"Log saved to:\n{path}")

    def save_log(self):
        path = self.get_default_path()
        self._write_log(path)
        messagebox.showinfo("Saved", f"Log saved to:\n{path}")

    def _write_log(self, path):
        text_snapshot = self.text.get("1.0", "end-1c")
        with open(path, "w", encoding="utf-8") as f:
            f.write("=== Visible typed text (user-facing) ===\n")
            f.write(text_snapshot + "\n\n")
            f.write("=== Key events (timestamp, keysym, repr(char), display) ===\n")
            f.write(self.format_log())
        # ensure file flushed and saved

    def clear(self):
        if messagebox.askyesno("Clear", "Clear the text area and recorded events?"):
            self.text.delete("1.0", "end")
            self.log_events.clear()

    def on_ctrl_s(self, event):
        self.save_log()
        return "break"

def main():
    root = tk.Tk()
    app = GuiLoggerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
