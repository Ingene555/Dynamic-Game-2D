"""
Golddigger is a game where you have to catch golden eggs with a basket.
"""

from pyfunct import Temps, Cursor, Assign, WriteFile, Sound
from bubblewidgets import BubbleTriangle, BubbleSquare
from tkinter.font import Font
from tkinter import Canvas, Tk, Frame, Text, Scrollbar, Message as Msg
from random import randrange
from PIL import Image, ImageTk


class Animation:

    def __init__(self, master, obj, direction='s', speed=10, op=None):
        # I forgot why i created this class but I think it's important
        self.master = master
        self.obj = obj
        self.dir = direction
        self.index = speed
        self.repeat = True
        self.after = None
        self.op = op
        self.anime()

    def anime(self):
        try:
            if self.dir == 's':
                self.master.move(self.obj, 0, self.index)
            elif self.dir == 'n':
                self.master.move(self.obj, 0, -self.index)
            elif self.dir == 'e':
                self.master.move(self.obj, self.index, 0)
            elif self.dir == 'w':
                self.master.move(self.obj, -self.index, 0)
            elif self.dir == 'se':
                self.master.move(self.obj, self.index, self.index)
            elif self.dir == 'ne':
                self.master.move(self.obj, self.index, -self.index)
            elif self.dir == 'sw':
                self.master.move(self.obj, -self.index, self.index)
            elif self.dir == 'nw':
                self.master.move(self.obj, -self.index, -self.index)
            if self.op:
                self.op += self.index
            if self.repeat == True:
                self.after = self.master.after(16, self.anime)
        except:
            self.stop()

    def stop(self):
        self.repeat = False
        # self.master.after_cancel(self.after)
        self.after = None

    def play(self):
        self.repeat = True
        self.anime()

    def chdir(self, direction='s'):
        self.dir = direction

    def chspeed(self, speed=10):
        self.index = speed

    def getop(self):
        return self.op


class Gold(object):

    def __init__(self, master, top=None, classmaster=None, son=True):
        """ All calculations are in this class"""
        self.master = master
        self.top = top
        self.clm = classmaster
        self.son = son
        self.wdt, self.hgt = eval(str(self.master['width'])), eval(str(self.master['height']))

        self.reset()
        
        Assign(self.master, self.cont, ['Button-1'])

    def reset(self, event=None):
        self.master.delete('all')
        self.pause = True
        
        self.x = self.wdt / 2; self.y = self.hgt - 25

        self.panier = self.master.create_polygon(self.x - 60, self.y - 25, self.x + 60, self.y - 25,
                                                 self.x + 45, self.y + 25, self.x - 45, self.y + 25,
                                                 fill='#805050', outline='grey55')
        self.line = self.master.create_line(self.x - 60, self.y - 25, self.x + 60, self.y - 25,
                                            fill='dark red', width=5, capstyle='round')
        self.txtscore = self.master.create_text(self.wdt - 5, 5, text=0, fill='white', font='gameplay 50', anchor='ne')
        self.score = 0

        self.textfail = self.master.create_text(self.wdt / 2, self.hgt / 2, fill='white', font='gameplay 50',
                                                text='Click to start')

        self.listegg = list()
        self.listcoordx = list()
        self.listcoordy = list()
        self.listanim = list()
        self.speed = 6
        
        Assign(self.master, self.movebasket, ['Motion'])

    def movebasket(self, event=None):
        if self.pause == False:
            a = event.x - self.x
            self.x += a
            self.master.move(self.panier, a, 0)
            self.master.move(self.line, a, 0)

    def fallgold(self, event=None):
        self.master.itemconfigure(self.textfail, text='', fill='red')
        if self.pause == False:
            self.add_egg()
            self.master.lift(self.panier)
            self.master.lift(self.line)
            self.master.after(int(15000 / self.speed), self.fallgold)

    def add_egg(self):
        x = randrange(20, self.wdt - 20)
        a = self.master.create_oval(x - 10, -45, x + 10, -5, fill='gold', outline='gold')
        self.listcoordx.append(x)
        self.listcoordy.append(-50 / 2)
        self.listanim.append(Animation(can, a, speed=self.speed, op=self.listcoordy[len(self.listcoordy) - 1]))
        self.listegg.append(a)

    def check_egg(self):
        for ww in self.listegg:
            a = self.listegg.index(ww)
            b = self.listanim[a].getop()
            c = self.listcoordx[a]
            if b >= self.hgt - 50:
                if not self.x - 60 <= c <= self.x + 60:
                    self.echec()
                    break
                else:
                    self.gatin(a)
            else:pass
        if self.pause == False:
            self.master.after(200, self.check_egg)

    def echec(self):
        self.pause = True
        self.master.itemconfigure(self.textfail, text='😓', fill='red', font='cube 200')
        for ww in self.listanim:
            ww.stop()
        if self.son == True:
            Sound('audio\\golddigger\\2.mp3').play()
        
        f = open('data\\golddigger.dat', 'a')
        f.write('%s #score: %s\n' % (Temps().temps(), self.score))
        f.close()
        self.clm.thistory['stat'] = 'normal'
        self.clm.thistory.insert('end', '%s #score: %s\n' % (Temps().temps(), self.score))
        self.clm.thistory['stat'] = 'disabled'
        self.master.after(1500, self.reset)

    def gatin(self, index):
        self.master.delete(self.listegg[index])
        del(self.listegg[index])
        del(self.listcoordx[index])
        del(self.listcoordy[index])
        del(self.listanim[index])
        self.score += 1
        self.master.itemconfigure(self.txtscore, text=self.score)
        self.speed += .05
        for ww in self.listanim:
            ww.index = self.speed
        if self.son == True:
            Sound('audio\\golddigger\\1.mp3').play()

    def cont(self, event=None):
        if self.pause == True:
            self.pause = False
            for ww in self.listanim:
                ww.play()
            self.fallgold()
            self.check_egg()
            self.clm.can.itemconfigure(self.textfail, fill='white', font='gameplay 48',
                                                text='')

        elif self.pause == False:
            self.pause = True
            for ww in self.listanim:
                ww.stop()
            self.clm.can.itemconfigure(self.textfail, fill='white', font='gameplay 45',
                                                text='Click to continue')
            self.clm.can.lift(self.textfail)


class Digger(Canvas):

    def __init__(self, master, top=None, sound=True, **cnf):
        """The interface is created here"""
        Canvas.__init__(self, master, cnf)
        self.master = master
        self.top = top
        self.sound = sound
        self.son = Sound('audio\\default4.mp3')
        self.final = Sound('audio\\beta home page.mp3')
        self.son.play(400)
        self.playtest()

        self.config(bg='black', bd=0, highlightthickness=0, relief='flat',
                    width=master.winfo_screenwidth(), height=master.winfo_screenheight())

        self.swdt, self.shgt = eval(str(self['width'])), eval(str(self['height']))

        imag = Image.open('media\\golddigger\\icon.png')
        self.image = imag.resize((400, 190))
        self.image = ImageTk.PhotoImage(self.image)
        self.create_image(self.swdt / 2, 100, image=self.image)
        imag.close()

        self.create_text(self.swdt / 2, 220, text='Gold Digger', fill='light blue',
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

        f = open('text\\golddigger\\idetails.txt', 'r')
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
        self.game()
        self.setpar()

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

    def onclicvol(self, event=None, son=None):
        if son:
            self.sound = son
            
        if self.sound == True:
            self.itemconfigure(self.pvol.title, text='')
            self.sound = False
            self.gold.son = False
            self.son.volm()
            
        else:
            self.itemconfigure(self.pvol.title, text='')
            self.sound = True
            self.gold.son = True
            self.son.volp()

    def game(self, event=None):
        if self.vergame == False:
            self.vergame = True
            self.vergame2 = True
            self.frame = Frame(self, bg='black', bd=0, highlightthickness=0, relief='flat',
                               width=self['width'], height=self['height'])

            self.frame1 = Canvas(self.frame, bg='grey5', bd=0, highlightthickness=0, relief='flat',
                                width=self['width'], height=self.shgt / 11)
            self.frame1.grid(row=1, column=1, sticky='ew')
            x1, y1 = int(eval(str(self.frame1['width']))), int(eval(str(self.frame1['height'])))
            x1

            self.can = Canvas(self.frame, bg='black', bd=2, highlightthickness=2, relief='flat',
                              width=1000, height=600)
            self.can.grid(row=2, column=1, padx=int((self.swdt - 900) / 2),
                          pady=int((self.shgt - eval(str(self.frame1['height'])) - 580) / 2.5))
            self.frame['width'], self.frame['height'] = self.swdt, self.shgt

            self.frame.place(x=0, y=0)
            
            self.gold = Gold(self.can, self.master, classmaster=self)
            self.gold.wdt = 1000; self.gold.hgt = 600

            wdt, hgt = int(y1 * .5) + y1 // 2 - int(y1 * .5) - y1 // 2, y1 / 2 + 10 + y1 // 2 - y1 / 2 + 10 - y1 // 2
            
            BubbleSquare(self.frame1, int(y1 * .5), y1 / 2 + 10, width=wdt, height=hgt, text='', fg='red',
                            bg='grey5', font=['helvetica', y1 // 2, 'bold'], command=self.quitgamecommand)

            BubbleSquare(self.frame1, int(y1 * 1.5), y1 / 2 + 10, width=wdt, height=hgt, text='', fg='light blue',
                            bg='grey5', font=['helvetica', y1 // 2, 'bold'], command=self.uselessresetgame)

            self.bpause = BubbleSquare(self.frame1, int(y1 * 2.5), y1 / 2 + 10, width=wdt, height=hgt, text='', fg='light blue',
                            bg='grey5', font=['helvetica', y1 // 2, 'bold'], command=self.pausegamecommand)

            self.audiogame = BubbleSquare(self.frame1, int(y1 * 3.5), y1 / 2 + 10, width=wdt, height=hgt, text='', fg='light blue',
                            bg='grey5', font=['helvetica', y1 // 2, 'bold'], command=self.audiogamecommand)
            if self.sound == False:
                self.frame1.itemconfigure(self.audiogame.title, text='')
            self.gold.add_egg = self.uselessadd_egg
            self.uselessresetgame()
            
        if self.vergame == True:
            self.uselessresetgame()
            if self.vergame2 == True:
                self.frame.place_forget()
                self.vergame2 = False
            elif self.vergame2 == False:
                self.frame.place(x=0, y=0)
                self.vergame2 = True

    def pausegamecommand(self):
        self.gold.cont()
        if self.gold.pause == True:
            self.can.itemconfigure(self.bpause.title, text='')
        elif self.gold.pause == False:
            self.can.itemconfigure(self.bpause.title, text='')

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

    def quitgamecommand(self, event=None):  # Leave golddiger game
        self.vergame2 = False
        self.gold.pause = False
        self.gold.cont()
        for ww in self.gold.listanim:
            ww.stop()
        self.frame.place_forget()
        Cursor('media\\cursor\\cursor.cur')

    def audiogamecommand(self, event=None):
        if self.gold.son == True:
            self.gold.son = False
            self.frame1.itemconfigure(self.audiogame.title, text='')
            self.sound = False
            self.son.volm()
            self.itemconfigure(self.pvol.title, text='')
        elif self.gold.son == False:
            self.gold.son = True
            self.frame1.itemconfigure(self.audiogame.title, text='')
            self.sound = True
            self.son.volp()
            self.itemconfigure(self.pvol.title, text='')
            
    def uselessresetgame(self, event=None):
        self.can.delete('all')
        self.gold.pause = True
        
        self.gold.x = self.gold.wdt / 2; self.gold.y = self.gold.hgt - 25

        self.gold.panier = self.can.create_polygon(self.gold.x - 60, self.gold.y - 25, self.gold.x + 60, self.gold.y - 25,
                                                 self.gold.x + 45, self.gold.y + 25, self.gold.x - 45, self.gold.y + 25,
                                                 fill='#805050', outline='grey55')
        self.gold.line = self.can.create_line(self.gold.x - 60, self.gold.y - 25, self.gold.x + 60, self.gold.y - 25,
                                            fill='dark red', width=5, capstyle='round')
        self.gold.txtscore = self.can.create_text(self.gold.wdt - 5, 5, text=0, fill='white', font='gameplay 50', anchor='ne')
        self.gold.score = 0

        self.gold.textfail = self.can.create_text(self.gold.wdt / 2, self.gold.hgt / 2, fill='white', font='gameplay 50',
                                                text='Click to start')

        self.gold.listegg = list()
        self.gold.listcoordx = list()
        self.gold.listcoordy = list()
        self.gold.listanim = list()
        self.gold.speed = 6
        Assign(self.can, self.gold.movebasket, ['Motion'])

    def uselessadd_egg(self):
        x = randrange(20, self.gold.wdt - 20)
        a = self.can.create_oval(x - 10, -45, x + 10, -5, fill='gold', outline='gold')
        self.gold.listcoordx.append(x)
        self.gold.listcoordy.append(-50 / 2)
        self.gold.listanim.append(Animation(self.can, a, speed=self.gold.speed, op=self.gold.listcoordy[len(self.gold.listcoordy) - 1]))
        self.gold.listegg.append(a)

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
                f = open('data\\golddigger.dat', 'r')
                l = f.read()
            except:
                f = open('data\\golddigger.dat', 'a')
                f.close()
                l = '<EMPTY>'
            self.thistory['stat'] = 'normal'
            self.thistory.delete('0.0', 'end')
            self.thistory.insert('end', l)
            self.thistory['stat'] = 'disabled'
            WriteFile('data\\gdstat.dat', '')

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
        f = open('data\\golddigger.dat', 'w')
        f.write('')
        f.close()


if __name__ == '__main__':
    fen = Tk()
    fen['bg'] = 'dark grey'
    fen.wm_attributes('-fullscreen', True)
    can = Canvas(fen, width=1000, height=600, bg='black')
    can.pack()
    a = Digger(can, fen)
    a.pack()
    fen.mainloop()

    Cursor()

