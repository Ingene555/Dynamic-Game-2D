"""
Flippawns is a game about flipping pawns.
The goal is to turn them all black.
"""

from pyfunct import Assign, Sound, Temps, Cursor, WriteFile
from bubblewidgets import BubbleOval, BubbleTriangle, BubbleSquare, BubbleScale
from PIL import ImageTk, Image
from tkinter.font import Font
from tkinter import Canvas, Frame, Tk, Message as Msg, IntVar, Text, Scrollbar


class Flip(object):

    def __init__(self, master, top=None, classmaster=None, son=True):
        """All calculations are in this class"""
        self.master = master
        self.top = top
        self.clm = classmaster
        self.son = son

        self.wdt, self.hgt = eval(str(self.master['width'])), eval(str(self.master['height']))

        self.listobject = list()
        self.listhlines = list()
        self.listvlines = list()
        self.px, self.py = list(), list()
        self.x, self.y = list(), list()
        self.numx = 7
        self.numy = 4
        self.radius = self.wdt / self.numx - 15
        self.true = list()

        self.initw = self.wdt
        self.inith = self.hgt
        self.wd, self.hg = self.wdt, self.hgt
        self.initr = self.radius
        self.accesstouch = True
        self.after = None

        self.reset()
        Assign(self.master, self.onclic, ['Button-1'])

    def reset(self):
        if self.after:
            self.master.after_cancel(self.after)
            self.after = None
        self.master.delete('all')
        self.listobject = list()
        self.listhlines = list()
        self.listvlines = list()
        self.true = list()
        self.x = list()
        self.y = list()
        self.accesstouch = True
        
        self.square = self.master.create_rectangle(1, 1, self.wdt, self.hgt, fill='dark olive green', width=2)

        for ww in range(1, self.numx + 1):
            self.listvlines.append(self.master.create_line(self.wdt / self.numx * ww, 0, self.wdt / self.numx * ww, self.hgt, width=2, fill='white'))

        for ww in range(1, self.numy + 1):
            self.listhlines.append(self.master.create_line(0, self.hgt / self.numy * ww, self.wdt, self.hgt / self.numy * ww, width=2, fill='white'))
        for xx in range(1, self.numy + 1):
            l = []
            x = []
            y = []
            m = []
            for ww in range(1, self.numx + 1):
                l.append(BubbleOval(self.master, self.wdt / self.numx * ww - (self.radius + 15) / 2,
                                                  self.hgt / self.numy * xx - (self.radius + 15) / 2,
                                              width=self.radius, height=self.radius, son=False, bg='white',
                                                  og='grey90').circle)
                x.append(self.wdt / self.numx * ww - (self.radius + 15) / 2)
                y.append(self.hgt / self.numy * xx - (self.radius + 15) / 2)
                m.append(False)
                
            self.listobject.append(l)
            self.x.append(x)
            self.y.append(y)
            self.true.append(m)

    def setcolumn(self, value=7):
        #Create columns based on value
        self.numx = value
        a = self.wdt / self.numx - 15
        b = self.hgt / self.numy - 15
        if a > b:
            self.radius = b
        elif b > a:
            self.radius = a
        self.hgt = self.numy * (self.radius + 15)
        self.reset()
        self.hgt = self.inith
        self.hg = self.hgt

    def setrow(self, value=4):
        #Create columns based on value
        self.numy = value
        a = self.wdt / self.numx - 15
        b = self.hgt / self.numy - 15
        if a > b:
            self.radius = b
        elif b > a:
            self.radius = a
            
        self.wdt = self.numx * (self.radius + 15)
        self.reset()
        self.wdt = self.initw
        self.wd = self.wdt

    def restart(self):
        self.radius = self.initr
        self.wdt = self.initw
        self.hgt = self.inith
        self.numx = 7
        self.numy = 4
        self.reset()

    def win(self):
        self.accesstouch = False
        self.a = 0
        if self.son == True:
            Sound('audio\\flippawns\\1.mp3').play()
        self.animwin()
        f = open('data\\flippawns.dat', 'a')
        f.write(f'{Temps().temps()} {self.numx}x{self.numy} : Winner\n')
        f.close()
        f = open('data\\flippawns.dat', 'r')
        self.clm.thistory['stat'] = 'normal'
        self.clm.thistory.delete('0.0', 'end')
        self.clm.thistory.insert('end', str(f.read()))
        f.close()
        self.clm['stat'] = 'disabled'

    def animwin(self):
        #Board effect when the user wins
        l = ['white', 'black']
        if self.a > 1:
            self.a = 0
        for ww in self.listobject:
            for xx in ww:
                self.master.itemconfigure(xx, fill=l[self.a])
        self.a += 1
        self.after = self.master.after(400, self.animwin)

    def onclic(self, event=None):
        if self.accesstouch == True:
            obj = self.master.find_closest(event.x, event.y)
            for ww in self.listobject:
                if obj[0] in ww:
                    index1 = self.listobject.index(ww)
                    index2 = ww.index(obj[0])
                    for ww in range(-1, 2):
                        for xx in range(-1, 2):
                            try:
                                if index1 + ww < 0 or index1 + ww >= len(self.listobject) or index2 + xx < 0 or index2 + xx >= len(self.listobject[ww]):
                                    pass
                                else:
                                    a = self.listobject[index1 + ww][index2 + xx]
                                    if a != self.listobject[index1][index2]:
                                        if self.true[index1 + ww][index2 + xx] == True:
                                            self.master.itemconfigure(a, fill='white')
                                            self.true[index1 + ww][index2 + xx] = False
                                        elif self.true[index1 + ww][index2 + xx] == False:
                                            self.master.itemconfigure(a, fill='black')
                                            self.true[index1 + ww][index2 + xx] = True
                                    else:pass
                            except: pass
                    wdi = 0
                    for ww in self.true:
                        for xx in ww:
                            if xx == True:
                                wdi += 1
                    if wdi == self.numx * self.numy:
                        self.win()
                        break
                    break


class Pawns(Canvas):

    def __init__(self, master, top=None, sound=True, **cnf):
        """Interface is created here"""
        Canvas.__init__(self, master, **cnf)
        self.master = master
        self.top = top
        self.sound = sound
        self.son = Sound('audio\\default3.mp3')
        self.final = Sound('audio\\beta home page.mp3')
        self.son.play(400)
        self.playtest()
        self.varcol = IntVar(value=7); self.varrow = IntVar(value=4)

        self.config(bg='black', bd=0, highlightthickness=0, relief='flat',
                    width=master.winfo_screenwidth(), height=master.winfo_screenheight())

        self.swdt, self.shgt = eval(str(self['width'])), eval(str(self['height']))

        image = Image.open('media\\flippawns\\icon.png')  # Image
        self.image = image.resize((400, 190))
        self.image = ImageTk.PhotoImage(self.image)
        self.create_image(self.swdt / 2, 100, image=self.image)
        image.close()

        self.create_text(self.swdt / 2, 220, text='Flip Pawns', fill='light blue',
                         font=Font(family='Gameplay', size=30, weight='bold', underline=True))  # text contain
        BubbleTriangle(self, 200, 350, width=300, height=100, text='Play', bg='dark blue', fg='light blue',
                       og='dark blue', font=['helvetica', 20, 'bold'], mode='left', command=self.game)
        
        BubbleTriangle(self, 200, 410, width=300, height=100, text='Continue', bg='dark blue', fg='light blue',
                       og='dark blue', font=['helvetica', 20, 'bold'], mode='right', command=self.continuegamecommand)

        BubbleTriangle(self, 200, 470, width=300, height=100, text='History', bg='dark blue', fg='light blue',
                       og='dark blue', font=['helvetica', 20, 'bold'], mode='left', command=self.setpar)

        BubbleTriangle(self, 200, 530, width=300, height=100, text='Quit', bg='dark red', fg='light blue',
                       og='dark red', font=['helvetica', 20, 'bold'], mode='right', command=self.onclicquit)

        self.pvol = BubbleSquare(self, self.swdt - 45, self.shgt - 45, width=70, height=70, bg='black',
                                 fg='light blue', text='', font=['helvetica', 45], command=self.onclicvol)

        f = open('text\\flippawns\\idetails.txt', 'r')
        self.msg = Msg(self, width=400, bg='black', fg='white', bd=0, highlightthickness=0, text=f.read(),
                       font=Font(size=11, slant='italic'))
        f.close()
        self.msg.place(x=self.swdt / 2 - 200, y=300)

        self.frm = Frame(self, bg='black', bd=0, highlightthickness=0, relief='flat',
                          width=10, height=50)
        self.frm.place(x=self.swdt - 370, y=200)

        self.verpar = False
        self.verpar2 = False
        self.vergame = False
        self.vergame2 = False
        self.setpar()

    def onclicvol(self, event=None, son=None):
        if son:
            self.sound = son
            
        if self.sound == True:
            self.itemconfigure(self.pvol.title, text='')
            self.sound = False
            self.flip.son = False
            self.son.volm()
            
        else:
            self.itemconfigure(self.pvol.title, text='')
            self.sound = True
            self.flip.son = True
            self.son.volp()

    def onclicquit(self, event=None):
        self.son.stop()
        self.final.play()
        self.destroy()
        Cursor('media\\cursor\\cursor.cur')

    def playtest(self, event=None):
        if self.sound == True:
            self.son.volp()
        elif self.sound == False:
            self.son.volm()

    def game(self, event=None):  #Play option
        if self.vergame == False:
            self.vergame = True
            self.vergame2 = True
            self.frame = Frame(self, bg='black', bd=0, highlightthickness=0, relief='flat',
                               width=self['width'], height=self['height'])

            self.frame1 = Canvas(self.frame, bg='grey5', bd=0, highlightthickness=0, relief='flat',
                                width=self['width'], height=self.shgt / 11)
            self.frame1.grid(row=1, column=1, sticky='ew')
            x1, y1 = int(eval(str(self.frame1['width']))), int(eval(str(self.frame1['height'])))

            self.can = Canvas(self.frame, bg='black', bd=0, highlightthickness=0, relief='flat',
                              width=1000, height=600)
            self.can.grid(row=2, column=1, padx=int((self.swdt - 900) / 2),
                          pady=int((self.shgt - eval(str(self.frame1['height'])) - 580) / 2.5))
            self.frame['width'], self.frame['height'] = self.swdt, self.shgt

            self.frame.place(x=0, y=0)
            
            self.flip = Flip(self.can, self.master, classmaster=self)
            self.flip.wdt = eval(str(self.can['width'])); self.flip.hgt = eval(str(self.can['height']))
            self.flip.restart()

            wdt, hgt = int(y1 * .5) + y1 // 2 - int(y1 * .5) - y1 // 2, y1 / 2 + 10 + y1 // 2 - y1 / 2 + 10 - y1 // 2
            
            BubbleSquare(self.frame1, int(y1 * .5), y1 / 2 + 10, width=wdt, height=hgt, text='', fg='red',
                            bg='grey5', font=['helvetica', y1 // 2, 'bold'], command=self.quitgamecommand)

            BubbleSquare(self.frame1, int(y1 * 1.5), y1 / 2 + 10, width=wdt, height=hgt, text='', fg='light blue',
                            bg='grey5', font=['helvetica', y1 // 2, 'bold'], command=self.uselessplacecircle)

            self.audiogame = BubbleSquare(self.frame1, int(y1 * 2.5), y1 / 2 + 10, width=wdt, height=hgt, text='', fg='light blue',
                            bg='grey5', font=['helvetica', y1 // 2, 'bold'], command=self.audiogamecommand)
            if self.sound == False:
                self.frame1.itemconfigure(self.audiogame.title, text='')

            self.frame1.create_text(x1 - 50 - 100, 10, text='Column', fill='light yellow', font=Font(size='9', underline=True))

            self.frame1.create_text(x1 - 70 - 300, 10, text='Row', fill='light yellow', font=Font(size='9', underline=True))

            self.scol = BubbleScale(self.frame1, x1 - 50 - 100, 50, from_=2, to=50,
                                    value=7, variable=self.varcol, command=self.setcol, fg='purple')
            self.srow = BubbleScale(self.frame1, x1 - 70 - 300, 50, from_=2, to=50,
                                    value=4, variable=self.varrow, command=self.setrow, fg='purple')
            
            self.uselessplacecircle()
            
        if self.vergame == True:
            self.uselessplacecircle()
            if self.vergame2 == True:
                self.frame.place_forget()
                self.vergame2 = False
            elif self.vergame2 == False:
                self.frame.place(x=0, y=0)
                self.vergame2 = True

    def continuegamecommand(self):
        if self.vergame == True:
            if self.vergame2 == True:
                self.frame.place_forget()
                self.vergame2 = False
            elif self.vergame2 == False:
                self.frame.place(x=0, y=0)
                self.vergame2 = True
        else:
            self.game()

    def quitgamecommand(self, event=None):  # Leave Flippawns game
        self.vergame2 = False
        self.frame.place_forget()
        Cursor('media\\cursor\\cursor.cur')

    def uselessplacecircle(self):
        del(self.flip.listobject[:])
        for xx in range(1, self.flip.numy + 1):
                l = []
                for ww in range(1, self.flip.numx + 1):
                    l.append(BubbleOval(self.can, self.flip.x[xx - 1][ww - 1],
                                                  self.flip.y[xx - 1][ww - 1],
                                              width=self.flip.radius, height=self.flip.radius, son=False, bg='white',
                                                  og='grey90').circle)
                self.flip.listobject.append(l)

    def audiogamecommand(self, event=None):
        if self.flip.son == True:
            self.flip.son = False
            self.frame1.itemconfigure(self.audiogame.title, text='')
            self.sound = False
            self.son.volm()
            self.itemconfigure(self.pvol.title, text='')
        elif self.flip.son == False:
            self.flip.son = True
            self.frame1.itemconfigure(self.audiogame.title, text='')
            self.sound = True
            self.son.volp()
            self.itemconfigure(self.pvol.title, text='')

    def restart(self):
        self.flip.restart()
        self.scol.value = 7
        self.srow.value = 4
        self.scol.default_position()
        self.srow.default_position()

    def setcol(self):
        self.flip.setcolumn(self.varcol.get())
        self.uselessplacecircle()

    def setrow(self):
        self.flip.setrow(self.varrow.get())
        self.uselessplacecircle()

    def setpar(self, event=None):  # history options
        if self.verpar == False:
            self.verpar = True
            self.verpar2 = True
            
            frame = self.frm
            frame.config(bg='grey20', width=300, height=500)
            can = Canvas(frame, bg='grey30', bd=0, highlightthickness=0, relief='flat',
                         width=250, height=50)
            can.grid(row=1, column=1, sticky='ew', columnspan=2)
            can.create_text(250 / 2, 25, text='History', fill='light blue',
                            font=Font(family='helvetica', size=14, underline=True))

            self.thistory = Text(frame, width=int(35), height=20, bg='grey10', fg='light blue', cursor='circle blue',
                                 bd=0, highlightthickness=0, relief='flat', selectbackground='grey10', stat='disabled',
                                 selectforeground='light blue', font=Font(family='Callibri', size=8))

            bar = Scrollbar(frame, activebackground='grey15', activerelief='flat', background='grey10', bd=0,
                            bg='grey10', borderwidth=0, command=self.thistory.yview, elementborderwidth=0,
                            highlightbackground='grey15', highlightcolor='grey10', highlightthickness=0,
                            relief='flat', troughcolor='grey10', width=13)

            self.thistory['yscrollcommand'] = bar.set

            self.thistory.grid(row=2, column=1, sticky='nsew')
            bar.grid(row=2, column=2, sticky='ns')
            text = can.create_text(15, 25, text='', fill='red', font=Font(size=14))
            self.tdelhistory = text
            self.tcanhistory = can

            try:
                f = open('data\\flippawns.dat', 'r')
                l = f.read()
            except:
                f = open('data\\flippawns.dat', 'a')
                f.close()
                l = '<EMPTY>'
            self.thistory['stat'] = 'normal'
            self.thistory.delete('0.0', 'end')
            self.thistory.insert('end', l)
            self.thistory['stat'] = 'disabled'
            WriteFile('data\\fpstat.dat', '')

            can.tag_bind(text, '<Enter>', self.indelhistory)
            can.tag_bind(text, '<Leave>', self.outdelhistory)
            can.tag_bind(text, '<Button-1>', self.onclicdelhistory)
            
            self.frm.place(x=self.swdt - 370, y=200)
            
        if self.verpar == True:
            if self.verpar2 == False:
                self.frm.place(x=self.swdt - 370, y=200)
                self.verpar2 = True
            elif self.verpar2 == True:
                self.frm.place_forget()
                self.verpar2 = False

    def indelhistory(self, event=None):
        self.tcanhistory.itemconfigure(self.tdelhistory, font=Font(size=17))
        Cursor('media\\cursor\\hand.cur')
        Sound('audio\\motioneffect1.mp3').play()

    def outdelhistory(self, event=None):
        self.tcanhistory.itemconfigure(self.tdelhistory, font=Font(size=14))
        Cursor('media\\cursor\\cursor.cur')
        Sound('audio\\motioneffect2.mp3').play()

    def onclicdelhistory(self, event=None):
        self.thistory['stat'] = 'normal'
        self.thistory.delete('0.0', 'end')
        self.thistory.insert('end', '<EMPTY>')
        self.thistory['stat'] = 'disabled'
        f = open('data\\flippawns.dat', 'w')
        f.write('')
        f.close()


if __name__ == '__main__':
    fen = Tk()
    fen.wm_attributes('-fullscreen', True)
    can = Canvas(fen, width=1000, height=600, bg='white')
    can.pack
    b = Flip(can, fen)
    a = Pawns(fen)
    a.pack()
    fen.mainloop()
    Cursor()

