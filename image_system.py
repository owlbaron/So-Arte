from tkinter import filedialog
from skimage import data
from recents import Recents
import matplotlib.pyplot as plt
import os


class ImageSystem:
    def open_file(self, filepath=None):
        if not filepath:
            filepath = filedialog.askopenfilename()

            if not filepath:
                return

        Recents.add_new({
            "type": "file",
            "name": os.path.basename(filepath),
            "param": filepath
        })

        return plt.imread(filepath)

    def open_sample(self, name):
        dict = {
            "camera": lambda: data.camera(),
            "moedas": lambda: data.coins(),
            "foguete": lambda: data.rocket(),
            "astronauta": lambda: data.astronaut()
        }

        sample = dict[name]()

        Recents.add_new({
            "type": "sample",
            "name": name.title(),
            "param": name
        })

        return sample
