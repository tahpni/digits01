import tkinter as tk
import requests as req
from tkinter import colorchooser, filedialog, ttk
from matplotlib import pyplot as plt
import PIL.ImageGrab as ImageGrab
import os

class DrawingModule:
    def __init__(self, root):
        self.root = root
        self.root.title("Draw a Number")
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

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

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
        x1 = self.canvas.winfo_rootx()
        y1 = self.canvas.winfo_rooty()
        x2 = x1 + self.canvas.winfo_width()
        y2 = y1 + self.canvas.winfo_height()

        ImageGrab.grab(bbox = (x1, y1, x2, y2)).save("UserInput.png")
        response = req.post('http://localhost:5000/execute_neural')
        exit()
if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingModule(root)
    root.mainloop()
