"""Dynamic Games DG2D 1.0
by Cled
16th Nov 2023"""

from pyfunct import Cursor, Sound
from functions import *
from tkinter import PhotoImage, Tk, Frame, Canvas
import flippawns as flp
import golddigger as god
import morpion as mop
import pingpong as pnp
import snake as snk
import os
from tkinter.font import Font
import ctypes

     
def quit(root, master=None, sound=None):
    root.destroy()


def soon(a=None, b=None, c=None):
    None


if __name__ == "__main__":
    root = Tk()
    root['bg'] = 'black'
    root.title('Dynamic Games')
    root.iconphoto(False, PhotoImage(file='media\\icons\\icon.png'))
    root.wm_attributes('-fullscreen', True)
    curseur = Cursor('media\\cursor\\cursor.cur')

    can = Canvas(root, width=root.winfo_width() + 200, height=root.winfo_height(),
                 bg='black', bd=0, relief='flat', highlightthickness=0)
    can.grid(sticky='nsew')
    root.grid_rowconfigure(0, minsize=root.winfo_height())
    frame = Frame(can, width=can['width'], bg='grey5', bd=0, relief='flat', highlightthickness=0,
                                   height=int(eval(str(can['height'])) * 10 / 100))
    frame.grid(row=0, column=1, columnspan=4, sticky='ew')
                  
    media = ['media\\pingpong\\icon.png',
           'media\\flippawns\\icon.png',
           'media\\golddigger\\icon.png',
           'media\\morpion\\icon.png',
           'media\\snake\\icon.png',
           'media\\comingsoon\\icon.png',
           'media\\leave\\icon.png']
    title = ['Ping Pong', 'Fip pawns', 'Golddiger', 'Morpion',
           'Snake', 'Coming soon', 'Leave']
    details = ['Ping Pong game 1.0\nPlayable in solo or with a friend',
             'Flip all pawns and set them the same color',
             'Catch gold fallen with your pot',
             'A classical Morpion game',
             'Classical snake game',
             'An upgrade will be available soon',
             'Leave Dynamic Game 2D']
    cls = [pnp.Pong,
           flp.Pawns,
           god.Digger,
           mop.Pion,
           snk.Snake,
           soon,
           quit]

    a = 1
    b = 1
    ss = None

    def t(x):
        global ss
        if ss:
            ss.stop()
        a = x(root, root)
        if a:
            son.stop()
            ss = a.final
            a.place(x=1, y=1)
        elif a == "soon":
            ss = Sound('audio\\beta home page.mp3')
            ss.play(loop=200)

    for ww in range(1, len(media) + 1):
        if a > 2:
            a = 1
            b += 1
        x = int(eval(str(can['width'])) * a / 3)
        y = int(eval(str(can['height'])) * b / 2)
        c = SquareImage(can, media[ww - 1], command=lambda arg=ww - 1: t(cls[arg]))
        c.label['text'] = title[ww - 1]
        c.text['text'] = details[ww - 1]
        c.grid(row=b, column=a, sticky='nsew', padx=300, pady=25)
        a += 1

    image = Image.open('media\\icons\\icon 1080x1080.png')
    image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    image = ImageTk.PhotoImage(image)
    can.create_image(eval(str(can['width'])) / 2, eval(str(can['height'])) / 2, image=image)
        
    son = Sound('audio\\beta home page.mp3')
    son.play(loop=200)
    if os.name == "nt":
        FR_PRIVATE = 0x10
        ctypes.windll.gdi32.AddFontResourceExW(os.path.abspath("font/gameplay/gameplay.ttf"), FR_PRIVATE, 0)
    root.mainloop()
    son.stop()
    
    curseur.setdefault()

