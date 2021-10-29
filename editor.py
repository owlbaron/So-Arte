import tkinter
from numpy.core.arrayprint import printoptions
from scipy.ndimage.interpolation import rotate
from utils import Utils
from image_system import ImageSystem
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial
from skimage import data, transform, img_as_float
import numpy as np


class Editor(Tk):
    def __init__(self, img):
        Tk.__init__(self)

        self.image_system = ImageSystem()
        self.protocol("WM_DELETE_WINDOW", partial(Utils.close_all, self))

        self.title('Só Arte')
        self.state('zoomed')
        self.menu = Menu(self)
        self.__configMenu__()

        self.painel = Frame(relief="raised", bd=4)
        self.painel.pack(side=RIGHT, fill=BOTH)
        

        self.fig = plt.figure(figsize=(10,10))
        self.ax = self.fig.add_subplot(111)
        self.ax.axis("off")
        self.ax.imshow(img)
        self.image = img
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x = 100, y = 0)
        
        self.histRotate = 0
        
        self.population_buttons()
        

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
                "Sair": partial(Utils.close_all, self)
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
            self.image = ImageSystem.open_file(self)
        else:
            self.image = ImageSystem.open_sample(self, name)
    
        self.ax.imshow(self.image)
        self.canvas.draw_idle()


    def stringTeste(self):
        self.valor += 1
        self.lblTest.config(text=self.valor)
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


    def population_buttons(self):
        buttonsEditorDict = {
            "btn1": {
                "titulo": "Transformação 1", 
            },
            "btn2": {
                "titulo": "Transformação 2", 
            },
            "btn3": {
                "titulo": "Transformação 3", 
            },
            "btn4": {
                "titulo": "Filtro 1", 
            },
            "btn5": {
                "titulo": "Filtro 2", 
            },
            "btn6": {
                "titulo": "Filtro 3", 
            },
        }
        
        i = 0 

        for btn in buttonsEditorDict.values():
            btnTeste = Button(self, text=btn["titulo"], command=partial(self.population_panedRight, btn["titulo"]))
            btnTeste.place(x = 0, y = 25 * i)
            i+=1

    def population_panedRight(self, title):
        for child in self.painel.winfo_children():
            child.destroy()
        
        

        lbl = Label(self.painel, text=title)
        lbl.grid(row=0, column=2, padx=1, pady=10)

        if title == "Transformação 1":
            lbltitle = Label(self.painel,text=title)
            lbltitle.grid(row=1, column=0, padx=1, pady=10)

        elif title == "Transformação 2":
            btnHorizontal = Button(self.painel, text="Horizontal", command=partial(self.flip, "horizontal"))
            btnHorizontal.grid(row=1, column=3, padx=1, pady=10)
            btnVertical = Button(self.painel, text="Vertical", command=partial(self.flip, "vertical"))
            btnVertical.grid(row=2, column=3, padx=1, pady=10)

        elif title == "Transformação 3":
            lblRotate = Label(self.painel,text="Rotate(Degrees):")
            lblRotate.grid(row=1, column=0, padx=1, pady=10)
            etyRotate = Entry(self.painel, bd=3)
            etyRotate.grid(row=1, column=2, padx=1, pady=10)
            btn = Button(self.painel, text="Rotate", command=partial(self.rotation, etyRotate))
            btn.grid(row=1, column=3, padx=1, pady=10)


    def rotation(self, degrees):
        # camerarot = np.zeros(self.image.shape)
        # angulo = np.pi/2 #Angulo em radianos 45 -> np.pi/4

        # #Codigo para realizar a rotação
        # matriz_rotacao = np.zeros((3,3))
        # matriz_rotacao[0][0] = np.cos(angulo)
        # matriz_rotacao[0][1] = np.sin(angulo)
        # matriz_rotacao[1][0] = -np.sin(angulo)
        # matriz_rotacao[1][1] = np.cos(angulo)
        # matriz_rotacao[2][2] = 1

        # #Codigo para alterar a posição da imagem
        # # matriz_rotacao[0][2] = -100
        # matriz_rotacao[1][2] = self.image.shape[1]


        # # Outra maneira de montar a matriz
        # # matriz_rotacao = np.array([[np.cos(angulo), np.sin(angulo), -100],
        # #                            [-np.sin(angulo), np.cos(angulo), 250],
        # #                            [0,0,1]])


        # trans = transform.EuclideanTransform(matriz_rotacao)

        # camerarot = transform.warp(self.image, trans.inverse)
        imgRot = np.array(rotate(self.image, int(degrees.get()) - self.histRotate), dtype=type(self.image[0,0,0]))
        self.histRotate = int(degrees.get())
        self.image = imgRot
        self.ax.clear()
        self.ax.axis("off")
        self.ax.imshow(self.image)
        self.canvas.draw_idle()

    def flip(self, direction):
        imgFlip = np.zeros(self.image.shape, dtype=type(self.image[0,0,0]))
        for i in range(self.image.shape[0]):
            for j in range(self.image.shape[1]):

                if direction == "horizontal":
                    imgFlip[i, j, :] = self.image[i, -(j+1), :]

                elif direction == "vertical":
                    imgFlip[i, j, :] = self.image[-(i+1), j, :]

        # print(self.image)
        # print(imgFlip)
        print("Terminou")
        self.image = imgFlip
        self.ax.imshow(self.image)
        self.canvas.draw_idle()