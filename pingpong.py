# Ping Pong 1.0
# by LTS

from pyfunct import Temps, WriteFile, ReadFile, Assign, Unassign, Sound, Cursor
from tkinter import Tk, Canvas, Frame, Text, Scrollbar, Message as Msg
from tkinter.font import Font
from random import choice
from PIL import Image, ImageTk


class Ping(object):  # class of ping that contain objects

    def __init__(self, master, top=None, mode='normal', difficulty='n', side='right', start='left', classmaster=None, son=True):
        """All calculations are in this class"""
        self.master = master
        self.top = top
        self.mode = mode
        self.dif = difficulty
        self.side = side
        self.sidestart = start
        self.clm = classmaster

        self.wdt = eval(str(self.master['width']))
        self.hgt = eval(str(self.master['height']))

        self.master.create_rectangle(0, 0, self.wdt, self.hgt, width=5, outline='white')
        
        self.midline = self.master.create_line(self.wdt / 2, 2, self.wdt / 2, self.hgt - 2,
                                               width=5, fill='blue')
        self.lping = self.master.create_rectangle(20, self.hgt / 2 - 40, 30, self.hgt / 2 + 40,
                                                  width=0, fill='white')
        self.rping = self.master.create_rectangle(self.wdt - 20, self.hgt / 2 - 40, self.wdt - 30, self.hgt / 2 + 40,
                                                  width=0, fill='white')
        self.lscore = self.master.create_text(self.wdt / 4, 20, text='0', fill='grey80',
                                              font=Font(family='helvetica', size=13))
        self.rscore = self.master.create_text(self.wdt / 4 * 3, 20, text='0', fill='grey80',
                                              font=Font(family='helvetica', size=13))
        self.ball = self.master.create_oval(self.wdt / 2 - 10, self.hgt / 2 - 10, self.wdt / 2 + 10, self.hgt / 2 + 10,
                                            width=0, fill='red')
        self.lmsg = self.master.create_text(self.wdt / 4, self.hgt / 2, font=Font(family='helvetica', size='25'))
        self.rmsg = self.master.create_text(self.wdt / 4 * 3, self.hgt / 2, font=Font(family='helvetica', size='25'))

        self.pause = True

        self.lsc = 0  # Score
        self.rsc = 0

        self.history = []

        self.lpy = self.hgt / 2  # bar pos
        self.rpy = self.hgt / 2

        self.lspeed = 0  # bar speed
        self.rspeed = 0

        self.lray = 40  # bar radius
        self.rray = 40

        self.hbspeed = 0  # balle speed
        self.vbspeed = 0
        
        self.bposx = self.wdt / 2  # balle pos
        self.bposy = self.hgt / 2
        self.aftb = None

        self.gauche = False
        self.droite = False

        self.iaft = None
        self.dict = {'e': self.easy, 'n': self.normal, 'h': self.hard, 'v': self.veryhard}

        self.son = son

        self.lecture()
        self.svs

    def lmoveup(self, event=None):  # left bar move up
        if self.lpy > 0 and self.gauche == True and self.pause == False:
            self.master.move(self.lping, 0, -self.lspeed)
            self.lpy -= self.lspeed

    def rmoveup(self, event=None):  # right bar move up
        if self.rpy > 0 and self.droite == True and self.pause == False:
            self.master.move(self.rping, 0, -self.rspeed)
            self.rpy -= self.rspeed

    def lmovedown(self, event=None):  # left bar move down
        if self.lpy < self.hgt and self.gauche == True and self.pause == False:
            self.master.move(self.lping, 0, self.lspeed)
            self.lpy += self.lspeed

    def rmovedown(self, event=None):  # right bar move down
        if self.rpy < self.hgt and self.droite == True and self.pause == False:
            self.master.move(self.rping, 0, self.rspeed)
            self.rpy += self.rspeed

    def moveballe(self):  # Ball motion
        if self.pause == False:
            self.ia()
            self.postest()
            self.verticalmove()
            self.master.move(self.ball, self.hbspeed, self.vbspeed)
            self.bposx += self.hbspeed; self.bposy += self.vbspeed
            self.aftb = self.master.after(30, self.moveballe)
            self.savestate()

        else:
            self.master.after_cancel(self.aftb)

    def verticalmove(self):
        if self.bposy <= 10 or self.bposy >= self.hgt - 10:
            self.vbspeed = -1 * self.vbspeed
            a = choice([-1, 0, 1])
            self.vbspeed += a
            if self.son == True:
                au = Sound('audio\\pingpong\\2.1.mp3')
                au.play()

    def mainside(self, side):
        if side == 'left':
            self.droite = False
            self.gauche = True
        elif side == 'right':
            self.droite = True
            self.gauche = False
        elif side == 'both':
            self.droite = True
            self.gauche = True
        elif self.side == 'none':
            self.droite = False
            self.gauche = False

    def easy(self):  # easy mod
        self.lray = 40
        self.rray = 40
        self.lspeed = 20
        self.rspeed = 20
        self.hbspeed = 6
        self.vbspeed = choice([-11, -10, -9, -8, -7, -6, -5,
                               11, 10, 9, 8, 7, 6, 5])
        if self.sidestart == 'left':
            self.hbspeed = -1 * self.hbspeed

    def normal(self):  # normal mod
        self.lray = 40
        self.rray = 40
        self.lspeed = 15
        self.rspeed = 15
        self.hbspeed = 10
        self.vbspeed = choice([-11, -10, -9, -8, -7, -6, -5,
                               11, 10, 9, 8, 7, 6, 5])
        if self.sidestart == 'left':
            self.hbspeed = -1 * self.hbspeed

    def hard(self):  #  hard mod
        self.lray = 30
        self.rray = 30
        self.lspeed = 20
        self.rspeed = 20
        self.hbspeed = 15
        self.vbspeed = choice([-11, -10, -9, -8, -7, -6, -5,
                               11, 10, 9, 8, 7, 6, 5])
        if self.sidestart == 'left':
            self.hbspeed = -1 * self.hbspeed

    def veryhard(self):  # very hard mod
        self.lray = 25
        self.rray = 25
        self.lspeed = 15
        self.rspeed = 15
        self.hbspeed = 20
        self.vbspeed = choice([-11, -10, -9, -8, -7, -6, -5,
                               11, 10, 9, 8, 7, 6, 5])
        if self.sidestart == 'left':
            self.hbspeed = -1 * self.hbspeed

    def ia(self):  # AI mod
        if self.mode != 'normal':
            if self.side == 'left':
                Unassign(self.top, ['Up'])
                Unassign(self.top, ['Down'])
                Assign(self.top, self.lmoveup, ['w', 'W'])
                Assign(self.top, self.lmovedown, ['s', 'S'])
                self.iamove()
            elif self.side == 'right':
                Unassign(self.top, ['w', 'W'])
                Unassign(self.top, ['s', 'S'])
                Assign(self.top, self.rmoveup, ['Up'])
                Assign(self.top, self.rmovedown, ['Down'])
            self.iamove()
        else:
            Assign(self.top, self.lmoveup, ['w', 'W'])
            Assign(self.top, self.lmovedown, ['s', 'S'])
            Assign(self.top, self.rmoveup, ['Up'])
            Assign(self.top, self.rmovedown, ['Down'])

    def iamove(self):  # AI control
        win = choice(['win', 'win', 'win', 'lose'])
        if win == 'win':
            if self.side == 'left':
                if self.rpy > self.bposy:
                    self.rmoveup()
                elif self.rpy < self.bposy:
                    self.rmovedown()
            elif self.side == 'right':
                if self.lpy > self.bposy:
                    self.lmoveup()
                elif self.lpy < self.bposy:
                    self.lmovedown()
        else:pass

    def postest(self):  # fail test
        if self.bposx >= self.wdt - 40:
            a, b = self.rpy - self.rray, self.rpy + self.rray
            if not a < self.bposy < b:
                self.rfail()
            else:
                self.hbspeed = -1 * self.hbspeed
                if self.son == True:
                    au = Sound('audio\\pingpong\\1.mp3')
                    au.play()
                if self.mode == 'normal':
                    self.mainside('left')
                else:
                    self.mainside('both')

        elif self.bposx <= 40:
            a, b = self.lpy - self.lray, self.lpy + self.lray
            if not a < self.bposy < b:
                self.lfail()
            else:
                self.hbspeed = -1 * self.hbspeed
                if self.son == True:
                    au = Sound('audio\\pingpong\\1.mp3')
                    au.play()
                if self.mode == 'normal':
                    self.mainside('right')
                else:
                    self.mainside('both')

    def rfail(self):  # right player failed
        self.pause = True
        self.lsc += 1
        self.master.itemconfigure(self.lmsg, fill='blue', text='+1')
        self.master.itemconfigure(self.rmsg, fill='red', text='+0')
        self.master.itemconfigure(self.lscore, text=self.lsc)
        self.evalu_sc()

    def lfail(self):  # left player failed
        self.pause = True
        self.rsc += 1
        self.master.itemconfigure(self.rmsg, fill='blue', text='+1')
        self.master.itemconfigure(self.lmsg, fill='red', text='+0')
        self.master.itemconfigure(self.rscore, text=self.rsc)
        self.evalu_sc()

    def evalu_sc(self):  # score evaluation
        self.keepprogress()
        if self.son == True:
            Sound('audio\\pingpong\\failed1.mp3').play()
            Sound('audio\\pingpong\\failed2.mp3').play()
        if self.lsc > self.rsc:
            self.master.itemconfigure(self.lscore, fill='green')
            self.master.itemconfigure(self.rscore, fill='orange')
        elif self.lsc < self.rsc:
            self.master.itemconfigure(self.lscore, fill='orange')
            self.master.itemconfigure(self.rscore, fill='green')
        else:
            self.master.itemconfigure(self.lscore, fill='grey80')
            self.master.itemconfigure(self.rscore, fill='grey80')
        self.afteva = self.master.after(1200, self.msg_fail)

    def msg_fail(self): 
        self.master.itemconfigure(self.rmsg, text='')
        self.master.itemconfigure(self.lmsg, text='')
        self.master.after_cancel(self.afteva)
        
        self.history.append([[Temps().temps()], [self.lsc, self.rsc], [self.wdt / 2], [self.hgt / 2],
                             [self.lpy, self.rpy], [self.lray, self.rray],
                             [self.mode, self.dif], [self.side, self.sidestart], [self.son]])  # keep history
        self.recentre()

    def recentre(self):  # restart after failling
        self.master.coords(self.ball, self.wdt / 2 - 10, self.hgt / 2 - 10, self.wdt / 2 + 10, self.hgt / 2 + 10)
        self.master.coords(self.lping, 20, self.hgt / 2 - self.lray, 30, self.hgt / 2 + self.lray)
        self.master.coords(self.rping, self.wdt - 20, self.hgt / 2 - self.lray, self.wdt - 30, self.hgt / 2 + self.lray)
        self.lpy = self.hgt / 2
        self.rpy = self.hgt / 2
        self.bposx = self.wdt / 2  
        self.bposy = self.hgt / 2

    def touchstart(self, event=None):  # Start
        if self.hbspeed < 0:
                if self.mode == 'normal':
                    self.mainside('left')
                else:
                    self.mainside('both')
        elif self.hbspeed > 0:
                if self.mode == 'normal':
                    self.mainside('right')
                else:
                    self.mainside('both')
        else:
            self.hbspeed = choice([-11, -10, -9, -8, -7, -6, -5,
                               11, 10, 9, 8, 7, 6, 5])
            self.touchstart()
            
        if self.pause == True:
            self.pause = False
            self.moveballe()
        elif self.pause == False:
            self.pause = True
            
    def restart(self, event=None):  # Restart game
        self.lsc = 0  # Score
        self.rsc = 0

        self.gauche = False
        self.droite = False

        self.master.itemconfigure(self.lscore, fill='grey80', text=self.lsc)
        self.master.itemconfigure(self.rscore, fill='grey80', text=self.rsc)

        self.dict[self.dif]()
        self.recentre()
        self.dict[self.dif]()
        self.touchstart()
        self.pause = True

    def lecture(self):
        try:
            f = open('data\\pingpong.dat', 'r')
            self.history = f.readlines()
            f.close()
        except:
            f = open('data\\pingpong.dat', 'a')
            f.close()

    def keepprogress(self):
        self.history.append(str(f'{Temps().temps()} player1: {self.lsc} player2: {self.rsc}'))
        f = open('data\\pingpong.dat', 'a')
        f.write(self.history[len(self.history) - 1] + '\n')
        f.close()
        self.clm.thistory['stat'] = 'normal'
        self.clm.thistory.delete('0.0', 'end')
        f = open('data\\pingpong.dat', 'r')
        self.clm.thistory.insert('end', f.read())
        self.clm.thistory['stat'] = 'disabled'

    def svs(self, event=None):
        self.master.after(2000, self.savestate)

    def savestate(self, event=None):  # bposx bposy hbspeed vbspeed lpy rpy mod dif side star son lsc rsc
        if self.pause == False:
            WriteFile('data\\ppstat.dat',
                   '{0}x{1}x{2}x{3}x{4}x{5}x{6}x{7}x{8}x{9}x{10}x{11}x{12}x'.format(self.bposx, self.bposy,
                                                                                      self.hbspeed, self.vbspeed,
                                                                                      self.lpy, self.rpy,
                                                                                      self.mode, self.dif,
                                                                                      self.side, self.sidestart,
                                                                                      self.son,
                                                                                      self.lsc, self.rsc))
        
    def readstate(self, event=None):
        try:
            data = ReadFile('data\\ppstat.dat').assigne()
        except:
            WriteFile('data\\ppstat.dat', '')
            data = None
        finally:
            return data

    def setside(self, event=None):
        if self.start == 'left' and self.hbspeed > 0 or self.start == 'right' and self.hbspeed < 0:
            self.hbspeed = -1 * self.hbspeed

    def unevent(self):
        if self.top:
            Unassign(self.top, ['w', 'W'])
            Unassign(self.top, ['s', 'S'])
            Unassign(self.top, ['Up'])
            Unassign(self.top, ['Down'])

    def isevent(self):
        if self.top:
            Assign(self.top, self.lmoveup, ['w', 'W'])
            Assign(self.top, self.lmovedown, ['s', 'S'])
            Assign(self.top, self.rmoveup, ['Up'])
            Assign(self.top, self.rmovedown, ['Down'])


class Pong(Canvas):  # class of pingpong home page

    def __init__(self, master, top=None, sound=True, **cnf):
        """The interface is created here"""
        Canvas.__init__(self, master, cnf)
        self.master = master
        self.top = top
        self.sound = sound
        self.son = Sound('audio\\default2.2.mp3')
        self.final = Sound('audio\\beta home page.mp3')
        self.son.play(400)
        self.playtest()

        self.config(bg='black', bd=0, highlightthickness=0, relief='flat',
                    width=master.winfo_screenwidth(), height=master.winfo_screenheight())

        self.swdt, self.shgt = eval(str(self['width'])), eval(str(self['height']))

        imag = Image.open('media\\pingpong\\icon.png')
        self.image = imag.resize((400, 190))
        self.image = ImageTk.PhotoImage(self.image)
        self.create_image(self.swdt / 2, 100, image=self.image)
        imag.close()

        self.create_text(self.swdt / 2, 220, text='Ping Pong', fill='light blue',
                         font=Font(family='Gameplay', size=30, weight='bold', underline=True))  # text contain

        self.pnew = self.create_polygon(50, 300, 350, 350, 50, 400, fill='dark blue', outline='dark blue')  # Buttons 
        self.tnew = self.create_text(130, 350, text='Play', fill='light blue', font='helvetica 20 bold')

        self.pcont = self.create_polygon(350, 360, 50, 410, 350, 460, fill='dark blue', outline='dark blue')
        self.tcont = self.create_text(270, 410, text='Continue', fill='light blue', font='helvetica 20 bold')

        self.ppar = self.create_polygon(50, 420, 350, 470, 50, 520, fill='dark blue', outline='dark blue')
        self.tpar = self.create_text(130, 470, text='History', fill='light blue', font='helvetica 20 bold')

        self.pquit = self.create_polygon(350, 480, 50, 530, 350, 580, fill='dark red', outline='dark red')
        self.tquit = self.create_text(270, 530, text='Quit', fill='light blue', font='helvetica 20 bold')

        self.pvol = self.create_rectangle(self.swdt - 90, self.shgt - 90, self.swdt - 20, self.shgt - 20, fill='black')
        self.tvol = self.create_text(self.swdt - 55, self.shgt - 55, text='', fill='light blue', font='helvetica 45')

        f = open('text\\pingpong\\idetails.txt', 'r')
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

        self.mode = 'normal'
        self.side = 'right'
        self.dif = 'n'
        self.start = 'left'

        self.tag_bind(self.pnew, '<Enter>', self.inanimenew)  # assignement
        self.tag_bind(self.tnew, '<Enter>', self.inanimenew)
        self.tag_bind(self.pnew, '<Leave>', self.outanimenew)
        self.tag_bind(self.tnew, '<Leave>', self.outanimenew)
        self.tag_bind(self.pnew, '<Button-1>', self.game)
        self.tag_bind(self.tnew, '<Button-1>', self.game)

        self.tag_bind(self.pcont, '<Enter>', self.inanimecont)
        self.tag_bind(self.tcont, '<Enter>', self.inanimecont)
        self.tag_bind(self.pcont, '<Leave>', self.outanimecont)
        self.tag_bind(self.tcont, '<Leave>', self.outanimecont)
        self.tag_bind(self.pcont, '<Button-1>', self.oncliccont)
        self.tag_bind(self.tcont, '<Button-1>', self.oncliccont)

        self.tag_bind(self.ppar, '<Enter>', self.inanimepar)
        self.tag_bind(self.tpar, '<Enter>', self.inanimepar)
        self.tag_bind(self.ppar, '<Leave>', self.outanimepar)
        self.tag_bind(self.tpar, '<Leave>', self.outanimepar)
        self.tag_bind(self.ppar, '<Button-1>', self.setpar)
        self.tag_bind(self.tpar, '<Button-1>', self.setpar)

        self.tag_bind(self.pquit, '<Enter>', self.inquit)
        self.tag_bind(self.tquit, '<Enter>', self.inquit)
        self.tag_bind(self.pquit, '<Leave>', self.outquit)
        self.tag_bind(self.tquit, '<Leave>', self.outquit)
        self.tag_bind(self.pquit, '<Button-1>', self.onclicquit)
        self.tag_bind(self.tquit, '<Button-1>', self.onclicquit)

        self.tag_bind(self.pvol, '<Enter>', self.invol)
        self.tag_bind(self.tvol, '<Enter>', self.invol)
        self.tag_bind(self.pvol, '<Leave>', self.outvol)
        self.tag_bind(self.tvol, '<Leave>', self.outvol)
        self.tag_bind(self.pvol, '<Button-1>', self.onclicvol)
        self.tag_bind(self.tvol, '<Button-1>', self.onclicvol)

    def inanimenew(self, event=None):  # Motion effect
        self.itemconfigure(self.pnew, width=7)
        self.itemconfigure(self.tnew, font='helvetica 23 bold')
        Sound('audio\\motioneffect1.mp3').play()
        Cursor('media\\cursor\\hand.cur')

    def outanimenew(self, event):
        self.itemconfigure(self.pnew, width=0)
        self.itemconfigure(self.tnew, font='helvetica 20 bold')
        Sound('audio\\motioneffect2.mp3').play()
        Cursor('media\\cursor\\cursor.cur')

    def inanimecont(self, event=None):
        self.itemconfigure(self.pcont, width=7)
        self.itemconfigure(self.tcont, font='helvetica 23 bold')
        Sound('audio\\motioneffect1.mp3').play()
        Cursor('media\\cursor\\hand.cur')

    def outanimecont(self, event):
        self.itemconfigure(self.pcont, width=0)
        self.itemconfigure(self.tcont, font='helvetica 20 bold')
        Sound('audio\\motioneffect2.mp3').play()
        Cursor('media\\cursor\\cursor.cur')

    def inanimepar(self, event=None):
        self.itemconfigure(self.ppar, width=7)
        self.itemconfigure(self.tpar, font='helvetica 23 bold')
        Sound('audio\\motioneffect1.mp3').play()
        Cursor('media\\cursor\\hand.cur')

    def outanimepar(self, event):
        self.itemconfigure(self.ppar, width=0)
        self.itemconfigure(self.tpar, font='helvetica 20 bold')
        Sound('audio\\motioneffect2.mp3').play()
        Cursor('media\\cursor\\cursor.cur')

    def inquit(self, event=None):
        self.itemconfigure(self.pquit, width=7)
        self.itemconfigure(self.tquit, font='helvetica 23 bold')
        Sound('audio\\motioneffect1.mp3').play()
        Cursor('media\\cursor\\hand.cur')

    def outquit(self, event=None):
        self.itemconfigure(self.pquit, width=0)
        self.itemconfigure(self.tquit, font='helvetica 20 bold')
        Sound('audio\\motioneffect2.mp3').play()
        Cursor('media\\cursor\\cursor.cur')

    def invol(self, event=None):
        self.itemconfigure(self.pvol, width=7)
        self.itemconfigure(self.tvol, font='helvetica 48 bold')
        Sound('audio\\motioneffect1.mp3').play()
        Cursor('media\\cursor\\hand.cur')

    def outvol(self, event=None):
        self.itemconfigure(self.pvol, width=0)
        self.itemconfigure(self.tvol, font='helvetica 45 bold')
        Sound('audio\\motioneffect2.mp3').play()
        Cursor('media\\cursor\\cursor.cur')

    def onclicvol(self, event=None, son=None):
        if son:
            self.sound = son
            
        if self.sound == True:
            self.itemconfigure(self.tvol, text='')
            self.sound = False
            self.son.volm()
            
        else:
            self.itemconfigure(self.tvol, text='')
            self.sound = True
            self.son.volp()
    
    def oncliccont(self, event=None):
        self.game()
        data = self.ping.readstate()
        if data:  # bposx bposy hbspeed vbspeed lpy rpy mode dif side star son lsc rsc
            if len(data) > 13:
                sp = self.ping
                sp.restart()
                li = [sp.bposx, sp.bposy, sp.hbspeed, sp.vbspeed, sp.lpy, sp.rpy, sp.mode,
                      sp.dif, sp.side, sp.sidestart, sp.son, sp.lsc, sp.rsc]
                lo = data.split('x')
                sp.dict[li[7]]()
                
                li[0] = eval(lo[0]); li[1] = eval(lo[1])  # bposx, bposy
                li[2] = eval(lo[2]); li[3] = eval(lo[3])  # hbspeed, vbspeed
                li[4] = eval(lo[4]); li[5] = eval(lo[5])  # lpy, rpy
                li[6] = str(lo[6]); li[7] = str(lo[7])  # mode, dif
                li[8] = str(lo[8]); li[9] = str(lo[9])  # side, start
                li[10] = eval(lo[10]);  # son
                li[11] = eval(lo[11]); li[12] = eval(lo[12])  # lsc rsc
                
                sp.master.move(sp.lping, 0, sp.hgt / 2 - li[4])
                sp.master.move(sp.rping, 0, sp.hgt / 2 - li[5])
                sp.master.move(sp.ball, sp.wdt / 2 - li[0], sp.hgt / 2 - li[1])
                sp.master.itemconfigure(sp.lscore, text=li[11])
                sp.master.itemconfigure(sp.rscore, text=li[12])

    def onclicquit(self, event=None):
        self.son.stop()
        self.final.play()
        self.destroy()
        Cursor('media\\cursor\\cursor.cur')

    def game(self, event=None):  # ping option
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
                              width=900, height=580)
            self.can.grid(row=2, column=1, padx=int((self.swdt - 900) / 2),
                          pady=int((self.shgt - eval(str(self.frame1['height'])) - 580) / 2))
            self.frame['width'], self.frame['height'] = self.swdt, self.shgt

            self.frame.place(x=0, y=0)
            
            self.ping = Ping(self.can, self.master, 'ia', side='left', classmaster=self, son=self.sound)
            self.ping.isevent()
            self.ping.restart()

            self.sqrleave = self.frame1.create_rectangle(int(y1 * .5) - y1 // 2, y1 / 2 + 10 - y1 // 2, int(y1 * .5) + y1 // 2, y1 / 2 + 10 + y1 // 2,
                                                     fill='grey5')
            self.leavegame = self.frame1.create_text(int(y1 * .5), y1 / 2 + 10, text='', fill='red',
                                                     font=Font(size=y1 // 2, weight='bold'))
            
            self.sqrrestart = self.frame1.create_rectangle(int(y1 * 1.5) - y1 // 2, y1 / 2 + 10 - y1 // 2, int(y1 * 1.5) + y1 // 2, y1 / 2 + 10 + y1 // 2,
                                                     fill='grey5')
            self.restartgame = self.frame1.create_text(int(y1 * 1.5), y1 // 2 + 10, text='',
                                                      fill='light blue', font=Font(size=y1 // 2, weight='bold'))
            
            self.sqrpause = self.frame1.create_rectangle(int(y1 * 2.5) - y1 // 2, y1 / 2 + 10 - y1 // 2, int(y1 * 2.5) + y1 // 2, y1 / 2 + 10 + y1 // 2,
                                                     fill='grey5')
            self.pausegame = self.frame1.create_text(int(y1 * 2.5), y1 // 2 + 10, text='',
                                                      fill='light blue', font=Font(size=y1 // 2, weight='bold'))

            self.sqraudio = self.frame1.create_rectangle(int(y1 * 3.5) - y1 // 2, y1 / 2 + 10 - y1 // 2, int(y1 * 2.5) + y1 // 2, y1 / 2 + 10 + y1 // 2,
                                                     fill='grey5')
            self.audiogame = self.frame1.create_text(int(y1 * 3.5), y1 // 2 + 10, text='',
                                                 fill='light blue', font=Font(size=y1 // 2, weight='bold'))
            if self.sound == False:
                self.frame1.itemconfigure(self.audiogame, text='')

            self.sqrstart = self.frame1.create_rectangle(int((x1 - 350) - (y1 // 6 * 4 / 2)), y1 - 30 - y1 // 6, int((x1 - 350) + (y1 // 6 * 4 / 2)), y1 - 30 + y1 // 6,
                                                     fill='grey10', outline='grey10')
            self.startgame = self.frame1.create_text(int(x1 - 350), y1 - 30, text='Left',
                                                      fill='purple', font=Font(size=y1 // 6, weight='bold'))
            self.frame1.create_text(int(x1 - 350), 10, text='Begenner', fill='light yellow', font=Font(size=8, weight='bold', underline=True))
            
            self.sqrmode = self.frame1.create_rectangle(int((x1 - 250) - (y1 // 6 * 5 / 2)), y1 - 30 - y1 // 6, int((x1 - 250) + (y1 // 6 * 5 / 2)), y1 - 30 + y1 // 6,
                                                     fill='grey10', outline='grey10')
            self.modegame = self.frame1.create_text(int(x1 - 250), y1 - 30, text='VS AI',
                                                      fill='purple', font=Font(size=y1 // 6, weight='bold'))
            self.frame1.create_text(int(x1 - 250), 10, text='Mode', fill='light yellow', font=Font(size=8, weight='bold', underline=True))

            self.sqrdif = self.frame1.create_rectangle(int((x1 - 150) - (y1 // 6 * 6 / 2)), y1 - 30 - y1 // 6, int((x1 - 150) + (y1 // 6 * 6 / 2)), y1 - 30 + y1 // 6,
                                                     fill='grey10', outline='grey10')
            self.difgame = self.frame1.create_text(int(x1 - 150), y1 - 30, text='Normal',
                                                      fill='purple', font=Font(size=y1 // 6, weight='bold'))
            self.frame1.create_text(int(x1 - 150), 10, text='Difficulty', fill='light yellow', font=Font(size=8, weight='bold', underline=True))
            
            self.sqrside = self.frame1.create_rectangle(int((x1 - 50) - (y1 // 6 * 5 / 2)), y1 - 30 - y1 // 6, int((x1 - 50) + (y1 // 6 * 5 / 2)), y1 - 30 + y1 // 6,
                                                     fill='grey10', outline='grey10')
            self.sidegame = self.frame1.create_text(int(x1 - 50), y1 - 30, text='Left',
                                                      fill='purple', font=Font(size=y1 // 6, weight='bold'))
            self.frame1.create_text(int(x1 - 50), 10, text='Side', fill='light yellow', font=Font(size=8, weight='bold', underline=True))

            self.frame1.tag_bind(self.sqrleave, '<Enter>', self.inleavegame)
            self.frame1.tag_bind(self.leavegame, '<Enter>', self.inleavegame)
            self.frame1.tag_bind(self.sqrleave, '<Leave>', self.outleavegame)
            self.frame1.tag_bind(self.leavegame, '<Leave>', self.outleavegame)
            self.frame1.tag_bind(self.sqrleave, '<Button-1>', self.quitgamecommand)
            self.frame1.tag_bind(self.leavegame, '<Button-1>', self.quitgamecommand)

            self.frame1.tag_bind(self.sqrpause, '<Enter>', self.inpausegame)
            self.frame1.tag_bind(self.pausegame, '<Enter>', self.inpausegame)
            self.frame1.tag_bind(self.sqrpause, '<Leave>', self.outpausegame)
            self.frame1.tag_bind(self.pausegame, '<Leave>', self.outpausegame)
            self.frame1.tag_bind(self.sqrpause, '<Button-1>', self.pausegamecommand)
            self.frame1.tag_bind(self.pausegame, '<Button-1>', self.pausegamecommand)

            self.frame1.tag_bind(self.sqrrestart, '<Enter>', self.inrestartgame)
            self.frame1.tag_bind(self.restartgame, '<Enter>', self.inrestartgame)
            self.frame1.tag_bind(self.sqrrestart, '<Leave>', self.outrestartgame)
            self.frame1.tag_bind(self.restartgame, '<Leave>', self.outrestartgame)
            self.frame1.tag_bind(self.sqrrestart, '<Button-1>', self.ping.restart)
            self.frame1.tag_bind(self.restartgame, '<Button-1>', self.ping.restart)

            self.frame1.tag_bind(self.sqraudio, '<Enter>', self.inaudiogame)
            self.frame1.tag_bind(self.audiogame, '<Enter>', self.inaudiogame)
            self.frame1.tag_bind(self.sqraudio, '<Leave>', self.outpausegame)
            self.frame1.tag_bind(self.audiogame, '<Leave>', self.outaudiogame)
            self.frame1.tag_bind(self.sqraudio, '<Button-1>', self.audiogamecommand)
            self.frame1.tag_bind(self.audiogame, '<Button-1>', self.audiogamecommand)

            self.frame1.tag_bind(self.sqrmode, '<Enter>', self.inmode)
            self.frame1.tag_bind(self.modegame, '<Enter>', self.inmode)
            self.frame1.tag_bind(self.sqrmode, '<Leave>', self.outmode)
            self.frame1.tag_bind(self.modegame, '<Leave>', self.outmode)
            self.frame1.tag_bind(self.sqrmode, '<Button-1>', self.modegamecommand)
            self.frame1.tag_bind(self.modegame, '<Button-1>', self.modegamecommand)

            self.frame1.tag_bind(self.sqrdif, '<Enter>', self.indif)
            self.frame1.tag_bind(self.difgame, '<Enter>', self.indif)
            self.frame1.tag_bind(self.sqrdif, '<Leave>', self.outdif)
            self.frame1.tag_bind(self.difgame, '<Leave>', self.outdif)
            self.frame1.tag_bind(self.sqrdif, '<Button-1>', self.difgamecommand)
            self.frame1.tag_bind(self.difgame, '<Button-1>', self.difgamecommand)

            self.frame1.tag_bind(self.sqrside, '<Enter>', self.inside)
            self.frame1.tag_bind(self.sidegame, '<Enter>', self.inside)
            self.frame1.tag_bind(self.sqrside, '<Leave>', self.outside)
            self.frame1.tag_bind(self.sidegame, '<Leave>', self.outside)
            self.frame1.tag_bind(self.sqrside, '<Button-1>', self.sidegamecommand)
            self.frame1.tag_bind(self.sidegame, '<Button-1>', self.sidegamecommand)

            self.frame1.tag_bind(self.sqrstart, '<Enter>', self.instart)
            self.frame1.tag_bind(self.startgame, '<Enter>', self.instart)
            self.frame1.tag_bind(self.sqrstart, '<Leave>', self.outstart)
            self.frame1.tag_bind(self.startgame, '<Leave>', self.outstart)
            self.frame1.tag_bind(self.sqrstart, '<Button-1>', self.startgamecommand)
            self.frame1.tag_bind(self.startgame, '<Button-1>', self.startgamecommand)

            Assign(self.ping.master, self.pausegamecommand, ['Button-1', 'Button-3', 'Return'])

        if self.vergame == True:
            if self.vergame2 == True:
                self.frame.place_forget()
                self.vergame2 = False
            elif self.vergame2 == False:
                self.frame.place(x=0, y=0)
                self.vergame2 = True
        
    def quitgamecommand(self, event=None):  # Leave pingpong game
        self.ping.restart()
        self.vergame2 = False
        self.frame.place_forget()

    def pausegamecommand(self, event=None):  # pause on game
        if self.ping.pause == True:
            self.ping.pause = False
            self.ping.moveballe()
            self.frame1.itemconfigure(self.pausegame, text='')
        elif self.ping.pause == False:
            self.ping.pause = True
            self.frame1.itemconfigure(self.pausegame, text='')

    def audiogamecommand(self, event=None):
        if self.ping.son == True:
            self.ping.son = False
            self.frame1.itemconfigure(self.audiogame, text='')
            self.sound = False
            self.son.volm()
            self.itemconfigure(self.tvol, text='')
        elif self.ping.son == False:
            self.ping.son = True
            self.frame1.itemconfigure(self.audiogame, text='')
            self.sound = True
            self.son.volp()
            self.itemconfigure(self.tvol, text='')

    def modegamecommand(self, event=None):
        x1, y1 = int(eval(str(self.frame1['width']))), int(eval(str(self.frame1['height'])))  # option mod
        
        if self.mode == 'normal':
            self.mode = 'ia'
            self.ping.pause = True
            self.ping.mode = self.mode
            self.ping.restart()
            self.frame1.itemconfigure(self.modegame, text='VS AI')
            self.frame1.coords(self.sqrmode,
                               int((x1 - 250) - (y1 // 6 * 5 / 2)), y1 - 30 - y1 // 6, int((x1 - 250) + (y1 // 6 * 5 / 2)), y1 - 30 + y1 // 6)
        else:
            self.mode = 'normal'
            self.ping.pause = True
            self.ping.mode = self.mode
            self.ping.restart()
            self.frame1.itemconfigure(self.modegame, text='VS Friend')
            self.frame1.coords(self.sqrmode,
                               int((x1 - 250) - (y1 // 6 * 9 / 2)), y1 - 30 - y1 // 6, int((x1 - 250) + (y1 // 6 * 9 / 2)), y1 - 30 + y1 // 6)

    def difgamecommand(self, event=None):
        x1, y1 = int(eval(str(self.frame1['width']))), int(eval(str(self.frame1['height'])))  # difficulty option
        
        if self.dif == 'e':
            self.dif = 'n'
            self.ping.pause = True
            self.ping.dif = self.dif
            self.ping.normal()
            self.frame1.itemconfigure(self.difgame, text='Normal')
            self.frame1.coords(self.sqrdif,
                               int((x1 - 150) - (y1 // 6 * 6 / 2)), y1 - 30 - y1 // 6, int((x1 - 150) + (y1 // 6 * 6 / 2)), y1 - 30 + y1 // 6)
        elif self.dif == 'n':
            self.dif = 'h'
            self.ping.pause = True
            self.ping.dif = self.dif
            self.ping.hard()
            self.frame1.itemconfigure(self.difgame, text='Hard')
            self.frame1.coords(self.sqrdif,
                               int((x1 - 150) - (y1 // 6 * 4 / 2)), y1 - 30 - y1 // 6, int((x1 - 150) + (y1 // 6 * 4 / 2)), y1 - 30 + y1 // 6)

        elif self.dif == 'h':
            self.dif = 'v'
            self.ping.pause = True
            self.ping.dif = self.dif
            self.ping.veryhard()
            self.frame1.itemconfigure(self.difgame, text='Very Hard')
            self.frame1.coords(self.sqrdif,
                               int((x1 - 150) - (y1 // 6 * 9 / 2)), y1 - 30 - y1 // 6, int((x1 - 150) + (y1 // 6 * 9 / 2)), y1 - 30 + y1 // 6)

        elif self.dif == 'v':
            self.dif = 'e'
            self.ping.pause = True
            self.ping.dif = self.dif
            self.ping.easy()
            self.frame1.itemconfigure(self.difgame, text='Easy')
            self.frame1.coords(self.sqrdif,
                               int((x1 - 150) - (y1 // 6 * 4 / 2)), y1 - 30 - y1 // 6, int((x1 - 150) + (y1 // 6 * 4 / 2)), y1 - 30 + y1 // 6)
        self.ping.restart()

    def sidegamecommand(self, event=None):
        x1, y1 = int(eval(str(self.frame1['width']))), int(eval(str(self.frame1['height'])))  # side option

        if self.side == 'left':
            self.side = 'right'
            self.ping.pause = True
            self.ping.side = self.side
            self.ping.restart()
            self.frame1.itemconfigure(self.sidegame, text='Right')
            self.frame1.coords(self.sqrside,
                              int((x1 - 50) - (y1 // 6 * 5 / 2)), y1 - 30 - y1 // 6, int((x1 - 50) + (y1 // 6 * 5 / 2)), y1 - 30 + y1 // 6)
        elif self.side == 'right':
            self.side = 'left'
            self.ping.pause = True
            self.ping.side = self.side
            self.ping.restart()
            self.frame1.itemconfigure(self.sidegame, text='Left')
            self.frame1.coords(self.sqrside,
                              int((x1 - 50) - (y1 // 6 * 4 / 2)), y1 - 30 - y1 // 6, int((x1 - 50) + (y1 // 6 * 4 / 2)), y1 - 30 + y1 // 6)

    def startgamecommand(self, event=None):
        x1, y1 = int(eval(str(self.frame1['width']))), int(eval(str(self.frame1['height'])))  # side option

        if self.start == 'left':
            self.start = 'right'
            self.ping.pause = True
            self.ping.start = self.start
            self.ping.restart()
            self.frame1.itemconfigure(self.startgame, text='Right')
            self.frame1.coords(self.sqrstart,
                              int((x1 - 350) - (y1 // 6 * 5 / 2)), y1 - 30 - y1 // 6, int((x1 - 350) + (y1 // 6 * 5 / 2)), y1 - 30 + y1 // 6)
        elif self.start == 'right':
            self.start = 'left'
            self.ping.pause = True
            self.ping.start = self.start
            self.ping.restart()
            self.frame1.itemconfigure(self.startgame, text='Left')
            self.frame1.coords(self.sqrstart,
                              int((x1 - 350) - (y1 // 6 * 4 / 2)), y1 - 30 - y1 // 6, int((x1 - 350) + (y1 // 6 * 4 / 2)), y1 - 30 + y1 // 6)
        self.ping.setside()

    def inleavegame(self, event=None):  # motion effect
        self.frame1.itemconfigure(self.sqrleave, width=5)
        self.frame1.itemconfigure(self.leavegame, font=Font(size=eval(str(self.frame1['height'])) // 2 + 3))
        Sound('audio\\motioneffect1.mp3').play()
        Cursor('media\\cursor\\hand.cur')

    def outleavegame(self, event=None):
        self.frame1.itemconfigure(self.sqrleave, width=1)
        self.frame1.itemconfigure(self.leavegame, font=Font(size=eval(str(self.frame1['height'])) // 2))
        Sound('audio\\motioneffect2.mp3').play()
        Cursor('media\\cursor\\cursor.cur')

    def inrestartgame(self, event=None):
        self.frame1.itemconfigure(self.sqrrestart, width=5)
        self.frame1.itemconfigure(self.restartgame, font=Font(size=eval(str(self.frame1['height'])) // 2 + 3))
        Sound('audio\\motioneffect1.mp3').play()
        Cursor('media\\cursor\\hand.cur')

    def outrestartgame(self, event=None):
        self.frame1.itemconfigure(self.sqrrestart, width=1)
        self.frame1.itemconfigure(self.restartgame, font=Font(size=eval(str(self.frame1['height'])) // 2))
        Sound('audio\\motioneffect2.mp3').play()
        Cursor('media\\cursor\\cursor.cur')

    def inpausegame(self, event=None):
        self.frame1.itemconfigure(self.sqrpause, width=5)
        self.frame1.itemconfigure(self.pausegame, font=Font(size=eval(str(self.frame1['height'])) // 2 + 3))
        Sound('audio\\motioneffect1.mp3').play()
        Cursor('media\\cursor\\hand.cur')

    def outpausegame(self, event=None):
        self.frame1.itemconfigure(self.sqrpause, width=1)
        self.frame1.itemconfigure(self.pausegame, font=Font(size=eval(str(self.frame1['height'])) // 2))
        Sound('audio\\motioneffect2.mp3').play()
        Cursor('media\\cursor\\cursor.cur')

    def inaudiogame(self, event=None):
        self.frame1.itemconfigure(self.sqraudio, width=5)
        self.frame1.itemconfigure(self.audiogame, font=Font(size=eval(str(self.frame1['height'])) // 2 + 3))
        Sound('audio\\motioneffect1.mp3').play()
        Cursor('media\\cursor\\hand.cur')

    def outaudiogame(self, event=None):
        self.frame1.itemconfigure(self.sqraudio, width=1)
        self.frame1.itemconfigure(self.audiogame, font=Font(size=eval(str(self.frame1['height'])) // 2))
        Sound('audio\\motioneffect2.mp3').play()
        Cursor('media\\cursor\\cursor.cur')

    def inmode(self, event=None):
        self.frame1.itemconfigure(self.sqrmode, width=5)
        self.frame1.itemconfigure(self.modegame, font=Font(size=eval(str(self.frame1['height'])) // 6 + 3, weight='bold'))
        Sound('audio\\motioneffect1.mp3').play()
        Cursor('media\\cursor\\hand.cur')

    def outmode(self, event=None):
        self.frame1.itemconfigure(self.sqrmode, width=1)
        self.frame1.itemconfigure(self.modegame, font=Font(size=eval(str(self.frame1['height'])) // 6, weight='bold'))
        Sound('audio\\motioneffect2.mp3').play()
        Cursor('media\\cursor\\cursor.cur')

    def indif(self, event=None):
        self.frame1.itemconfigure(self.sqrdif, width=5)
        self.frame1.itemconfigure(self.difgame, font=Font(size=eval(str(self.frame1['height'])) // 6 + 3, weight='bold'))
        Sound('audio\\motioneffect1.mp3').play()
        Cursor('media\\cursor\\hand.cur')

    def outdif(self, event=None):
        self.frame1.itemconfigure(self.sqrdif, width=1)
        self.frame1.itemconfigure(self.difgame, font=Font(size=eval(str(self.frame1['height'])) // 6, weight='bold'))
        Sound('audio\\motioneffect2.mp3').play()
        Cursor('media\\cursor\\cursor.cur')

    def inside(self, event=None):
        self.frame1.itemconfigure(self.sqrside, width=5)
        self.frame1.itemconfigure(self.sidegame, font=Font(size=eval(str(self.frame1['height'])) // 6 + 3, weight='bold'))
        Sound('audio\\motioneffect1.mp3').play()
        Cursor('media\\cursor\\hand.cur')

    def outside(self, event=None):
        self.frame1.itemconfigure(self.sqrside, width=1)
        self.frame1.itemconfigure(self.sidegame, font=Font(size=eval(str(self.frame1['height'])) // 6, weight='bold'))
        Sound('audio\\motioneffect2.mp3').play()
        Cursor('media\\cursor\\cursor.cur')

    def instart(self, event=None):
        self.frame1.itemconfigure(self.sqrstart, width=5)
        self.frame1.itemconfigure(self.startgame, font=Font(size=eval(str(self.frame1['height'])) // 6 + 3, weight='bold'))
        Sound('audio\\motioneffect1.mp3').play()
        Cursor('media\\cursor\\hand.cur')

    def outstart(self, event=None):
        self.frame1.itemconfigure(self.sqrstart, width=1)
        self.frame1.itemconfigure(self.startgame, font=Font(size=eval(str(self.frame1['height'])) // 6, weight='bold'))
        Sound('audio\\motioneffect2.mp3').play()
        Cursor('media\\cursor\\cursor.cur')
        
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
                f = open('data\\pingpong.dat', 'r')
                l = f.read()
            except:
                f = open('data\\pingpong.dat', 'a')
                f.close()
                l = '<EMPTY>'
            self.thistory['stat'] = 'normal'
            self.thistory.delete('0.0', 'end')
            self.thistory.insert('end', l)
            self.thistory['stat'] = 'disabled'
            WriteFile('data\\ppstat.dat', '')

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
        f = open('data\\pingpong.dat', 'w')
        f.write('')
        f.close()

    def playtest(self, event=None):
        if self.sound == True:
            self.son.volp()
        elif self.sound == False:
            self.son.volm()


if __name__ == '__main__':
    fen = Tk()
    fen.wm_attributes('-fullscreen', True)
    Cursor('media\\cursor\\cursor.cur')
    a = Pong(fen, fen).grid()
    fen.mainloop()
    Cursor()

