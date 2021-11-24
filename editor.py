import tkinter
from numpy.core.arrayprint import printoptions
from scipy.ndimage.interpolation import rotate
from utils import Utils
from image_system import ImageSystem
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial
from skimage import data, transform, img_as_float, exposure, filters
import numpy as np
from recents import Recents

class Editor(Tk):
    def __init__(self, img):
        Tk.__init__(self)

        self.recents = Recents.read()
        self.image_system = ImageSystem()
        self.protocol("WM_DELETE_WINDOW", partial(Utils.close_all, self))

        self.title('Só Arte')
        self.state('zoomed')
        self.menu = Menu(self)
        self.__configMenu__()

        self.painel = Frame(relief="raised", bd=4)
        self.painel.pack(side=RIGHT, fill=BOTH)

        self.fig = plt.figure(figsize=(10, 10))
        self.ax = self.fig.add_subplot(111)
        self.ax.axis("off")
        self.ax.imshow(img)
        self.image = img
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=100, y=0)

        self.histRotate = 0
        self.histImg = img

        self.population_buttons()
        

    def __configMenu__(self):
        exempleImageDict = {
            "camera": partial(self.open_file, name='camera'),
            "moeda": partial(self.open_file, name='moeda'),
            "foguete": partial(self.open_file, name='foguete'),
            "astronauta": partial(self.open_file, name='astronauta')
        }

        recentsDict = {}
        for index, recent in enumerate(self.recents):
            if recent["type"] == "file":
                recentsDict[recent["name"]] = partial(self.open_file, name=recent["param"].lower())
            else:
                recentsDict[recent["name"]] = partial(self.open_file, name=recent["param"])

        menuConfigDict = {
            "File": {
                "Save": self.save,
                "Save as...": self.save_as,
                "Separator": "__________",
                "Open Image": partial(self.open_file, type='File'),
                "Open Exemple": exempleImageDict,
                "Open Recent": recentsDict,
                "Separator1": "__________",
                "Sair": partial(Utils.close_all, self)
            },
        }

        for itemCascade in menuConfigDict:
            self.population_menu(menuConfigDict[itemCascade], self.menu, itemCascade)

        self.config(menu=self.menu)

    def save(self):
        self.image_system.save(self.image)

    def save_as(self):
        self.image_system.save_as(self.image)

    def open_file(self, type='Img', name='Default'):
        if type == 'File':
            self.image = ImageSystem.open_file(self)
        else:
            self.image = ImageSystem.open_sample(self, name)

        self.ax.imshow(self.image)
        self.canvas.draw_idle()

    def population_menu(self, list_item_menu, menu, itemCascade):
        new_item = Menu(menu, tearoff=0)
        for item in list_item_menu:
            func = list_item_menu[item]
            if item.startswith("Separator"):
                new_item.add_separator()

            elif (isinstance(func, dict)):
                self.population_menu(func, new_item, item)

            else:
                new_item.add_command(label=item, command=func)

        menu.add_cascade(label=itemCascade, menu=new_item)

    def population_buttons(self):
        buttonsEditorDict = {
            "btn1": {
                "titulo": "Ajustar tamanho",
            },
            "btn2": {
                "titulo": "Mover",
            },
            "btn3": {
                "titulo": "Transformação 2",
            },
            "btn4": {
                "titulo": "Transformação 3",
            },
            "btn5": {
                "titulo": "Filtro 1",
            },
            "btn6": {
                "titulo": "Filtro 2",
            },
            "btn7": {
                "titulo": "Filtro 3",
            },
            "btn7": {
                "titulo": "Filtro 4", 
            },
        }

        i = 0

        for btn in buttonsEditorDict.values():
            btnTeste = Button(self, text=btn["titulo"], command=partial(self.population_panedRight, btn["titulo"]))
            btnTeste.place(x=0, y=25 * i)
            i += 1

    def population_panedRight(self, title):
        for child in self.painel.winfo_children():
            child.destroy()

        lbl = Label(self.painel, text=title)
        lbl.grid(row=0, column=2, padx=1, pady=10)

        if title == "Ajustar tamanho":
            lblScale = Label(self.painel, text="Escala (percentual, ex.: 50)")
            lblScale.grid(row=1, column=0, padx=1, pady=10)
            etyScale = Entry(self.painel, bd=3)
            etyScale.grid(row=1, column=1, padx=1, pady=10)
            btn = Button(self.painel, text="Aplicar", command=partial(self.scale, etyScale))
            btn.grid(row=1, column=3, padx=1, pady=10)

        elif title == "Mover":
            lblTranslateX = Label(self.painel, text="X (Valor em pixels. ex.: 90)")
            lblTranslateX.grid(row=1, column=0, padx=1, pady=10)
            etyTranslateX = Entry(self.painel, bd=3)
            etyTranslateX.grid(row=1, column=1, padx=1, pady=10)
            lblTranslateY = Label(self.painel, text="Y (Valor em pixels. ex.: 130)")
            lblTranslateY.grid(row=2, column=0, padx=1, pady=10)
            etyTranslateY = Entry(self.painel, bd=3)
            etyTranslateY.grid(row=2, column=1, padx=1, pady=10)
            btn = Button(self.painel, text="Aplicar", command=partial(self.translate, etyTranslateX, etyTranslateY))
            btn.grid(row=3, column=0, padx=1, pady=10)

        elif title == "Transformação 2":
            btnHorizontal = Button(self.painel, text="Horizontal", command=partial(self.flip, "horizontal"))
            btnHorizontal.grid(row=1, column=3, padx=1, pady=10)
            btnVertical = Button(self.painel, text="Vertical", command=partial(self.flip, "vertical"))
            btnVertical.grid(row=2, column=3, padx=1, pady=10)

        elif title == "Transformação 3":
            lblRotate = Label(self.painel, text="Rotate(Degrees):")
            lblRotate.grid(row=1, column=0, padx=1, pady=10)
            etyRotate = Entry(self.painel, bd=3)
            etyRotate.grid(row=1, column=2, padx=1, pady=10)
            btn = Button(self.painel, text="Rotate", command=partial(self.rotation, etyRotate))
            btn.grid(row=1, column=3, padx=1, pady=10)

        elif title == "Filtro 1":
            dict = {
                "Gato": data.chelsea(),
                "Café": data.coffee(),
                "Cores": data.colorwheel(),
                "Espaço": data.hubble_deep_field(),
                "Foguete": data.rocket(),
                "Astronauta": data.astronaut()
            }

            lblRotate = Label(self.painel, text="Image Filter:")
            lblRotate.grid(row=1, column=0, padx=1, pady=10)

            cboImgs = ttk.Combobox(self.painel, values=list(dict.keys()), state='readonly')
            cboImgs.current(0)
            cboImgs.grid(row=1, column=2, padx=1, pady=10)
            cboImgs.bind('<<ComboboxSelected>>', partial(self.mesclar, cboImgs, dict))

            btn = Button(self.painel, text="Import", command=self.mesclarImport)
            btn.grid(row=3, column=2, padx=1, pady=10)

            # btn = Button(self.painel, text="Apply", command=partial(self.mesclar, cboImgs, dict, True))
            btn = Button(self.painel, text="Apply", command=self.apply)
            btn.grid(row=4, column=1, padx=1, pady=10)

            btn = Button(self.painel, text="Cancel", command=self.cancel)
            btn.grid(row=4, column=3, padx=1, pady=10)
        
        elif title == "Filtro 4":

            lblRotate = Label(self.painel,text="Otsu:")
            lblRotate.grid(row=1, column=0, padx=1, pady=10)
            
            btn = Button(self.painel, text="Import", command=self.otsu)
            btn.grid(row=3, column=2, padx=1, pady=10)
            
        elif title == 'Filtro 2':
            lblSigma = Label(self.painel, text="Sigma")
            lblSigma.grid(row=1, column=0, padx=1, pady=10)
            etySigma = Entry(self.painel, bd=3)
            etySigma.grid(row=1, column=1, padx=1, pady=10)
            btn = Button(self.painel, text="Aplicar", command=partial(self.filtro_gausiano, etySigma))
            btn.grid(row=1, column=3, padx=1, pady=10)

    def convolucao(self, imagem, kernel):
        hkernel, wkernel = kernel.shape

        padimagem = np.pad(imagem, pad_width=(
            (hkernel // 2, hkernel // 2), (wkernel // 2, wkernel // 2)
        ), mode="constant", constant_values=0).astype(np.float)

        resultado = np.zeros(padimagem.shape)

        h = hkernel // 2
        w = wkernel // 2

        hpadimagem, wpadimagem = padimagem.shape

        for i in range(h, hpadimagem - h):
            for j in range(w, wpadimagem - w):
                x = padimagem[i - h:i - h + hkernel, j - w:j - w + wkernel]
                x = x.flatten() * kernel.flatten()
                resultado[i][j] = x.sum()

        if h == 0:
            return resultado[h:, w:-w]

        if w == 0:
            return resultado[h:-h, w:]

        return resultado[h:-h, w:-w]

    def filtro_gausiano(self, etySigma):
        sigma = int(etySigma.get())
        tam_filtro = 2 * int(4 * sigma - 0.5) + 1
        filtro = np.zeros((tam_filtro, tam_filtro), np.float32)

        h = tam_filtro // 2
        w = tam_filtro // 2

        for i in range(-h, h + 1):
            for j in range(-w, w + 1):
                x1 = 2 * np.pi * (sigma ** 2)
                x2 = np.exp(-(i ** 2 + j ** 2) / (2 * sigma ** 2))

                filtro[i + h, j + w] = (1 / x1) * x2

        filtrada = np.zeros_like(self.image, np.float32)

        filtrada[:, :] = self.convolucao(self.image[:, :], filtro)

        self.image = filtrada.astype(np.uint8)
        self.ax.imshow(self.image)
        self.canvas.draw_idle()

    def scale(self, scale):
        img = img_as_float(self.image)
        imgScale = rescale(img, int(scale.get()) / 100)

        self.image = imgScale
        self.ax.imshow(self.image)
        self.canvas.draw_idle()

    def translate(self, etyX, etyY):
        img = img_as_float(self.image)
        matrix_translate = np.array([
            [1, 0, int(etyX.get())],
            [0, 1, int(etyY.get())],
            [0, 0, 1]
        ])

        trans = transform.EuclideanTransform(matrix=matrix_translate)

        imgTranslate = transform.warp(img, trans.inverse)

        self.image = imgTranslate
        self.ax.clear()
        self.ax.axis("off")
        self.ax.imshow(self.image)
        self.canvas.draw_idle()

    def rotation(self, degrees):
        imgRot = np.array(rotate(self.image, int(degrees.get()) - self.histRotate), dtype=type(self.image[0, 0, 0]))
        self.histRotate = int(degrees.get())
        self.image = imgRot
        self.showCanvas(self.image)

    def flip(self, direction):
        imgFlip = np.zeros(self.image.shape, dtype=type(self.image[0, 0, 0]))
        for i in range(self.image.shape[0]):
            for j in range(self.image.shape[1]):

                if direction == "horizontal":
                    imgFlip[i, j, :] = self.image[i, -(j + 1), :]

                elif direction == "vertical":
                    imgFlip[i, j, :] = self.image[-(i + 1), j, :]

        self.image = imgFlip
        self.showCanvas(self.image)

    def mesclar(self, cbo, imgs, save):
        self.histImg = np.array(exposure.match_histograms(self.image, imgs[cbo.get()]), dtype=type(imgs[cbo.get()][0,0,0]))

        self.showCanvas(self.image)

    def mesclarImport(self):
        imgImport = ImageSystem.open_file(self)

        self.histImg = np.array(exposure.match_histograms(self.image, imgImport), dtype=type(imgImport[0,0,0]))
        self.showCanvas(self.histImg)
        
    def showCanvas(self, img):
        self.ax.clear()
        self.ax.axis("off")
        self.ax.imshow(img)
        self.canvas.draw_idle()

    def cancel(self):
        self.showCanvas(self.image)

    def apply(self):
        self.image = self.histImg
        self.showCanvas(self.image)

    def otsu(self):
        qPixels = self.image.size

        peso_media = 1.0/qPixels
        hist, bins = np.histogram(self.image, np.arange(0, 257))
        limiar = -1
        valor = -1
        intensidades = np.arange(256)

        for t in bins[1:-1]:
            pc1 = np.sum(hist[:t])
            pc2 = np.sum(hist[t:])
            peso1 = pc1 * peso_media
            peso2 = pc2 * peso_media

            mc1 = np.sum(intensidades[:t]*hist[:t])/pc1
            mc2 = np.sum(intensidades[t:]*hist[t:])/pc2

            temp = peso1 * peso2 * (mc1 - mc2) ** 2

            if temp > valor:
                limiar = t
                valor = temp
        
        classificada = self.image < limiar

        self.image = classificada - limiar
        self.showCanvas(self.image)

