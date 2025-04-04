"""This library will contain some functions used everywhere"""

from tkinter.colorchooser import askcolor
import pickle as pkl
import pygame   
from datetime import datetime
import ctypes

# Variables
NO = 'no'
NC = 'nc'
NE = 'ne'
SO = 'so'
SC = 'sc'
SE = 'se'
CO = 'co'
CE = 'ce'
CERCLE = 'cercle'
CARRE = 'carre'
POLYGONE = 'polygone'
ARC = 'arc'
LIGNE = 'ligne'
TEXTE = 'texte'
FENETRE = 'fenetre'
LISTE = 'liste'
ELEMENT = 'element'
DEVANT = 'first'
DERRIER = 'last'
TOUT = 'both'
PLUS = 'plus'
BARRE = 'barre'
AUCUN = 'aucun'
TEXTE = 'texte'
VAR = 'var'

VIDE = '\t\t\t\t\t'
pygame.init()


class Temps():

    def __init__(self):
        """Time  class
        """
        # I created this class long years ago, when i didn't know how to use correctly datetime
        self.temps_ = datetime.today()
        self.annee = self.temps_.year
        self.month = self.temps_.month
        self.j = self.temps_.day
        self.h = self.temps_.hour
        self.m = self.temps_.minute
        self.s = self.temps_.second
        self.ms = self.temps_.microsecond

    def temps(self):
        temps = ('{}.{}.{} {}:{} {}'.format(self.jour(), self.mois(), self.an(), self.heure(), self.minute(), self.seconde()))
        return temps

    def an(self):
        return self.annee

    def mois(self, n=True):
        dictio = {1:'January', 2:'Febuary', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September',
                10:'October', 11:'November', 12:'December'}
        if n is False:
            return dictio[eval(str(self.month))]
        elif n is True:
            return self.month

    def jour(self, n=True):
        liste = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        if n is False:
            return liste[self.temps_.weekday()]
        elif n is True:
            return self.j

    def heure(self):
        return self.h

    def minute(self):
        return self.m

    def seconde(self):
        return self.s

    def micros(self):
        return self.ms


class ReadFile(object):

    def __init__(self, fichier=None):
        f = open(fichier, 'rb')
        self.t = ''
        while True:
            try:
                self.t += str(pkl.load(f))
            except:
                f.close()
                break
        self.assigne()

    def assigne(self):
        return self.t


class WriteFile(object):

    def __init__(self, fichier=None, info=None):
        f = open(fichier, 'wb')
        pkl.dump(info, f)
        f.close()


class Get(object):

    def __init__(self, master):
        """This class gives back dimension of a widget"""
        self.master = master

    def x(self):
        return self.master.winfo_width()

    def y(self):
        return self.master.winfo_height()

    def width(self):
        return eval(str(self.master['width']))

    def height(self):
        return eval(str(self.master['height']))


class Assign(object):

    def __init__(self, mil, definit, touche=[]):
        """This class add one or many event to one widget"""
        self.m = mil
        self.d = definit
        self.t = touche
        for ww in self.t:
            self.m.bind('<{}>'.format(ww), self.d)

    def modifie(self, mil=None, definit=None, touche=[]):
        if mil != None:
            self.m = mil
        if definit != None:
            self.d = definit
        if touche != []:
            self.t = touche
        for ww in self.t:
            self.m.bind('<{}>'.format(ww), self.d)


class Unassign(object):

    def __init__(self, mil, touche=[], definit=None):
        """This class remove one or many event from one widget"""
        self.m = mil
        self.d = definit
        self.t = touche
        for ww in self.t:
            self.m.unbind('<%s>' % ww)

    def modifie(self, mil=None, definit=None, touche=[]):
        if mil != None:
            self.m = mil
        if definit != None:
            self.d = definit
        if touche != []:
            self.t = touche
        for ww in self.t:
            self.m.unbind('<{}>'.format(ww))


class Sound(object):

        def __init__(self, audio):
            """This class uses pygame to play sound"""
            pygame.mixer.init()
            self.audio = pygame.mixer.Sound(audio)
            self.audio.set_volume(1)

        def volp(self):
            self.audio.set_volume(1)

        def volm(self):
            self.audio.set_volume(0)

        def play(self, loop=0):
            self.audio.play(loops=loop)

        def stop(self):
            self.audio.stop()

        def delay(self, delai=1):
            pygame.time.delay(delai)

        def length(self):
            return self.audio.get_length()

        def get(self):
            return self.audio



class Cursor(object):

    def __init__(self, cursor="C:\\Windows\\Cursors\\arrow_r.cur"):
        """This class set cursor"""
        chemin_image_curseur = cursor
        user32 = ctypes.windll.user32
        user32.LoadCursorFromFileW.restype = ctypes.c_void_p
        curseur = user32.LoadCursorFromFileW(chemin_image_curseur)
        self.cur = curseur
        user32.SetSystemCursor(curseur, 32512)

    def setdefault(self):
        chemin_image_curseur = "C:\\Windows\\Cursors\\arrow_r.cur"
        user32 = ctypes.windll.user32
        user32.LoadCursorFromFileW.restype = ctypes.c_void_p
        curseur = user32.LoadCursorFromFileW(chemin_image_curseur)
        self.cur = curseur
        user32.SetSystemCursor(curseur, 32512)

    def setcursor(self, cursor="C:\\Windows\\Cursors\\arrow_r.cur"):
        chemin_image_curseur = cursor
        user32 = ctypes.windll.user32
        user32.LoadCursorFromFileW.restype = ctypes.c_void_p
        curseur = user32.LoadCursorFromFileW(chemin_image_curseur)
        self.cur = curseur
        user32.SetSystemCursor(curseur, 32512)


# Cursors
CURSORS = ['X_cursor', 'arrow', 'based_arrow_down', 'based_arrow_up', 'boat', 'bogosity',
          'bottom_left_corner', 'bottom_right_corner', 'bottom_side', 'bottom_tee', 'box_spiral',
          'center_ptr', 'circle', 'clock', 'coffee_mug', 'cross', 'cross_reverse', 'crosshair', 'diamond_cross',
          'dot', 'dotbox', 'double_arrow', 'draft_large', 'draft_small', 'draped_box', 'exchange', 'fleur', 'gobbler',
          'gumby', 'hand1', 'hand2', 'heart', 'icon', 'iron_cross', 'left_ptr', 'left_side', 'left_tee', 'leftbutton', 'll_angle',
          'lr_angle', 'man', 'middlebutton', 'mouse', 'pencil', 'pirate', 'plus', 'question_arrow', 'right_ptr', 'right_side',
          'right_tee', 'rightbutton', 'rtl_logo', 'sailboat', 'sb_down_arrow', 'sb_h_double_arrow', 'sb_left_arrow',
          'sb_right_arrow', 'sb_up_arrow', 'sb_v_double_arrow', 'shuttle', 'sizing', 'spider', 'spraycan', 'star', 'target',
          'tcross', 'top_left_arrow', 'top_left_corner', 'top_right_corner', 'top_side', 'top_tee', 'trek', 'ul_angle',
          'umbrella', 'ur_angle', 'watch', 'xterm']

