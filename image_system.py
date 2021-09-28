from tkinter import filedialog
from skimage import data
import matplotlib.pyplot as plt


class ImageSystem:
    def open_file(self):
        filepath = filedialog.askopenfilename()

        return plt.imread(filepath)

    def open_sample(self, name):
        dict = {
            "camera": data.camera(),
            "moeda": data.coin(),
            "foguete": data.rocket(),
            "astronauta": data.astronaut()
        }

        return dict[name]
