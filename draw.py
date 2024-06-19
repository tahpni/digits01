import tkinter as tk
from tkinter import colorchooser, filedialog, ttk
from matplotlib import pyplot as plt
import PIL.ImageGrab as ImageGrab
import os

class DrawingModule:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing Module")
        self.canvas = tk.Canvas(self.root, bg="white", width=600, height=600)
        self.canvas.pack()

        self.color_fg = 'black'
        self.color_bg = 'white'
        self.old_x = None
        self.old_y = None
        self.pen_width = 5

        self.create_widgets()
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.stop_paint)

    def create_widgets(self):
        self.clear_button = tk.Button(self.root, text="Submit", command=self.submit_canvas)
        self.clear_button.pack(side=tk.BOTTOM)

    def paint(self, event):
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                    width=self.pen_width, fill=self.color_fg,
                                    capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def stop_paint(self, event):
        self.old_x = None
        self.old_y = None

    def submit_canvas(self):
       # Save the canvas content as an image file
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

        # Grab the image from the canvas and save it
        ImageGrab.grab().crop((x, y, x1, y1)).save("UserInput.png") 
    
        
        fetch('/execute_draw', { method: 'POST' })
        then(response) => {response.json()
        then(data) => {alert(data.output)};
        }
if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingModule(root)
    root.mainloop()
