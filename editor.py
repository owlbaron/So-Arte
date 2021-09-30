from utils import Utils
from image_system import ImageSystem
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial


class Editor(Tk):
    def __init__(self, img):
        Tk.__init__(self)

        self.image_system = ImageSystem()
        self.protocol("WM_DELETE_WINDOW", partial(Utils.close_all, Utils, self))

        self.title('Só Arte')
        self.state('zoomed')

        self.menu = Menu(self)
        self.__configMenu__()

        self.fig = plt.figure(figsize=(12, 10))
        self.ax = self.fig.add_subplot(111)
        self.ax.axis("off")
        self.ax.imshow(img)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1, )

    def __configMenu__(self):
        exempleImageDict = {
            "camera": partial(self.open_file, name = 'camera'),
            "moeda": partial(self.open_file, name = 'moeda'),
            "foguete": partial(self.open_file, name = 'foguete'),
            "astronauta": partial(self.open_file, name = 'astronauta')
        }

        menuConfigDict = {
            "File": {
                "New": self.stringTeste,
                "Separator": "__________",
                "Open Image": partial(self.open_file, type='File'),
                "Open Exemple": exempleImageDict,
                "Separator1": "__________",
                "Sair": partial(Utils.close_all, self = Utils(), tela=self)
            },
            "View": {
                "Teste": self.stringTeste
            },

            "Help": {
                "Welcome": self.stringTeste,
                "About": self.stringTeste
            }
        }

        for itemCascade in menuConfigDict:
            self.population_menu(menuConfigDict[itemCascade], self.menu, itemCascade)
            


        self.config(menu=self.menu)

    

    def open_file(self, type='Img', name='Default'):
        if type == 'File':
            img = ImageSystem.open_file(self)
        else:
            img = ImageSystem.open_sample(self, name)
    
        self.ax.imshow(img)
        self.canvas.draw_idle()


    def stringTeste(self):
        print("Teste")

    def population_menu(self, list_item_menu, menu, itemCascade):
        new_item = Menu(menu, tearoff=0)
        for item in list_item_menu:
            func = list_item_menu[item]
            if item.startswith("Separator"):
                new_item.add_separator()

            elif(isinstance(func, dict)):
                self.population_menu(func, new_item, item)

            else:
                new_item.add_command(label=item, command=func)

        menu.add_cascade(label=itemCascade, menu=new_item)

# Arrumar o SEPARATOR
