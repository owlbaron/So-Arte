from tkinter import *

from numpy.lib import utils

class Utils:
    @staticmethod
    def close_all(tela):
        tela.destroy()
        quit()
