from tkinter import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Editor(Tk):
    def __init__(self, img):
        Tk.__init__(self)

        self.title('Só Arte')
        self.state('zoomed')

        fig = plt.figure(figsize=(12, 10))
        plt.axis("off")
        plt.imshow(img)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

