# Simple Drawing App

A beginner-friendly **desktop drawing application built with Python, Tkinter, and Pillow (PIL)**. The application provides a digital canvas where users can draw freehand, erase, create basic geometric shapes, choose pen/background colors, change brush size, clear the canvas, and save the artwork as a PNG image.

> **Project type:** Python GUI / Desktop Application  
> **Primary platform:** Windows 10 / Windows 11  
> **Main file:** `simple_drawing.py`

---

## 1. Project Overview

The **Simple Drawing App** is a graphical desktop application designed to demonstrate practical Python GUI programming, event-driven programming, mouse-event handling, canvas graphics, file handling, and basic image processing.

The application uses **Tkinter** for the graphical user interface and drawing canvas, while **Pillow (PIL)** is used during the image-saving process. The interface contains a drawing canvas, a right-side toolbar, and a bottom status bar.

### Main features currently implemented

- Freehand **Pencil** drawing
- **Eraser** tool
- **Line** tool
- **Rectangle** tool
- **Circle** tool
- **Triangle** tool
- **Pen Color** selection
- **Canvas Background Color** selection
- Adjustable **Brush Size: 1–20 pixels**
- **Clear** canvas
- **Save** drawing as PNG
- Live shape preview while dragging
- Status bar showing selected tool, brush size, and pen color
- Windows DPI-awareness handling for high-resolution displays
- PNG saving with an ImageGrab method and a PostScript fallback

The project documentation describes the same overall workflow: initialize the application, build the interface, choose tools/settings, interact using mouse events, and finally save or clear the canvas.

---

## 2. Technology Stack

| Technology / Module | Purpose |
|---|---|
| **Python 3.x** | Main programming language |
| **Tkinter** | GUI, window, buttons, canvas, dialogs, status bar |
| **ttk** | Themed/modern Tkinter widgets |
| **colorchooser** | Select pen and canvas background colors |
| **filedialog** | Select PNG save location and filename |
| **messagebox** | Show success/error messages |
| **Pillow (PIL)** | Image handling during saving |
| **ImageGrab** | Capture the canvas screen area as an image |
| **Image** | Open/process image data for fallback saving |
| **ctypes** | Enable Windows DPI awareness |
| **io** | Convert PostScript string data into an in-memory byte stream |

### Imports used by the project

```python
import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox
from PIL import ImageGrab, Image
import ctypes
import io
```

---

## 3. System Requirements

### Software

- Windows 10 or Windows 11
- Python 3.x
- Visual Studio Code, PyCharm, or IDLE
- Pillow package
- Tkinter

### Hardware

The project documentation specifies:

- Intel Core i3 or equivalent processor (or above)
- Minimum 4 GB RAM
- Around 100 MB free storage
- Display resolution of 1366 × 768 or higher
- Keyboard and mouse/touchpad

---

## 4. Installation

### Step 1: Install Python

Install Python 3.x and make sure Python is available from the command line.

Check the installation:

```bash
python --version
```

On systems where the `python` command is not mapped, try:

```bash
py --version
```

### Step 2: Verify Tkinter

Tkinter is required for the GUI.

Run:

```bash
python -m tkinter
```

If a small Tkinter window opens, Tkinter is available.

### Step 3: Install Pillow

Open Command Prompt or the VS Code terminal and run:

```bash
pip install Pillow
```

A safer Windows alternative is:

```bash
py -m pip install Pillow
```

### Step 4: Put the project file in a folder

Recommended structure:

```text
Simple-Drawing-App/
└── simple_drawing.py
```

### Step 5: Run the application

From the project directory:

```bash
python simple_drawing.py
```

or:

```bash
py simple_drawing.py
```

The application window opens with a drawing canvas and a tools panel.

---

## 5. How to Use the Application

### 5.1 Pencil

1. Click **Pencil**.
2. Move the mouse to the canvas.
3. Hold the left mouse button.
4. Drag to draw.
5. Release the mouse button when finished.

The pencil uses the selected pen color and brush size.

### 5.2 Eraser

1. Click **Eraser**.
2. Hold the left mouse button on the drawing.
3. Drag over the part that should be removed.

The implementation uses the **current canvas background color** as the eraser color. This means the eraser follows the selected canvas background instead of always assuming that the background is white.

> Important: this is a color-based eraser, not an object-aware eraser. It paints over existing pixels/lines rather than restoring the previous drawing state.

### 5.3 Shapes

Use the **Shapes** dropdown and select:

- Line
- Rectangle
- Circle
- Triangle

For each shape:

1. Select the shape.
2. Press the left mouse button at the starting point.
3. Drag the mouse.
4. Watch the temporary preview.
5. Release the mouse button to finish.

### 5.4 Pen Color

1. Click **Pen Color**.
2. Choose a color from the color picker.
3. Click OK/Select.
4. The selected color is then used for new drawings.

The selected color is also shown in the status bar.

### 5.5 Canvas Background Color

1. Click **BG Color**.
2. Select the desired color.
3. The canvas background changes immediately.

### 5.6 Brush Size

The vertical **Brush Size** slider controls drawing thickness.

- Minimum: **1 pixel**
- Maximum: **20 pixels**
- Default: **3 pixels**

The selected value affects Pencil strokes, Eraser strokes, and shape outlines.

### 5.7 Clear

Click **Clear** to:

- Delete all canvas objects
- Reset the canvas background to white

The clear operation is implemented with:

```python
self.canvas.delete("all")
self.canvas.configure(bg="white")
```

### 5.8 Save

1. Click **Save**.
2. Choose a filename and location.
3. The application attempts to capture the canvas.
4. The drawing is saved as a `.png` file.
5. A success or error message is displayed.

The current code first uses **Pillow ImageGrab** and then tries a **Canvas PostScript + Pillow** fallback when ImageGrab fails.

---

## 6. Interface Layout

The application is organized into three main areas:

```text
+---------------------------------------------------------------+
|                       Drawing Canvas                          |
|                                                               |
|                                                               |
|                                                               |
|                                                               |
|                                     +-----------------------+ |
|                                     | Tools                 | |
|                                     |-----------------------| |
|                                     | Pencil                | |
|                                     | Eraser                | |
|                                     | Shapes ▼              | |
|                                     | Pen Color             | |
|                                     | BG Color              | |
|                                     | Brush Size            | |
|                                     | Clear                 | |
|                                     | Save                  | |
|                                     +-----------------------+ |
+---------------------------------------------------------------+
| Tool: Pencil | Brush Size: 3 | Color: #000000              |
+---------------------------------------------------------------+
```

The code creates a **1000 × 650 pixel** main window. The canvas expands with the window, the toolbar stays on the right, and the status bar is placed at the bottom.

---

## 7. How the Code Works

The application is implemented using a single main class:

```python
class DrawingApp:
```

The class stores the application state and contains methods for initialization, tool selection, drawing, color changes, clearing, and saving.

### Important instance variables

```python
self.tool = "Pencil"
self.color = "#000000"
self.size = 3
self.start_x = self.start_y = None
self.last_x = self.last_y = None
self.preview = None
```

#### `self.tool`
Stores the currently selected tool, such as `Pencil`, `Eraser`, `Line`, `Rectangle`, `Circle`, or `Triangle`.

#### `self.color`
Stores the selected pen color as a color string such as `#000000`.

#### `self.size`
Stores the current brush/outline size.

#### `self.start_x`, `self.start_y`
Store the position where a shape-drawing operation starts.

#### `self.last_x`, `self.last_y`
Store the previous mouse position during freehand drawing. They allow the application to connect the previous point to the current point.

#### `self.preview`
Stores the temporary canvas object used to preview geometric shapes while dragging.

---

## 8. GUI Creation

The constructor creates the complete interface.

### Main window

```python
root.title("Simple Drawing App")
root.geometry("1000x650")
```

### Canvas

The canvas is created with a white background and crosshair cursor:

```python
self.canvas = tk.Canvas(
    main,
    bg="white",
    cursor="crosshair",
    highlightthickness=2,
    highlightbackground="#cccccc"
)
```

### Toolbar

The controls are placed inside a `ttk.LabelFrame` on the right side.

### Status bar

A `StringVar` stores the status text:

```python
self.status = tk.StringVar()
```

The status is updated to show:

```text
Tool: Pencil | Brush Size: 3 | Color: #000000
```

This gives the user immediate feedback about the current drawing state.

---

## 9. Mouse Event Handling

One of the most important interview concepts in this project is **event-driven programming**.

The canvas binds three mouse events:

```python
self.canvas.bind("<Button-1>", self.start)
self.canvas.bind("<B1-Motion>", self.drag)
self.canvas.bind("<ButtonRelease-1>", self.release)
```

### `<Button-1>` — mouse press

Calls `start()`.

It records the first mouse coordinate:

```python
self.start_x, self.start_y = e.x, e.y
self.last_x, self.last_y = e.x, e.y
```

### `<B1-Motion>` — mouse movement while holding left button

Calls `drag()`.

For Pencil/Eraser, it continuously creates small connected line segments.

For shapes, it updates the temporary preview object.

### `<ButtonRelease-1>` — mouse release

Calls `release()`.

For geometric shapes, the current preview is left as the final shape by simply clearing the preview reference.

---

## 10. Freehand Drawing Algorithm

For Pencil and Eraser, the project uses the following basic idea:

```text
Mouse Press
    ↓
Store starting/last coordinates
    ↓
Mouse moves while button is held
    ↓
Draw line from previous point → current point
    ↓
Update last_x / last_y
    ↓
Repeat until mouse release
```

The key implementation is:

```python
self.canvas.create_line(
    self.last_x,
    self.last_y,
    e.x,
    e.y,
    fill=col,
    width=self.size,
    capstyle="round",
    smooth=True,
)
```

Using short line segments between consecutive mouse coordinates creates the appearance of continuous freehand drawing.

---

## 11. Shape Drawing Logic

### Line

A line uses the starting point and current mouse position:

```python
self.canvas.create_line(
    self.start_x,
    self.start_y,
    e.x,
    e.y,
    fill=self.color,
    width=self.size,
)
```

### Rectangle

A rectangle is created from the bounding coordinates:

```python
self.canvas.create_rectangle(
    self.start_x,
    self.start_y,
    e.x,
    e.y,
    outline=self.color,
    width=self.size,
)
```

### Circle / Oval

Tkinter uses `create_oval()` for the bounding box:

```python
self.canvas.create_oval(
    self.start_x,
    self.start_y,
    e.x,
    e.y,
    outline=self.color,
    width=self.size,
)
```

Depending on the bounding box dimensions, the resulting object can appear circular or elliptical.

### Triangle

The triangle is created by calculating three points from the starting and current positions:

```text
Point 1: left-middle
Point 2: top-middle
Point 3: right-middle
```

Then Tkinter's polygon drawing function is used:

```python
self.canvas.create_polygon(
    pts,
    outline=self.color,
    fill="",
    width=self.size,
)
```

---

## 12. Live Shape Preview

When drawing a shape, the previous temporary shape is removed before a new preview is created:

```python
if self.preview:
    self.canvas.delete(self.preview)
```

Then the current mouse position is used to create a new preview.

This produces an interactive effect:

```text
Start mouse drag
      ↓
Create preview
      ↓
Mouse moves
      ↓
Delete old preview
      ↓
Create updated preview
      ↓
Repeat
      ↓
Mouse release
      ↓
Keep final shape
```

This is one of the useful examples in the project of **real-time GUI interaction**.

---

## 13. Color Handling

### Pen color

The color chooser returns the selected color. If a valid color is returned, it is stored in:

```python
self.color = c
```

### Background color

The canvas background is changed using:

```python
self.canvas.configure(bg=c)
```

### Eraser behavior

The eraser gets the current canvas background:

```python
col = self.canvas.cget("bg") if self.tool == "Eraser" else self.color
```

This is why the eraser can match a changed canvas background.

---

## 14. Saving Mechanism

The Save function uses a two-stage approach.

### Stage 1: ImageGrab

The program first asks the user for a PNG filename:

```python
filepath = filedialog.asksaveasfilename(
    defaultextension=".png",
    filetypes=[("PNG", "*.png")]
)
```

Then it calculates the canvas position on the screen:

```python
x = self.canvas.winfo_rootx()
y = self.canvas.winfo_rooty()
x1 = x + self.canvas.winfo_width()
y1 = y + self.canvas.winfo_height()
```

The canvas region is captured with:

```python
ImageGrab.grab((x, y, x1, y1)).save(filepath)
```

### Stage 2: PostScript fallback

If ImageGrab fails, the code tries:

```python
ps = self.canvas.postscript(colormode="color")
img = Image.open(io.BytesIO(ps.encode("utf-8")))
img.save(filepath, "png")
```

The application then shows a success or error message.

> The source code notes that PostScript saving may require Ghostscript on some systems.

---

## 15. DPI Awareness

The application includes a Windows DPI-awareness block:

```python
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass
```

### Why is it used?

High-resolution Windows displays can scale GUI applications. The code attempts to make the application display more appropriately on high-DPI screens.

The `try/except` prevents the application from crashing if that Windows-specific call is unavailable or fails.

---

## 16. Application Startup

The entry point is:

```python
if __name__ == "__main__":
    root = tk.Tk()
    DrawingApp(root)
    root.mainloop()
```

### Meaning

1. `tk.Tk()` creates the main Tkinter window.
2. `DrawingApp(root)` builds the interface and connects events.
3. `root.mainloop()` starts the Tkinter event loop.

### What is the event loop?

The event loop waits for user actions such as:

- Mouse clicks
- Mouse movement
- Mouse release
- Button clicks
- Slider changes
- Dialog interactions

The application responds to these events by calling the appropriate methods.

---

## 17. Application Logic Flow

```text
Start Program
      ↓
Create Tkinter Root Window
      ↓
Create DrawingApp
      ↓
Initialize Tool / Color / Brush Size
      ↓
Build Canvas + Toolbar + Status Bar
      ↓
Bind Mouse Events
      ↓
Start mainloop()
      ↓
User Selects Tool
      ↓
User Presses / Drags / Releases Mouse
      ↓
Drawing or Shape Preview
      ↓
User Changes Color / Size / Background
      ↓
User Clears or Saves
      ↓
Application Continues Running
```

---

## 18. Project File Structure

The current implementation can run from a single Python source file:

```text
Simple-Drawing-App/
│
├── simple_drawing.py     # Main application source code
└── README.md             # Project documentation
```

A future version could separate the application into modules such as:

```text
Simple-Drawing-App/
├── app.py
├── drawing_tools.py
├── storage.py
├── ui.py
├── requirements.txt
└── README.md
```

That modular structure is a suggested improvement, not part of the current implementation.

---

## 19. Important Current Limitations

For interview discussions, it is important to distinguish **implemented features** from **planned features**.

### Implemented in the current source

- Pencil
- Eraser
- Line
- Rectangle
- Circle
- Triangle
- Pen color
- Background color
- Brush size
- Clear
- PNG saving
- Status bar
- Shape preview

### Mentioned in the project synopsis but not implemented in the current source

The synopsis describes **Undo and Redo** as intended/desired features, but the current `simple_drawing.py` file does **not** contain Undo/Redo buttons or undo/redo history logic.

This distinction is important in a viva/interview: explain that Undo/Redo is part of the proposed/future functionality rather than claiming that the current version implements it.

---

## 20. Future Scope

The project presentation identifies several possible extensions:

- Undo and Redo history
- Paint Bucket / Fill tool
- Text and annotations
- Multiple layers
- Multiple brush styles and textures
- Import and edit existing images
- JPEG export
- BMP export
- PDF export
- Canvas zoom and pan

These would turn the current beginner drawing tool into a more advanced graphics editor.

---

# 21. Interview / Viva Preparation

This section is written for a new developer or student preparing to explain the project in an interview, project viva, or practical examination.

## Q1. What is your project?

**Answer:**  
My project is a **Simple Drawing App**, a desktop GUI application developed using **Python, Tkinter, and Pillow**. It provides a digital canvas where users can draw freehand, erase, create basic shapes, change colors and brush size, clear the canvas, and save the drawing as a PNG image.

## Q2. Why did you choose Python?

**Answer:**  
Python provides simple syntax and has built-in GUI support through Tkinter. It is suitable for beginner desktop applications and allows quick development of event-driven graphical programs.

## Q3. Why did you use Tkinter?

**Answer:**  
Tkinter is Python's GUI toolkit and provides the window, buttons, labels, sliders, dialogs, and Canvas required for this application.

## Q4. What is the Canvas widget?

**Answer:**  
The Tkinter `Canvas` is the main drawing area. It supports graphical objects such as lines, rectangles, ovals, and polygons, which are used to implement the drawing tools.

## Q5. What is event-driven programming?

**Answer:**  
Event-driven programming means the application waits for user or system events and executes a corresponding function. In this project, mouse clicks, mouse movement, mouse release, button clicks, and slider changes trigger application logic.

## Q6. Which mouse events are used?

**Answer:**

- `<Button-1>` — left mouse button press
- `<B1-Motion>` — mouse movement while the left button is held
- `<ButtonRelease-1>` — left mouse button release

## Q7. How does freehand drawing work?

**Answer:**  
The program stores the previous mouse coordinate. During `<B1-Motion>`, it draws a line from the previous coordinate to the current coordinate and then updates the previous coordinate. Repeating this rapidly produces a continuous freehand stroke.

## Q8. How does the eraser work?

**Answer:**  
The eraser does not maintain a separate undo buffer. Instead, it draws using the current canvas background color, which visually covers the existing drawing.

## Q9. How are shapes drawn?

**Answer:**  
When the mouse is pressed, the starting coordinate is stored. During mouse movement, the application calculates the shape from the starting point to the current point. A temporary preview is shown. When the mouse is released, the preview becomes the final shape.

## Q10. How is the triangle generated?

**Answer:**  
The application calculates three points using the starting and current mouse coordinates, then passes those points to Tkinter's `create_polygon()` function.

## Q11. What is `StringVar` used for?

**Answer:**  
`StringVar` stores the status-bar text. Whenever the selected tool, brush size, or pen color changes, the text is updated automatically.

## Q12. What is `ttk`?

**Answer:**  
`ttk` is Tkinter's themed widget module. The project uses it for buttons, labels, frames, the option menu, and the brush-size slider to create a cleaner interface.

## Q13. What is Pillow?

**Answer:**  
Pillow is a Python imaging library. In this project it is used to save the drawing as a PNG image, including the ImageGrab capture method and the PostScript fallback processing.

## Q14. Why is `filedialog` used?

**Answer:**  
`filedialog` displays the Save dialog so the user can select the output filename and location.

## Q15. Why is `messagebox` used?

**Answer:**  
`messagebox` is used to show messages such as successful saving or an error when saving fails.

## Q16. What is `ctypes` doing in the project?

**Answer:**  
`ctypes` is used to call the Windows DPI-awareness API so the interface can scale more appropriately on high-resolution displays.

## Q17. What is `io.BytesIO` used for?

**Answer:**  
The PostScript fallback returns image data as text. `io.BytesIO` converts the encoded data into an in-memory byte stream that Pillow can read as image input.

## Q18. Why is there a `try/except` around DPI awareness?

**Answer:**  
The call is Windows-specific and can fail in some environments. The exception handling prevents that optional configuration step from terminating the application.

## Q19. How does the Clear button work?

**Answer:**  
It calls `canvas.delete("all")` to remove all drawing objects and then resets the background to white.

## Q20. Why does the Save function call `root.update()`?

**Answer:**  
The code updates the GUI before measuring and capturing the canvas so the interface is in its current visual state.

## Q21. How does the program know the canvas screen position?

**Answer:**  
It uses `winfo_rootx()` and `winfo_rooty()` to obtain the canvas's screen coordinates and combines those values with the canvas width and height to create the ImageGrab bounding box.

## Q22. What is the purpose of `mainloop()`?

**Answer:**  
`mainloop()` starts Tkinter's event loop. Without it, the GUI would not remain active and respond to user events.

## Q23. Is Undo/Redo implemented?

**Answer:**  
Not in the current source code. Undo and Redo were described in the project synopsis as desired functionality, but the current implementation does not contain a history stack or Undo/Redo controls.

## Q24. What could be improved?

**Answer:**  
The project can be extended with Undo/Redo history, fill color, text, layers, additional brush types, image import, more export formats, and zoom/pan support.

## Q25. What did you learn from the project?

**Answer:**  
The project provides practical experience with Python GUI development, object-oriented programming, event handling, mouse coordinates, canvas graphics, color selection, file dialogs, image capture, exception handling, and application workflow design.

---

# 22. Developer Walkthrough: Where to Modify the Code

A new developer can use the following map to understand where features live.

| Code area | Responsibility |
|---|---|
| Imports | Load Tkinter, Pillow, ctypes, and io |
| DPI block | Configure Windows DPI awareness |
| `DrawingApp.__init__()` | Create and configure the entire GUI |
| `update_status()` | Refresh status-bar information |
| `set_tool()` | Change active drawing tool |
| `pick_color()` | Change pen color |
| `pick_bg_color()` | Change canvas background |
| `change_size()` | Change brush size |
| `start()` | Record mouse starting position |
| `drag()` | Draw freehand strokes or shape previews |
| `release()` | Finish shape interaction |
| `clear()` | Delete all canvas objects and reset background |
| `save()` | Save canvas as PNG using capture/fallback logic |
| `mainloop()` | Keep the GUI running |

---

## 23. Example: Adding a New Tool

To add another drawing tool, a developer would generally:

1. Add a new button/menu option.
2. Store the tool name through `set_tool()`.
3. Add the drawing logic inside `drag()` and/or `release()`.
4. Add any required state variables in `__init__()`.
5. Update the status bar if extra information is needed.
6. Test mouse press, drag, and release behavior.

For example, a future Fill tool would require a different approach from Pencil because it must identify a region and replace its color rather than simply drawing a line.

---

## 24. Troubleshooting

### `ModuleNotFoundError: No module named 'PIL'`

Install Pillow:

```bash
python -m pip install Pillow
```

### `python` is not recognized

Try:

```bash
py simple_drawing.py
```

and verify Python is installed correctly.

### Tkinter does not open

Check:

```bash
python -m tkinter
```

If Tkinter is unavailable, use a Python installation that includes the Tk GUI components.

### Save does not work with ImageGrab

The current code automatically attempts a PostScript fallback. The source notes that PostScript support may require **Ghostscript** on some systems.

### The UI appears too large/small on Windows

The project includes a Windows DPI-awareness call, but display scaling can still vary between systems.

---

## 25. Recommended Development Workflow

For a beginner working on this project:

```text
1. Read simple_drawing.py
        ↓
2. Understand __init__()
        ↓
3. Understand the three mouse events
        ↓
4. Understand Pencil/Eraser logic
        ↓
5. Understand shape preview logic
        ↓
6. Understand color + brush-size handling
        ↓
7. Understand clear/save
        ↓
8. Add one feature at a time
        ↓
9. Test after every change
```

Do not change several core methods at once when learning the project. Small, testable changes make event-driven GUI bugs much easier to isolate.

---

## 26. Quick Start for New Users

```bash
# 1. Open the project folder
cd Simple-Drawing-App

# 2. Install dependency
python -m pip install Pillow

# 3. Run
python simple_drawing.py
```

Then:

```text
Choose Pencil / Eraser / Shape
        ↓
Choose color
        ↓
Set brush size
        ↓
Draw with the mouse
        ↓
Clear or Save
```

---

## 27. Project Objective

The project aims to provide a simple and user-friendly drawing application while demonstrating:

- Python GUI programming
- Event-driven programming
- Mouse event handling
- Basic computer graphics
- File handling
- Basic image processing
- Practical object-oriented programming

---

## 28. Academic Project Information

The supplied project report identifies the project as **Simple Drawing App** and describes it as a BCA project developed using Python, Tkinter, and Pillow. The supplied synopsis lists the student project group and identifies **Mr. Saumya Ranjan Pradhan** and **Mr. Swastik Ranjan Sahoo** as guides.

For repository documentation, the most important technical source is the current `simple_drawing.py` implementation. Where the synopsis and implementation differ, this README describes the **implemented code as the source of truth** and explicitly identifies proposed features such as Undo/Redo as not yet implemented.

---

## 29. References Mentioned in the Project Documents

The project documents reference:

- Python Software Foundation / Python documentation
- Tkinter documentation
- Pillow (PIL) documentation
- YouTube tutorials / online learning resources

For development, consult the official documentation corresponding to the Python, Tkinter, and Pillow versions installed on the machine.

---

## 30. Final Summary

The **Simple Drawing App** is a compact example of a Python event-driven desktop application. Its architecture is intentionally simple: a Tkinter window contains a Canvas and toolbar, mouse events control drawing, application variables store the current drawing state, and Pillow participates in image saving.

The most important concepts to understand before presenting this project are:

```text
Tkinter GUI
   +
Canvas Graphics
   +
Mouse Events
   +
Application State
   +
Shape Preview
   +
Image Saving
   =
Simple Drawing App
```

For an interview or viva, be able to explain **what each imported module does, how the three mouse events work, how freehand drawing is generated, how shape preview works, how colors/brush size are stored, how the canvas is cleared, and how PNG saving works**. Also clearly distinguish implemented functionality from future or proposed functionality.

---

## License

No explicit software license is specified in the supplied project documents. Add a license file before distributing the project publicly if one is required.
