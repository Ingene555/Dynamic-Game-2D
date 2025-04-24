from pyfunct import Temps, Assign, Unassign, Sound, WriteFile, Cursor
from bubblewidgets import BubbleTriangle, BubbleSquare, BubbleScale
from random import randrange
from tkinter import Canvas, Message as Msg, Frame, IntVar, Text, Scrollbar, Tk
from PIL import Image, ImageTk
from tkinter.font import Font
from math import inf


class Binary:

    def __init__(self, master, top=None, classmaster=None, son=True, mode='normal'):
        """All calculations are in this class"""
        self.master = master
        self.top = top
        self.clm = classmaster
        self.son = son
        self.mode = mode

    def binary(self, event=None):
        self.wdt, self.hgt = 1000, 600
        self.x = self.wdt / 2; self.y = self.hgt / 2
        self.convert = 1000 / 50
        self.speed = 150

        self.rad = self.convert / 2
        self.dia = self.convert

        self.snake = [[self.x, self.y], [self.x - self.dia, self.y], [self.x - self.dia * 2, self.y]]
        self.coords = self.snake.copy()

        self.dx = self.dia
        self.dy = 0

        self.bc = [randrange(50) * self.convert, randrange(int(self.hgt / 50)) * self.convert]

        self.balle = self.master.create_oval(self.bc[0], self.bc[1],
                                             self.bc[0] + self.dia, self.bc[1] + self.dia,
                                             fill='#898999')
        self.square = []
        for ww in self.snake:
            self.square.append(self.master.create_rectangle(ww[0], ww[1],
                                                            ww[0] + self.dia, ww[1] + self.dia,
                                                            fill='navy blue', width=0, outline='white'))
        self.master.itemconfigure(self.square[0], fill='#444499', outline='#454599', width=1)
        self.textfail = self.master.create_text(self.x, self.y - 50, text='click to start',
                                                font='gameplay 50 bold', fill='white')

        self.dir = 'e'
        self.pause = True

        if self.top:
            Assign(self.top, self.up, ['Up'])
            Assign(self.top, self.down, ['Down'])
            Assign(self.top, self.left, ['Left'])
            Assign(self.top, self.right, ['Right'])
        Assign(self.master, self.pauseplay, ['Button-1'])

    def go(self, event=None):
        if self.pause == False:
            if self.dir == 'n':
                self.dy = -self.dia
                self.dx = 0
                self.x = self.snake[0][0]

            elif self.dir == 's':
                self.dy = self.dia
                self.dx = 0
                self.x = self.snake[0][0]

            elif self.dir == 'e':
                self.dx = self.dia
                self.dy = 0
                self.y = self.snake[0][1]

            elif self.dir == 'w':
                self.dx = -self.dia
                self.dy = 0
                self.y = self.snake[0][1]

            x = self.snake[0][0] + self.dx
            y = self.snake[0][1] + self.dy
            self.coords.reverse()
            self.coords.append([x, y])
            self.coords.reverse()

            for ww in range(len(self.snake)):
                self.snake[ww] = self.coords[ww]
            self.check_echec()
                
            return self.snake

    def up(self, event=None):
        if self.pause == False:
            if self.dir != 's':
                self.dir = 'n'

    def down(self, event=None):
        if self.pause == False:
            if self.dir != 'n':
                self.dir = 's'

    def left(self, event=None):
        if self.pause == False:
            if self.dir != 'e':
                self.dir = 'w'

    def right(self, event=None):
        if self.pause == False:
            if self.dir != 'w':
                self.dir = 'e'

    def check_echec(self):
        self.master.lift(self.square[0])
        self.master.lift(self.balle)
        a = self.snake[0]
        for ww in self.snake[1:]:
            if ww == a:
                self.echec()
                
        if self.mode == 'normal':
            if a[0] < 0 or a[1] < 0 or a[0] >= self.wdt or a[1] >= self.hgt:
                self.echec()
        else:
            a = self.snake[0]
            if a[0] >= self.wdt:
                a[0] = 0
            if a[0] < 0:
                a[0] = self.wdt - self.dia
            if a[1] >= self.hgt:
                a[1] = 0
            if a[1] < 0:
                a[1] = self.hgt - self.dia

    def echec(self):
        self.pause = True
        if self.son == True:
            Sound('audio\\snake\\2.mp3').play()
        self.master.itemconfigure(self.textfail, text='😓', fill='red', font='cube 200')
        f = open('data\\snake.dat', 'a')
        f.write(f'{Temps().temps()} #score: {len(self.square)-3}\n')
        f.close()
        self.clm.thistory['stat'] = 'normal'
        f = open('data\\snake.dat', 'r')
        self.clm.thistory.delete('0.0', 'end')
        self.clm.thistory.insert('end', f.read())
        f.close()
        self.clm.thistory['stat'] = 'disabled'
        self.master.after(1000, self.reset)

    def check_ball(self):
        if self.snake[0] == self.bc:
            self.bc = [randrange(50) * self.convert, randrange(int(self.hgt / 50)) * self.convert]
            self.master.coords(self.balle, self.bc[0], self.bc[1],
                                             self.bc[0] + self.dia, self.bc[1] + self.dia)
            if self.son == True:
                Sound('audio\\snake\\1.mp3').play()
            self.add_square()

    def movecontinue(self, event=None):
        if self.pause == False:
            self.master.itemconfigure(self.textfail, text='', fill='red', font='cube 50 bold')
            self.go()
            for ww in range(len(self.square)):
                self.master.coords(self.square[ww], self.snake[ww][0], self.snake[ww][1],
                                   self.snake[ww][0] + self.dia, self.snake[ww][1] + self.dia)
            self.check_ball()
            self.master.after(self.speed, self.movecontinue)
            
    def pauseplay(self, event=None):
        if self.pause == True:
            self.pause = False
            if self.top:
                Assign(self.top, self.up, ['Up'])
                Assign(self.top, self.down, ['Down'])
                Assign(self.top, self.left, ['Left'])
                Assign(self.top, self.right, ['Right'])
            else:
                Assign(self.master, self.up, ['Up'])
                Assign(self.master, self.down, ['Down'])
                Assign(self.master, self.left, ['Left'])
                Assign(self.master, self.right, ['Right'])
            self.movecontinue()
        elif self.pause == False:
            self.pause = True
            self.master.itemconfigure(self.textfail, text='click to continue', fill='white', font='cube 50 bold')
            WriteFile('data\\snstat.dat', self.snake)

    def add_square(self, event=None):
        a = len(self.square)
        self.snake.append(self.coords[a])
        b = self.snake[a]
        self.square.append(self.master.create_rectangle(b[0], b[1], b[0] + self.dia, b[1] + self.dia,
                                                        fill='navy blue', width=0, outline='white'))

    def reset(self):
        self.master.delete('all')
        self.binary()

    def quit(self):
        if self.top:
            Unassign(self.top, ['Up', 'Down', 'Left', 'Right'])
        else:
            Unassign(self.master, ['Up', 'Down', 'Left', 'Right'])

    def setspeed(self, value=0):
        self.speed = 150 - value


class Snake(Canvas):

    def __init__(self, master, top=None, sound=True, **cnf):
        """The interface is created here"""
        Canvas.__init__(self, master, **cnf)
        self.master = master
        self.top = top
        self.sound = sound
        self.final = Sound('audio\\beta home page.mp3')
        self.son = Sound('audio\\default5.mp3')
        self.son.play(3)
        self.playtest()

        self.config(bg='black', bd=0, highlightthickness=0, relief='flat',
                    width=master.winfo_screenwidth(), height=master.winfo_screenheight())

        self.swdt, self.shgt = eval(str(self['width'])), eval(str(self['height']))

        imag = Image.open('media\\snake\\icon.png')
        self.image = imag.resize((400, 190))
        self.image = ImageTk.PhotoImage(self.image)
        self.create_image(self.swdt / 2, 100, image=self.image)
        imag.close()

        self.create_text(self.swdt / 2, 220, text='Snake', fill='light blue',
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

        f = open('text\\snake\\idetails.txt', 'r')
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
            self.binary.son = False
            self.son.volm()
            
        else:
            self.itemconfigure(self.pvol.title, text='')
            self.sound = True
            self.binary.son = True
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

            self.can = Canvas(self.frame, bg='black', bd=2, highlightthickness=2, relief='flat',
                              width=1000, height=600)
            self.can.grid(row=2, column=1, padx=int((self.swdt - 900) / 2),
                          pady=int((self.shgt - eval(str(self.frame1['height'])) - 580) / 2.5))
            self.frame['width'], self.frame['height'] = self.swdt, self.shgt

            self.frame.place(x=0, y=0)
            self.varspeed = IntVar(value=0)
            
            self.binary = Binary(self.can, self.top, classmaster=self)
            self.binary.wdt = 1000; self.binary.hgt = 600
            self.binary.reset()

            wdt, hgt = int(y1 * .5) + y1 // 2 - int(y1 * .5) - y1 // 2, y1 / 2 + 10 + y1 // 2 - y1 / 2 + 10 - y1 // 2
            
            BubbleSquare(self.frame1, int(y1 * .5), y1 / 2 + 10, width=wdt, height=hgt, text='', fg='red',
                            bg='grey5', font=['helvetica', y1 // 2, 'bold'], command=self.quitgamecommand)

            BubbleSquare(self.frame1, int(y1 * 1.5), y1 / 2 + 10, width=wdt, height=hgt, text='', fg='light blue',
                            bg='grey5', font=['helvetica', y1 // 2, 'bold'], command=self.uselessresetgame)

            self.bpause = BubbleSquare(self.frame1, int(y1 * 2.5), y1 / 2 + 10, width=wdt, height=hgt, text='', fg='light blue',
                            bg='grey5', font=['helvetica', y1 // 2, 'bold'], command=self.pausegamecommand)

            self.audiogame = BubbleSquare(self.frame1, int(y1 * 3.5), y1 / 2 + 10, width=wdt, height=hgt, text='', fg='light blue',
                            bg='grey5', font=['helvetica', y1 // 2, 'bold'], command=self.audiogamecommand)

            self.frame1.create_text(x1 - 50 - 100, 10, text='Speed', fill='light yellow', font=Font(size=9, underline=True))
            
            BubbleScale(self.frame1, x1 - 50 - 100, y1 / 2 + 10, variable=self.varspeed, command=self.setspeed, value=0,
                        from_=0, to=100, fg='purple')

            self.frame1.create_text(x1 - 300, 10, text='Boundary', fill='light yellow', font=Font(size=9, underline=True))

            self.sqrmode = BubbleSquare(self.frame1, x1 - 300, y1 / 2 + 10, text='Normal', og='grey2', command=self.mode,
                                        font=['helvetica', y1 // 6])
            self.sqrmode.auto_size()
            
            if self.sound == False:
                self.frame1.itemconfigure(self.audiogame.title, text='')
            self.uselessresetgame()
            
        if self.vergame == True:
            self.uselessresetgame()
            if self.vergame2 == True:
                self.frame.place_forget()
                self.vergame2 = False
            elif self.vergame2 == False:
                self.frame.place(x=0, y=0)
                self.vergame2 = True

    def setspeed(self, event=None):
        self.binary.reset()
        self.binary.setspeed(self.varspeed.get())

    def mode(self, event=None):
        self.binary.reset()
        if self.binary.mode == 'normal':
            self.binary.mode = inf
            self.frame1.itemconfigure(self.sqrmode.title, text='Illimited')
        else:
            self.binary.mode = 'normal'
            self.frame1.itemconfigure(self.sqrmode.title, text='Normal')
        self.sqrmode.auto_size()

    def pausegamecommand(self):
        self.binary.pauseplay()
        if self.binary.pause == True:
            self.can.itemconfigure(self.bpause.title, text='')
        elif self.binary.pause == False:
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

    def quitgamecommand(self, event=None):  # Leave snake game
        self.vergame2 = False
        self.binary.pause = False
        self.binary.pauseplay()
        self.binary.quit()
        self.frame.place_forget()
        Cursor('media\\cursor\\cursor.cur')

    def audiogamecommand(self, event=None):
        if self.binary.son == True:
            self.binary.son = False
            self.frame1.itemconfigure(self.audiogame.title, text='')
            self.sound = False
            self.son.volm()
            self.itemconfigure(self.pvol.title, text='')
        elif self.binary.son == False:
            self.binary.son = True
            self.frame1.itemconfigure(self.audiogame.title, text='')
            self.sound = True
            self.son.volp()
            self.itemconfigure(self.pvol.title, text='')
            
    def uselessresetgame(self, event=None):
        self.binary.reset()

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
                f = open('data\\snake.dat', 'r')
                l = f.read()
            except:
                f = open('data\\snake.dat', 'a')
                f.close()
                l = '<EMPTY>'
            self.thistory['stat'] = 'normal'
            self.thistory.delete('0.0', 'end')
            self.thistory.insert('end', l)
            self.thistory['stat'] = 'disabled'
            WriteFile('data\\snstat.dat', '')

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
        f = open('data\\snake.dat', 'w')
        f.write('')
        f.close()


if __name__ == '__main__':
    fen = Tk()
    fen['bg'] = 'dark grey'
    fen.wm_attributes('-fullscreen', True)
    can = Canvas(fen, width=1000, height=600, bg='black')
    can.pack

    a = Snake(fen, fen)
    a.pack()
    
    fen.mainloop()

    Cursor()

