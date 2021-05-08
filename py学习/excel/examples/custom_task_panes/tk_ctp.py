"""
PyXLL Examples: Tk Custom Task Pane

This example shows how a Tkinter window can be hosted
in an Excel Custom Task Pane.

Custom Task Panes are Excel controls that can be docked in the
Excel application or be floating windows. These can be used for
creating more advanced UI Python tools within Excel.
"""
from pyxll import create_ctp, CTPDockPositionRight, xl_app
import tkinter as tk
import tkinter.messagebox as messagebox
import logging
import os

_log = logging.getLogger(__name__)
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

try:
    # pip install pillow
    from PIL import Image, ImageTk
except ImportError:
    Image = ImageTk = None
    _log.warn("PIL not installed. Use 'pip install pillow' to install.")

class ExampleTkFrame(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.init_window()

    def init_window(self):
        # allow the widget to take the full space of the root window
        self.pack(fill=tk.BOTH, expand=True)

        # The widgets are aligned into 12 columns
        row = 0
        column = 0

        # Load the Tk icon and add the header to the widget
        if Image is not None:
            image_path = os.path.join(os.path.dirname(__file__), "icons", "tk.png")
            load = Image.open(image_path)
            render = ImageTk.PhotoImage(load)
            img = tk.Label(self, image=render)
            img.image = render
            img.grid(column=column, row=row, padx=10, pady=10, columnspan=2)
            column = 2

        label = tk.Label(self, text="Tk Custom Task Pane")
        label.grid(column=column, row=row, columnspan=12 - column, padx=10, sticky="w")
        row += 1

        # Step 1, getting the address of the currently selected cell
        label = tk.Label(self, text="1. Press the button to get the current selection")
        label.grid(column=0, row=row, columnspan=12, padx=10, pady=10, sticky="w")
        row += 1

        button = tk.Button(self, text=">>", command=self.get_selected_cell_address)
        button.grid(column=0, row=row, columnspan=1, padx=(10, 0), pady=10, sticky="nsew")

        self.address = tk.StringVar()
        entry = tk.Entry(self, textvar=self.address)
        entry.grid(column=1, row=row, columnspan=11, padx=(0, 10), pady=10, ipady=0, sticky="nsew")
        row += 1

        # Step 2, getting the value of the cell
        label = tk.Label(self, text="2. Press the button to get cell value")
        label.grid(column=0, row=row, columnspan=12, padx=10, sticky="w")
        row += 1

        button = tk.Button(self, text="Get Cell Value", command=self.get_cell_value)
        button.grid(column=0, row=row, columnspan=12, padx=10, pady=10, sticky="nsew")
        row += 1

        self.cell_value = tk.StringVar()
        entry = tk.Entry(self, textvar=self.cell_value)
        entry.grid(column=0, row=row, columnspan=12, padx=10, pady=30, sticky="nsew")
        row += 1

        # Step 3, setting the value of the cell
        label = tk.Label(self, text="3. Edit the text above and set it")
        label.grid(column=0, row=row, columnspan=12, padx=10, sticky="w")
        row += 1

        button = tk.Button(self, text="Set Cell Value", command=self.set_cell_value)
        button.grid(column=0, row=row, columnspan=12, padx=10, pady=10, sticky="nsew")

        # Allow the last grid column to stretch horizontally
        self.columnconfigure(11, weight=1)

    def get_selected_cell_address(self):
        """Get the address of the currently selected cell."""
        xl = xl_app(com_package="win32com")
        address = xl.Selection.Address
        self.address.set(address)

    def get_cell_value(self):
        address = self.address.get()
        if not address:
            messagebox.showerror("Error", "Select a cell with the button above first.")

        xl = xl_app(com_package="win32com")
        cell = xl.Range(address)
        self.cell_value.set(str(cell.Value))

    def set_cell_value(self):
        address = self.address.get()
        if not address:
            messagebox.showerror("Error", "Select a cell with the button above first.")

        xl = xl_app(com_package="win32com")
        cell = xl.Range(address)
        cell.Value = self.cell_value.get()

def show_tk_ctp():
    """Create a Tk window and embed it in Excel as a Custom Task Pane."""

    # Create the top level Tk window
    window = tk.Toplevel()
    window.title("Tk Example")

    # Add our example frame to it
    ExampleTkFrame(master=window)

    # Add the widget to Excel as a Custom Task Pane
    create_ctp(window, width=400, position=CTPDockPositionRight)

if __name__ == "__main__":
    root = tk.Tk()
    ExampleTkFrame(master=root)
    root.mainloop()