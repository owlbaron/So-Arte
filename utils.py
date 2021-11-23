from tkinter import *

from numpy.lib import utils
import numpy as np

class Utils:
    @staticmethod
    def close_all(tela):
        tela.destroy()
        quit()
