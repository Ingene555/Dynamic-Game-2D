"""Tic-tac-toe or Morpion(in French)"""

from pyfunct import Cursor, Temps, Assign, WriteFile, Unassign, Sound
from bubblewidgets import BubbleSquare, BubbleTriangle
from tkinter import Tk, Canvas, Frame, Text, Scrollbar, Message as Msg, IntVar
from tkinter.font import Font
from PIL import Image, ImageTk


class Solve:

    def __init__(self, morpion):
        """This class is made to find where the computer has to put his mark"""
        self.list = morpion

        self.solve()

    def solve(self):
        # Honeslty, i cannot explain what i did here
        solve = None
        place = None
        if not solve:
            for ww in range(3):
                a = [self.list[ww][0], self.list[ww][1], self.list[ww][2]]
                if 0 in a:
                    if a.count(0) > 1 and not 1 in a and None in a:
                        place = [ww, a.index(None)]
                        solve = 'solved'
                        break
            
        if not solve:
            for ww in range(3):
                a = [self.list[0][ww], self.list[1][ww], self.list[2][ww]]
                if 1 in a:
                    if a.count(0) > 1 and not 1 in a and None in a:
                        place = [a.index(None), ww]
                        solve = 'solved'
                        break
                
        if not solve:
            a = []
            b = []
            for ww in range(3):
                a.append(self.list[ww][ww])
                b.append(self.list[ww][2 - ww])
            if 1 in a:
                if a.count(0) > 1 and not 1 in a and None in a:
                    place = [a.index(None), a.index(None)]
                    solve = 'solved'
            if not solve:
                if 1 in b:
                    if b.count(0) > 1 and not 1 in b and None in b:
                        place = [b.index(None), b.index(None)]
                        solve = 'solved'
        
        if not solve:
            for ww in range(3):
                a = [self.list[ww][0], self.list[ww][1], self.list[ww][2]]
                if 1 in a:
                    if a.count(1) > 1 and not 0 in a and None in a:
                        place = [ww, a.index(None)]
                        solve = 'solved'
                        break
            
        if not solve:
            for ww in range(3):
                a = [self.list[0][ww], self.list[1][ww], self.list[2][ww]]
                if 1 in a:
                    if a.count(1) > 1 and not 0 in a and None in a:
                        place = [a.index(None), ww]
                        solve = 'solved'
                        break
                
        if not solve:
            a = []
            b = []
            for ww in range(3):
                a.append(self.list[ww][ww])
                b.append(self.list[ww][2 - ww])
            if 1 in a:
                if a.count(1) > 1 and not 0 in a and None in a:
                    place = [a.index(None), a.index(None)]
                    solve = 'solved'
            if not solve:
                if 1 in b:
                    if b.count(1) > 1 and not 0 in b and None in b:
                        place = [b.index(None), b.index(None)]
                        solve = 'solved'

        if not solve:
            for ww in self.list:
                if None in ww:
                    place = [self.list.index(ww), ww.index(None)]
                    solve = 'solved'
                    break
        
        if not solve:return None
        
        else:
            return place
        

class Mor:

    def __init__(self, master, top=None, classmaster=None, pion='o', start='you', son=True):
        """All calculations are in this class"""
        self.master = master
        self.top = top
        self.clm = classmaster
        self.son = son
        self.pion = pion
        self.start = start

        self.reset()

    def reset(self, event=None):
        self.master.delete('all')
        self.pause = True
        self.who = self.start

        self.wdt, self.hgt = eval(str(self.master['width'])), eval(str(self.master['height']))
        self.ix = self.wdt / 3 / 2; self.iy = self.hgt / 3 / 2
        self.wx = self.wdt / 3; self.hy = self.hgt / 3

        for ww in range(1, 3):
            self.master.create_line(40, self.hgt * ww / 3, self.wdt - 40, self.hgt * ww / 3, width=25, fill='light grey', capstyle='round')
            self.master.create_line(self.wdt * ww / 3, self.hgt - 40, self.wdt * ww / 3, 40, width=25, fill='light grey', capstyle='round')

        self.morpion = [[None, None, None],
                        [None, None, None],
                        [None, None, None]]
        self.place = [[(100, 100), (100, 300), (100, 500)],
                      [(300, 100), (300, 300), (300, 500)],
                      [(500, 100), (500, 300), (500, 500)]]
        
        self.failtext = self.master.create_text(self.wdt / 2, self.hgt / 2, text='Click to start',
                                                fill='purple', font='gameplay 30')

        self.timetext = self.master.create_text(self.wdt - 25, 25, text='', fill='white',
                                                font='gameplay 25 bold')

        Assign(self.master, self.game, ['Button-1'])

    def add_form(self, x, y, form='x'):
            if form == 'x':
                self.master.create_line(x - 45, y - 45, x + 45, y + 45, fill='orange', width=15, capstyle='round')
                self.master.create_line(x - 45, y + 45, x + 45, y - 45, fill='orange', width=15, capstyle='round')
            elif form == 'o':
                self.master.create_oval(x - 45, y - 45, x + 45, y + 45, outline='blue', width=15)

    def transform(self, value):
        if value <= 200:
            value = 0
        elif 200 < value <= 400:
            value = 1
        else: value = 2

        return value

    def ia(self):
        # When the computer has to play
        if self.pause == False:
            if self.who == 'ia':
                Unassign(self.master, ['Button-1'])
                b = Solve(self.morpion).solve()
                if b:
                    self.morpion[b[0]][b[1]] = 0
                    a = self.place[b[0]][b[1]]
                    x, y = a[0], a[1]
                    if self.pion == 'x':
                        self.add_form(x, y, 'o')
                    elif self.pion == 'o':
                        self.add_form(x, y, 'x')
                    self.who = 'you'
                    self.master.itemconfigure(self.timetext, text='⏳', angle=180)
                    Assign(self.master, self.you, ['Button-1'])
                    self.whowin()

    def you(self, event=None):
        # When the player has to play
        if self.pause == False:
            if self.who == 'you':
                xp = self.transform(event.x)
                yp = self.transform(event.y)
                if self.morpion[xp][yp] == None:
                    self.morpion[xp][yp] = 1
                    a = self.place[xp][yp]
                    x, y = a[0], a[1]
                    if self.pion == 'x':
                        self.add_form(x, y, 'x')
                    elif self.pion == 'o':
                        self.add_form(x, y, 'o')
                    self.who = 'ia'
                    self.master.itemconfigure(self.timetext, text='⏳', angle=0)
                    self.master.after(1000, self.ia)
                    self.whowin()

    def game(self, event=None):
            self.master.itemconfigure(self.failtext, fill='white', text='', font='gameplay 25 bold')
            Assign(self.master, self.you, ['Button-1'])
            self.pause = False
            if self.start == 'ia':
                self.ia()
        
    def whowin(self):
        a = self.cline()
        if a:
            self.pause = True
            if a[0] == 2:
                Unassign(self.master, ['Button-1'])
                self.master.itemconfigure(self.failtext, text='DRAW!', fill='yellow')
                self.master.lift(self.failtext)
                if self.son == True:
                    Sound('audio\\morpion\\1.mp3').play()
                self.ecrire('DRAW')
                self.master.after(1200, self.draw)
            elif a[0] == 1:
                Unassign(self.master, ['Button-1'])
                self.master.itemconfigure(self.failtext, text='WINNER!', fill='green')
                b = a[1]
                ax, ay = self.place[b[0][0]][b[0][1]], self.place[b[1][0]][b[1][1]]
                self.master.create_line(ax[0], ax[1], ay[0], ay[1],
                                        width=25, fill='white', capstyle='round')
                self.ecrire('WINNER!')
                self.master.lift(self.failtext)
                if self.son == True:
                    Sound('audio\\morpion\\2.mp3').play()
                self.master.after(1200, self.draw)
            elif a[0] == 0:
                Unassign(self.master, ['Button-1'])
                self.master.itemconfigure(self.failtext, text='LOSER!', fill='dark red')
                b = a[1]
                ax, ay = self.place[b[0][0]][b[0][1]], self.place[b[1][0]][b[1][1]]
                self.master.create_line(ax[0], ax[1], ay[0], ay[1],
                                        width=25, fill='white', capstyle='round')
                self.ecrire('LOSER!')
                self.master.lift(self.failtext)
                if self.son == True:
                    Sound('audio\\morpion\\failed1.mp3').play()
                self.master.after(1200, self.draw)

    def draw(self):
        self.master.itemconfigure(self.failtext, text='Click to restart', fill='purple')
        Assign(self.master, self.restart, ['Button-1'])

    def restart(self, event=None):
        self.reset()
        self.game()

    def ecrire(self, ecrit):
        f = open('data\\morpion.dat', 'a')
        f.write(f'{Temps().temps()} {ecrit}\n')
        f.close()
        with open('data\\morpion.dat', 'r') as f:
            self.clm.thistory['stat'] = 'normal'
            self.clm.thistory.delete('0.0', 'end')
            self.clm.thistory.insert('end', f.read())
            self.clm.thistory['stat'] = 'disabled'
            f.close()

    def cline(self):
        # I can't neither explain this
        winner = None
        place = None
        solve = None
        self.list = self.morpion

        if not solve:
            for ww in range(3):
                a = [self.list[ww][0], self.list[ww][1], self.list[ww][2]]
                if 1 in a:
                    if a.count(1) == 3:
                        winner = 1
                        place = [[ww, 0], [ww, 2]]
                        solve = 'solved'
                        break
                if not solve:
                    if 0 in a:
                        if a.count(0) == 3:
                            winner = 0
                            place = [[ww, 0], [ww, 2]]
                            solve = 'solved'
                            break
            
        if not solve:
            for ww in range(3):
                a = [self.list[0][ww], self.list[1][ww], self.list[2][ww]]
                if 1 in a:
                    if a.count(1) == 3:
                        winner = 1
                        place = [[0, ww], [2, ww]]
                        solve = 'solved'
                        break
                if not solve:
                    if 0 in a:
                        if a.count(0) == 3:
                            winner = 0
                            place = [[0, ww], [2, ww]]
                            solve = 'solved'
                            break
                
        if not solve:
            a = []
            b = []
            for ww in range(3):
                a.append(self.list[ww][ww])
                b.append(self.list[ww][2 - ww])
            if 1 in a:
                if a.count(1) == 3:
                    winner = 1
                    place = [[0, 0], [ww, ww]]
                    solve = 'solved'
            if not solve:
                if 0 in a:
                    if a.count(0) == 3:
                        winner = 0
                        place = [[0, 0], [ww, ww]]
                        solve = 'solved'
            if not solve:
                if 1 in b:
                    if b.count(1) == 3:
                        winner = 1
                        place = [[0, ww], [ww, 0]]
                        solve = 'solved'
                if not solve:
                    if 0 in b:
                        if b.count(0) == 3:
                            winner = 0
                            place = [[0, ww], [ww, 0]]
                            solve = 'solved'
        if not solve:
            useless = False
            for ww in self.morpion:
                for xx in ww:
                    if xx == None:
                        useless = True
                        break
                if useless == True:
                    break
                
            if useless == False:
                solve = 'solved'
                winner = 2
                place = None
            
        if not solve:
            return None
        else:
            return [winner, place]


class Pion(Canvas):

    def __init__(self, master, top=None, sound=True, **cnf):
        """The interface is created here"""
        Canvas.__init__(self, master, **cnf)
        self.master = master
        self.top = top
        self.sound = sound
        self.final = Sound('audio\\beta home page.mp3')
        self.son = Sound('audio\\default6.mp3')
        self.son.play(400)
        self.playtest()

        self.config(bg='black', bd=0, highlightthickness=0, relief='flat',
                    width=master.winfo_screenwidth(), height=master.winfo_screenheight())

        self.swdt, self.shgt = eval(str(self['width'])), eval(str(self['height']))

        imag = Image.open('media\\morpion\\icon.png')
        self.image = imag.resize((400, 190))
        self.image = ImageTk.PhotoImage(self.image)
        self.create_image(self.swdt / 2, 100, image=self.image)
        imag.close()

        self.create_text(self.swdt / 2, 220, text='Tic-Tac-Toe', fill='light blue',
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

        f = open('text\\morpion\\idetails.txt', 'r')
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
            self.mor.son = False
            self.son.volm()
            
        else:
            self.itemconfigure(self.pvol.title, text='')
            self.sound = True
            self.mor.son = True
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

            self.can = Canvas(self.frame, bg='black', bd=2, highlightthickness=0, relief='flat',
                              width=600, height=600)
            self.can.grid(row=2, column=1, padx=int((self.swdt - 900) / 2),
                          pady=int((self.shgt - eval(str(self.frame1['height'])) - 580) / 2.5))
            self.frame['width'], self.frame['height'] = self.swdt, self.shgt

            self.frame.place(x=0, y=0)
            self.varspeed = IntVar(value=0)
            
            self.mor = Mor(self.can, self.top, classmaster=self)
            self.mor.wdt = 600; self.mor.hgt = 600
            self.mor.reset()

            wdt, hgt = int(y1 * .5) + y1 // 2 - int(y1 * .5) - y1 // 2, y1 / 2 + 10 + y1 // 2 - y1 / 2 + 10 - y1 // 2
            
            BubbleSquare(self.frame1, int(y1 * .5), y1 / 2 + 10, width=wdt, height=hgt, text='', fg='red',
                            bg='grey5', font=['helvetica', y1 // 2, 'bold'], command=self.quitgamecommand)

            BubbleSquare(self.frame1, int(y1 * 1.5), y1 / 2 + 10, width=wdt, height=hgt, text='', fg='light blue',
                            bg='grey5', font=['helvetica', y1 // 2, 'bold'], command=self.uselessresetgame)

            self.audiogame = BubbleSquare(self.frame1, int(y1 * 2.5), y1 / 2 + 10, width=wdt, height=hgt, text='', fg='light blue',
                            bg='grey5', font=['helvetica', y1 // 2, 'bold'], command=self.audiogamecommand)

            self.frame1.create_text(x1 - 50, 10, text='Mark', fill='light yellow', font=Font(size=9, underline=True))
            
            self.sqrtoe = BubbleSquare(self.frame1, x1 - 50, y1 / 2 + 10, text='', og='grey2', command=self.toe,
                                        font=['helvetica', y1 // 6])
            self.sqrtoe.auto_size()

            self.frame1.create_text(x1 - 150, 10, text='Beginner', fill='light yellow', font=Font(size=9, underline=True))

            self.sqrmode = BubbleSquare(self.frame1, x1 - 150, y1 / 2 + 10, text='player', og='grey2', command=self.mode,
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

    def mode(self):
        if self.mor.start == 'you':
            self.mor.start = 'ia'
            self.mor.reset()
            self.frame1.itemconfigure(self.sqrmode.title, text='AI')
        elif self.mor.start == 'iai':
            self.mor.start = 'you'
            self.mor.reset()
            self.frame1.itemconfigure(self.sqrmode.title, text='Player')

    def toe(self):
        if self.mor.pion == 'x':
            self.mor.pion = 'o'
            self.mor.reset()
            self.frame1.itemconfigure(self.sqrtoe.title, text='')
        elif self.mor.pion == 'o':
            self.mor.pion = 'x'
            self.mor.reset()
            self.frame1.itemconfigure(self.sqrtoe.title, text='❌')

    def pausegamecommand(self):
        self.mor.pauseplay()
        if self.mor.pause == True:
            self.can.itemconfigure(self.bpause.title, text='')
        elif self.mor.pause == False:
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

    def quitgamecommand(self, event=None):  # Leave tic-tac-toe game
        self.vergame2 = False
        self.frame.place_forget()
        Cursor('media\\cursor\\cursor.cur')

    def audiogamecommand(self, event=None):
        if self.mor.son == True:
            self.mor.son = False
            self.frame1.itemconfigure(self.audiogame.title, text='')
            self.sound = False
            self.son.volm()
            self.itemconfigure(self.pvol.title, text='')
        elif self.mor.son == False:
            self.mor.son = True
            self.frame1.itemconfigure(self.audiogame.title, text='')
            self.sound = True
            self.son.volp()
            self.itemconfigure(self.pvol.title, text='')
            
    def uselessresetgame(self, event=None):
        self.mor.reset()

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
                f = open('data\\morpion.dat', 'r')
                l = f.read()
            except:
                f = open('data\\morpion.dat', 'a')
                f.close()
                l = '<EMPTY>'
            self.thistory['stat'] = 'normal'
            self.thistory.delete('0.0', 'end')
            self.thistory.insert('end', l)
            self.thistory['stat'] = 'disabled'
            WriteFile('data\\mpstat.dat', '')

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
        f = open('data\\morpion.dat', 'w')
        f.write('')
        f.close()


if __name__ == '__main__':
    fen = Tk()
    fen['bg'] = 'dark grey'
    fen.wm_attributes('-fullscreen', True)
    can = Canvas(fen, width=600, height=600, bg='black')
    can.pack

    a = Pion(fen, fen)
    a.pack()
    
    fen.mainloop()

    Cursor()

# 1:19:13-1:22:31

