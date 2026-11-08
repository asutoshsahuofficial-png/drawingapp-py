import ctypes
import os
import sys
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, ttk

try:
    from PIL import Image, ImageDraw, ImageTk
except ModuleNotFoundError:
    print("\n" + "=" * 60)
    print("[Error] 'Pillow' is not installed in your current Python environment.")
    print("=" * 60)
    print("Please install Pillow by running:")
    print("    pip install Pillow")
    print("=" * 60 + "\n")
    sys.exit(1)

# Windows DPI Awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except (AttributeError, OSError):
    pass


class DrawingApp:
    PALETTE_COLORS = [
        "#000000", "#555555", "#e53935", "#fb8c00",
        "#fdd835", "#43a047", "#00acc1", "#1e88e5",
        "#8e24aa", "#d81b60", "#795548", "#ffffff"
    ]

    def __init__(self, root):
        self.root = root
        root.title("Simple Drawing App")
        root.geometry("1060x700")
        root.minsize(860, 560)
        root.configure(bg="#f3f4f6")

        self.tool = "Pencil"
        self.color = "#000000"
        self.bg_color = "#ffffff"
        self.size = 3

        self.start_x = self.start_y = None
        self.last_x = self.last_y = None
        self.preview = None

        # Layered Image Buffer: Transparent drawing layer composited onto background
        self.width = 1600
        self.height = 1200
        self.drawing_layer = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.drawing_layer)

        self.undo_stack = []
        self.redo_stack = []
        self.tk_canvas_img = None

        self._init_styles()
        self._build_ui()
        self._bind_shortcuts()

    def _init_styles(self):
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        self.style.configure("TFrame", background="#f3f4f6")
        self.style.configure("TLabelframe", background="#f3f4f6")
        self.style.configure("TLabelframe.Label", font=("Segoe UI", 9, "bold"), background="#f3f4f6", foreground="#1f2937")
        self.style.configure("TButton", font=("Segoe UI", 9))
        self.style.configure("Toolbutton", font=("Segoe UI", 9))
        self.style.configure("Primary.TButton", font=("Segoe UI", 9, "bold"), foreground="#0d47a1")
        self.style.configure("Danger.TButton", font=("Segoe UI", 9), foreground="#b71c1c")

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill="both", expand=True)

        # Left side: Canvas frame
        canvas_frame = ttk.Frame(main)
        canvas_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.canvas = tk.Canvas(
            canvas_frame,
            bg=self.bg_color,
            cursor="crosshair",
            highlightthickness=1,
            highlightbackground="#cbd5e1",
            bd=0,
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        # Right side: Sidebar container
        sidebar = ttk.Frame(main, width=230)
        sidebar.pack(side="right", fill="y")
        sidebar.pack_propagate(False)

        self.tool_var = tk.StringVar(value="Pencil")
        self.status = tk.StringVar()
        self.update_status()

        # ==================== 1. Primary Actions (Always at Top) ====================
        actions_group = ttk.LabelFrame(sidebar, text=" File & Actions ", padding=6)
        actions_group.pack(fill="x", pady=(0, 6))

        ttk.Button(
            actions_group, text="💾 Save Image (Ctrl+S)",
            style="Primary.TButton", command=self.save
        ).pack(fill="x", pady=2)

        action_btn_row = ttk.Frame(actions_group)
        action_btn_row.pack(fill="x", pady=2)
        ttk.Button(action_btn_row, text="↺ Undo", command=self.undo).pack(side="left", fill="x", expand=True, padx=(0, 2))
        ttk.Button(action_btn_row, text="↻ Redo", command=self.redo).pack(side="right", fill="x", expand=True, padx=(2, 0))

        ttk.Button(
            actions_group, text="🗑 Clear Canvas",
            style="Danger.TButton", command=self.clear
        ).pack(fill="x", pady=2)

        # ==================== 2. Tools & Shapes ====================
        tools_group = ttk.LabelFrame(sidebar, text=" Tools & Shapes ", padding=6)
        tools_group.pack(fill="x", pady=(0, 6))

        tools_grid = [
            ("Pencil", 0, 0),
            ("Eraser", 0, 1),
            ("Line", 1, 0),
            ("Rectangle", 1, 1),
            ("Circle", 2, 0),
            ("Triangle", 2, 1),
        ]
        for name, row, col in tools_grid:
            ttk.Radiobutton(
                tools_group, text=name, variable=self.tool_var,
                value=name, command=self._on_tool_change, style="Toolbutton"
            ).grid(row=row, column=col, padx=2, pady=2, sticky="ew")

        tools_group.columnconfigure(0, weight=1)
        tools_group.columnconfigure(1, weight=1)

        # ==================== 3. Quick Color Palette ====================
        color_group = ttk.LabelFrame(sidebar, text=" Colors ", padding=6)
        color_group.pack(fill="x", pady=(0, 6))

        # Current Color indicator header
        cur_color_frame = ttk.Frame(color_group)
        cur_color_frame.pack(fill="x", pady=(0, 4))
        ttk.Label(cur_color_frame, text="Active Pen:").pack(side="left")
        self.pen_swatch = tk.Label(cur_color_frame, width=3, height=1, bg=self.color, relief="solid", bd=1)
        self.pen_swatch.pack(side="left", padx=6)

        ttk.Button(cur_color_frame, text="More...", command=self.pick_color).pack(side="right")

        # 6x2 Quick Swatch Grid
        palette_frame = ttk.Frame(color_group)
        palette_frame.pack(fill="x", pady=3)
        self.swatch_buttons = []

        for idx, hex_code in enumerate(self.PALETTE_COLORS):
            r, c = divmod(idx, 6)
            btn = tk.Button(
                palette_frame,
                bg=hex_code,
                activebackground=hex_code,
                relief="ridge",
                bd=2,
                width=2,
                height=1,
                cursor="hand2",
                command=lambda color=hex_code: self.select_color(color),
            )
            btn.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
            palette_frame.columnconfigure(c, weight=1)
            self.swatch_buttons.append(btn)

        # Background color selection
        bg_frame = ttk.Frame(color_group)
        bg_frame.pack(fill="x", pady=(4, 0))
        ttk.Label(bg_frame, text="Canvas BG:").pack(side="left")
        self.bg_swatch = tk.Label(bg_frame, width=3, height=1, bg=self.bg_color, relief="solid", bd=1)
        self.bg_swatch.pack(side="left", padx=6)
        ttk.Button(bg_frame, text="Change BG", command=self.pick_bg_color).pack(side="right")

        # ==================== 4. Brush Size ====================
        brush_group = ttk.LabelFrame(sidebar, text=" Brush Size ", padding=6)
        brush_group.pack(fill="x", pady=(0, 6))

        size_info = ttk.Frame(brush_group)
        size_info.pack(fill="x")
        self.size_label = ttk.Label(size_info, text=f"Size: {self.size}px")
        self.size_label.pack(side="left")

        self.size_preview = tk.Canvas(size_info, width=28, height=28, bg="#f3f4f6", highlightthickness=0)
        self.size_preview.pack(side="right")
        self._update_size_preview()

        # Preset size pills
        presets_frame = ttk.Frame(brush_group)
        presets_frame.pack(fill="x", pady=(2, 4))
        for p_size in (2, 5, 10, 20):
            ttk.Button(
                presets_frame,
                text=f"{p_size}px",
                width=4,
                command=lambda s=p_size: self.change_size(s)
            ).pack(side="left", expand=True, fill="x", padx=1)

        self.slider = ttk.Scale(
            brush_group,
            from_=1,
            to=40,
            orient="horizontal",
            command=self.change_size
        )
        self.slider.set(self.size)
        self.slider.pack(fill="x", pady=2)

        # ==================== 5. Status Bar ====================
        status_bar = ttk.Frame(self.root, relief="sunken", padding=(8, 4))
        status_bar.pack(fill="x", side="bottom")
        ttk.Label(status_bar, textvariable=self.status, font=("Segoe UI", 9)).pack(side="left")

        # Canvas Mouse Bindings
        self.canvas.bind("<Button-1>", self.start)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.release)

    def _bind_shortcuts(self):
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-Z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-Y>", lambda e: self.redo())
        self.root.bind("<Control-s>", lambda e: self.save())
        self.root.bind("<Control-S>", lambda e: self.save())
        self.root.bind("<Control-n>", lambda e: self.clear())
        self.root.bind("<Control-N>", lambda e: self.clear())

    def _on_canvas_resize(self, event):
        if event.width > self.width or event.height > self.height:
            new_w = max(self.width, event.width + 400)
            new_h = max(self.height, event.height + 400)
            new_layer = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
            new_layer.paste(self.drawing_layer, (0, 0))
            self.drawing_layer = new_layer
            self.draw = ImageDraw.Draw(self.drawing_layer)
            self.width, self.height = new_w, new_h

    def _push_undo(self):
        self.undo_stack.append((self.drawing_layer.copy(), self.bg_color))
        if len(self.undo_stack) > 30:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def undo(self):
        if not self.undo_stack:
            return
        self.redo_stack.append((self.drawing_layer.copy(), self.bg_color))
        self.drawing_layer, self.bg_color = self.undo_stack.pop()
        self.draw = ImageDraw.Draw(self.drawing_layer)
        self.canvas.configure(bg=self.bg_color)
        self.bg_swatch.configure(bg=self.bg_color)
        self._refresh_canvas_display()
        self.update_status()

    def redo(self):
        if not self.redo_stack:
            return
        self.undo_stack.append((self.drawing_layer.copy(), self.bg_color))
        self.drawing_layer, self.bg_color = self.redo_stack.pop()
        self.draw = ImageDraw.Draw(self.drawing_layer)
        self.canvas.configure(bg=self.bg_color)
        self.bg_swatch.configure(bg=self.bg_color)
        self._refresh_canvas_display()
        self.update_status()

    def _refresh_canvas_display(self):
        self.canvas.delete("all")
        # Composite transparent drawing layer onto current canvas background
        composite = Image.new("RGB", (self.width, self.height), self.bg_color)
        composite.paste(self.drawing_layer, (0, 0), self.drawing_layer)
        self.tk_canvas_img = ImageTk.PhotoImage(composite)
        self.canvas.create_image(0, 0, image=self.tk_canvas_img, anchor="nw")

    def _on_tool_change(self):
        self.tool = self.tool_var.get()
        self._update_size_preview()
        self.update_status()

    def _update_size_preview(self):
        self.size_preview.delete("all")
        r = max(1, self.size // 2)
        cx, cy = 14, 14
        fill_col = self.bg_color if self.tool == "Eraser" else self.color
        self.size_preview.create_oval(cx - r, cy - r, cx + r, cy + r, fill=fill_col, outline="#475569")

    def update_status(self):
        self.status.set(
            f"Tool: {self.tool}  |  Size: {self.size}px  |  Pen: {self.color}  |  Canvas: {self.bg_color}"
        )

    def select_color(self, hex_code):
        self.color = hex_code
        self.pen_swatch.configure(bg=hex_code)
        self._update_size_preview()
        self.update_status()

    def pick_color(self):
        # Pass parent=self.root so the dialog always renders in front
        c = colorchooser.askcolor(parent=self.root, title="Choose Pen Color", initialcolor=self.color)[1]
        if c:
            self.select_color(c)

    def pick_bg_color(self):
        # Pass parent=self.root so the dialog always renders in front
        c = colorchooser.askcolor(parent=self.root, title="Choose Canvas Background Color", initialcolor=self.bg_color)[1]
        if c:
            self._push_undo()
            self.bg_color = c
            self.canvas.configure(bg=c)
            self.bg_swatch.configure(bg=c)
            self._refresh_canvas_display()
            self._update_size_preview()
            self.update_status()

    def change_size(self, value):
        self.size = max(1, int(float(value)))
        try:
            if abs(float(self.slider.get()) - self.size) >= 1.0:
                self.slider.set(self.size)
        except Exception:
            pass
        self.size_label.configure(text=f"Size: {self.size}px")
        self._update_size_preview()
        self.update_status()

    def start(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.last_x, self.last_y = event.x, event.y
        self._push_undo()

        if self.tool in ("Pencil", "Eraser"):
            r = max(1, self.size // 2)
            if self.tool == "Eraser":
                canvas_col = self.bg_color
                draw_col = (0, 0, 0, 0)
            else:
                canvas_col = self.color
                draw_col = self.color

            self.canvas.create_oval(
                event.x - r, event.y - r, event.x + r, event.y + r,
                fill=canvas_col, outline=canvas_col
            )
            self.draw.ellipse(
                [event.x - r, event.y - r, event.x + r, event.y + r],
                fill=draw_col, outline=draw_col
            )

    def drag(self, event):
        if self.tool in ("Pencil", "Eraser"):
            r = max(1, self.size // 2)
            if self.tool == "Eraser":
                canvas_col = self.bg_color
                draw_col = (0, 0, 0, 0)
            else:
                canvas_col = self.color
                draw_col = self.color

            self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                fill=canvas_col, width=self.size, capstyle="round", smooth=True
            )
            self.draw.line(
                [(self.last_x, self.last_y), (event.x, event.y)],
                fill=draw_col, width=self.size
            )
            self.draw.ellipse(
                [event.x - r, event.y - r, event.x + r, event.y + r],
                fill=draw_col, outline=draw_col
            )
            self.last_x, self.last_y = event.x, event.y
            return

        if self.preview:
            self.canvas.delete(self.preview)

        if self.tool == "Line":
            self.preview = self.canvas.create_line(
                self.start_x, self.start_y, event.x, event.y,
                fill=self.color, width=self.size
            )
        elif self.tool == "Rectangle":
            self.preview = self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline=self.color, width=self.size
            )
        elif self.tool == "Circle":
            self.preview = self.canvas.create_oval(
                self.start_x, self.start_y, event.x, event.y,
                outline=self.color, width=self.size
            )
        elif self.tool == "Triangle":
            pts = [
                self.start_x, event.y,
                (self.start_x + event.x) / 2, self.start_y,
                event.x, event.y,
            ]
            self.preview = self.canvas.create_polygon(
                pts, outline=self.color, fill="", width=self.size
            )

    def release(self, event):
        if self.preview:
            self.canvas.delete(self.preview)
            self.preview = None

        if self.tool == "Line":
            self.canvas.create_line(
                self.start_x, self.start_y, event.x, event.y,
                fill=self.color, width=self.size
            )
            self.draw.line(
                [(self.start_x, self.start_y), (event.x, event.y)],
                fill=self.color, width=self.size
            )
        elif self.tool == "Rectangle":
            x0, y0 = min(self.start_x, event.x), min(self.start_y, event.y)
            x1, y1 = max(self.start_x, event.x), max(self.start_y, event.y)
            self.canvas.create_rectangle(
                x0, y0, x1, y1, outline=self.color, width=self.size
            )
            self.draw.rectangle(
                [x0, y0, x1, y1], outline=self.color, width=self.size
            )
        elif self.tool == "Circle":
            x0, y0 = min(self.start_x, event.x), min(self.start_y, event.y)
            x1, y1 = max(self.start_x, event.x), max(self.start_y, event.y)
            self.canvas.create_oval(
                x0, y0, x1, y1, outline=self.color, width=self.size
            )
            self.draw.ellipse(
                [x0, y0, x1, y1], outline=self.color, width=self.size
            )
        elif self.tool == "Triangle":
            pts = [
                (self.start_x, event.y),
                ((self.start_x + event.x) / 2, self.start_y),
                (event.x, event.y),
            ]
            flat_pts = [c for pt in pts for c in pt]
            self.canvas.create_polygon(
                flat_pts, outline=self.color, fill="", width=self.size
            )
            int_pts = [(int(x), int(y)) for x, y in pts]
            self.draw.polygon(int_pts, outline=self.color, width=self.size)

    def clear(self):
        if not messagebox.askyesno(
            "Clear Canvas",
            "Are you sure you want to clear the canvas? All unsaved drawing will be lost.",
            parent=self.root
        ):
            return

        self._push_undo()
        self.canvas.delete("all")
        self.drawing_layer = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.drawing_layer)

    def save(self):
        # Pass parent=self.root so file dialog always renders in front
        filepath = filedialog.asksaveasfilename(
            parent=self.root,
            title="Save Drawing",
            defaultextension=".png",
            filetypes=[
                ("PNG Image (*.png)", "*.png"),
                ("JPEG Image (*.jpg;*.jpeg)", "*.jpg;*.jpeg"),
                ("BMP Image (*.bmp)", "*.bmp"),
                ("All Files (*.*)", "*.*")
            ],
            confirmoverwrite=True,
        )

        if not filepath:
            return

        norm_path = os.path.abspath(os.path.normpath(filepath))
        valid_extensions = {".png", ".jpg", ".jpeg", ".bmp"}
        _, ext = os.path.splitext(norm_path.lower())
        if ext not in valid_extensions:
            norm_path += ".png"
            ext = ".png"

        try:
            self.root.update_idletasks()
            w = max(10, self.canvas.winfo_width())
            h = max(10, self.canvas.winfo_height())

            # Composite drawing layer onto canvas background color
            composite = Image.new("RGB", (self.width, self.height), self.bg_color)
            composite.paste(self.drawing_layer, (0, 0), self.drawing_layer)

            crop_w = min(w, self.width)
            crop_h = min(h, self.height)
            export_img = composite.crop((0, 0, crop_w, crop_h))

            if ext in (".jpg", ".jpeg"):
                if export_img.mode != "RGB":
                    export_img = export_img.convert("RGB")
                export_img.save(norm_path, "JPEG", quality=95)
            else:
                export_img.save(norm_path)

            messagebox.showinfo(
                "Saved",
                f"Drawing saved successfully!\n\nSaved to: {norm_path}",
                parent=self.root
            )
        except Exception as ex:
            messagebox.showerror(
                "Save Error",
                f"Could not save image:\n{ex}",
                parent=self.root
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
