from tkinter import filedialog
from skimage import data
from recents import Recents
from PIL import ImageTk, Image
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

    def _save_jpg(self, img, directory):
        pass

    def save_as(self, img):
        directory = filedialog.asksaveasfilename(initialfile="image", title='Salvar imagem',
                                                 filetypes=[('PNG image', '.png'), ('JPG image', '.jpg'),
                                                            ('JPEG image', '.jpeg')])

        if not directory:
            return

        self.save(img, directory)

    def save(self, img, directory=None):
        if not directory:
            directory = Recents.read()[-1]

        if not (
                directory.endswith('.png') or
                directory.endswith('.jpg') or
                directory.endswith('.jpeg')
        ):
            directory += '.jpg'

        if directory.endswith(".jpeg") or directory.endswith('.jpg'):
            self._save_jpg(img, directory)
        else:
            Image.fromarray(img).save(directory)
