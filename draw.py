import tkinter as tk
from PIL import ImageGrab, Image
import pandas as pd
import numpy as np
import subprocess

class DrawingModule:
    def __init__(self, root):
        self.root = root
        root.resizable(False, False)
        self.root.title("Draw a Number")
        self.canvas = tk.Canvas(self.root, bg="white", width=560, height=560, borderwidth=0, highlightthickness=0)
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
                                    width=self.pen_width * 5, fill=self.color_fg,
                                    capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def stop_paint(self, event):
        self.old_x = None
        self.old_y = None

    def submit_canvas(self):
        x1 = self.canvas.winfo_rootx() + self.canvas.winfo_x()
        y1 = self.canvas.winfo_rooty() + self.canvas.winfo_y()
        x2 = x1 + self.canvas.winfo_width()
        y2 = y1 + self.canvas.winfo_height()
        img = ImageGrab.grab(bbox=(x1 + 1, y1 + 1, x2 - 1, y2 - 1))
        img = img.resize((28, 28), Image.LANCZOS)
        img.save("UserInput.png")
        self.downscale_and_convert_to_csv(img)
        subprocess.run(["g++", "neuron.cpp", "-o", "neuron"], check=True)
        process = subprocess.Popen(['./neuron'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout.decode())
        exit()

    def downscale_and_convert_to_csv(self, img):
        img = img.convert("L")
        img_data = np.asarray(img)
        img_data = 255 - img_data - img_data - img_data - img_data - 3
        img_data_flat = img_data.flatten()
        df = pd.DataFrame([img_data_flat])
        df.to_csv("test.csv", index=False, header=False)

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingModule(root)
    root.mainloop()
