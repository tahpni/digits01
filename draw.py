import tkinter as tk
from tkinter import colorchooser, filedialog, ttk
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
        img = ImageGrab

        # Save the image to a temporary location
        temp_path = "temp_image.png"
        img.save(temp_path)

        # Export the image path to a file for the C++ program
        with open('image_path.txt', 'w') as file:
            file.write(temp_path)

        # Optionally, you can call the C++ executable here
        os.system('./neuraldigits')   

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingModule(root)
    root.mainloop()
