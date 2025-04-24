"""
This library allows you to create custom, designed widgets from canvas objects to create a more gaming-like look.
because tkinter's native widgets are less modern.
However, since these are canvas objects, they obviously require a canvas as the master.
I called then with bubble prefix just for fun.
"""

from pyfunct import Sound, Cursor
from tkinter.font import Font
from tkinter import Canvas, Tk

text = '<Text>'


class BubbleSquare(object):

    def __init__(self, master, x, y, bg='grey10', fg='white', og='black', text=text,
                 command=None, width=80, height=80, length=1,
                 font=['helvetica', 25, 'bold'], son=True):
        """A normal button with hard corner"""
        self.master = master
        self.x, self.y = x, y
        self.bg, self.fg, self.og = bg, fg, og
        self.text = text
        self.command = command
        self.wdt, self.hgt, self.lgt = width, height, length
        self.font = font
        f = ''
        for ww in self.font:
            f += str(ww)
            f += ' '
        self.son = son

        self.square = self.master.create_rectangle(x - self.wdt / 2, y - self.hgt / 2, x + self.wdt / 2, y + self.hgt / 2,
                                                   width=self.lgt, fill=self.bg, outline=self.og)
        self.title = self.master.create_text(x, y, text=text, fill=fg, font=f.strip())

        self.master.tag_bind(self.square, '<Enter>', self.inbubble)
        self.master.tag_bind(self.title, '<Enter>', self.inbubble)
        self.master.tag_bind(self.square, '<Leave>', self.outbubble)
        self.master.tag_bind(self.title, '<Leave>', self.outbubble)
        self.master.tag_bind(self.square, '<Button-1>', self.onclicbubble)
        self.master.tag_bind(self.title, '<Button-1>', self.onclicbubble)

    def inbubble(self, event=None):
        # Effect of widget when cursor is hover.
        f1 = self.font.copy()
        f1[1] = self.font[1] + 3
        f = ''
        for ww in f1:
            f += str(ww)
            f += ' '
        self.master.itemconfigure(self.square, width=self.lgt + 1)
        self.master.itemconfigure(self.title, font=f.strip())
        if self.son == True:
            Sound('audio\\motioneffect1.mp3').play()
        Cursor('media\\cursor\\hand.cur')

    def outbubble(self, event=None):
        # The widget regains its basic properties with the cursor leaving
        f1 = self.font.copy()
        f = ''
        for ww in f1:
            f += str(ww)
            f += ' '
        self.master.itemconfigure(self.square, width=self.lgt)
        self.master.itemconfigure(self.title, font=f.strip())
        if self.son == True:
            Sound('audio\\motioneffect2.mp3').play()
        Cursor('media\\cursor\\cursor.cur')

    def onclicbubble(self, event=None):
        if self.command:
            self.command()

    def auto_size(self, event=None):
        # This function resizes the widget depending on its content
        wdt = len(self.text) * self.font[1] / 1.2
        hgt = self.font[1] + 15
        
        self.master.coords(self.square, self.x - wdt / 2, self.y - hgt / 2, self.x + wdt / 2, self.y + hgt / 2)

        self.wdt, self.hgt = wdt, hgt


class BubbleSmoothSquare(object):

    def __init__(self, master, x, y, bg='grey10', fg='white', og='black', text=text,
                 command=None, width=80, height=80, length=1,
                 font=['helvetica', 25, 'bold'], son=True):
        """A button with rounded corner"""
        self.master = master
        self.x, self.y = x, y
        self.bg, self.fg, self.og = bg, fg, og
        self.text = text
        self.command = command
        self.wdt, self.hgt, self.lgt = width, height, length
        self.font = font
        f = ''
        for ww in self.font:
            f += str(ww)
            f += ' '
        self.son = son

        a, b = self.wdt / 2, self.hgt / 2

        self.square = self.master.create_polygon(x - a - 3, y - b, x - a, y - b - 3, x + a, y - b - 3, x + a + 3, y - b,
                                                 x + a + 3, y + b, x + a, y + b + 3, x - a, y + b + 3, x - a - 3, y + b,
                                                 width=self.lgt, fill=self.bg, outline=self.og)
        self.title = self.master.create_text(x, y, text=text, fill=fg, font=f.strip())

        self.master.tag_bind(self.square, '<Enter>', self.inbubble)
        self.master.tag_bind(self.title, '<Enter>', self.inbubble)
        self.master.tag_bind(self.square, '<Leave>', self.outbubble)
        self.master.tag_bind(self.title, '<Leave>', self.outbubble)
        self.master.tag_bind(self.square, '<Button-1>', self.onclicbubble)
        self.master.tag_bind(self.title, '<Button-1>', self.onclicbubble)

    def inbubble(self, event=None):
        f1 = self.font.copy()
        f1[1] = self.font[1] + 3
        f = ''
        for ww in f1:
            f += str(ww)
            f += ' '
        self.master.itemconfigure(self.square, width=self.lgt + 1)
        self.master.itemconfigure(self.title, font=f.strip())
        if self.son == True:
            Sound('audio\\motioneffect1.mp3').play()
        Cursor('media\\cursor\\hand.cur')

    def outbubble(self, event=None):
        f1 = self.font.copy()
        f = ''
        for ww in f1:
            f += str(ww)
            f += ' '
        self.master.itemconfigure(self.square, width=self.lgt)
        self.master.itemconfigure(self.title, font=f.strip())
        if self.son == True:
            Sound('audio\\motioneffect2.mp3').play()
        Cursor('media\\cursor\\cursor.cur')

    def onclicbubble(self, event=None):
        if self.command:
            self.command()

    def auto_size(self, event=None):
        a = len(self.text) * self.font[1] / 2
        b = self.font[1]
        x = self.x
        y = self.y
        
        self.master.coords(self.square, x - a - 3, y - b, x - a, y - b - 3, x + a, y - b - 3, x + a + 3, y - b,
                            x + a + 3, y + b, x + a, y + b + 3, x - a, y + b + 3, x - a - 3, y + b)

        self.wdt, self.hgt = a, b


class BubbleScale(object):

    def __init__(self, master, x, y, bg='grey10', fg='white', og='black',
                 scalebg='grey20', scaleog='black', from_=0, to=10, value=0, step=1,
                 variable=None, command=None, width=12, height=28, length=1,
                 scalewidth=200, scaleheight=6, scalelength=1,
                 font=['helvetica', 9, 'bold'], son=True):
        """A scale similar to tkinter.Scale"""
        self.master = master
        self.x, self.y = x, y
        self.bg, self.fg, self.og = bg, fg, og
        self.sbg, self.sog = scalebg, scaleog
        self.from_, self.to = from_, to
        self.value, self.variable, self.step = value, variable, step
        self.command = command
        self.wdt, self.hgt, self.lgt = width, height, length
        self.swdt, self.shgt, self.slgt = scalewidth, scaleheight, scalelength
        self.font = font
        self.motion = False
        f = ''
        for ww in self.font:
            f += str(ww)
            f += ' '
        self.son = son

        a, b, c, d = self.swdt / 2, self.shgt / 2, self.wdt / 2, self.hgt / 2
        e, f = c + len(str(self.value)) * font[1] / 4, d / 2 + font[1] / 4
        x, y = self.x, self.y
        self.posx = self.x
        self.y2 = self.y - (self.y - d - font[1])

        self.scale = self.master.create_polygon(x - a - 3, y - b, x - a, y - b - 3, x + a, y - b - 3, x + a + 3, y - b,
                                                 x + a + 3, y + b, x + a, y + b + 3, x - a, y + b + 3, x - a - 3, y + b,
                                                fill=self.sbg, outline=self.sog, width=self.slgt)
        self.setperiod()

        self.square = self.master.create_rectangle(x - e, y - f, x + e, y + f, width=1, outline=og,
                                                   fill=bg)
        self.text = self.master.create_text(x, y, text=value, fill=fg,
                                            font=Font(size=font[1], weight='bold'))
        
        self.button = BubbleSmoothSquare(self.master, x, y, self.bg, self.fg, self.og, str(self.value),
                                        None, self.wdt, self.hgt, self.lgt,
                                        self.font, self.son)
        self.button.auto_size()
        self.default_position()

        # self.setinitial()

        self.master.tag_bind(self.scale, '<Button-1>', self.inmotion)
        self.master.tag_bind(self.scale, '<Button1-Motion>', self.inmotion)
        self.master.tag_bind(self.scale, '<ButtonRelease>', self.outmotion)
        self.master.tag_bind(self.scale, '<Button-1>', self.onclic)
        self.master.tag_bind(self.button.square, '<Button1-Motion>', self.inmotion)
        self.master.tag_bind(self.button.title, '<Button1-Motion>', self.inmotion)
        self.master.tag_bind(self.button.square, '<ButtonRelease>', self.outmotion)
        self.master.tag_bind(self.button.title, '<ButtonRelease>', self.outmotion)
        self.master.tag_bind(self.button.square, '<Button-1>', self.onclic)
        self.master.tag_bind(self.button.title, '<Button-1>', self.onclic)

    def setperiod(self, event=None):
        # This function calculates the length of the scale to place the marks accordingly
        nombre = len(range(self.from_, self.to, self.step))
        d0 = (self.x - self.swdt / 2)
        n = 200 / nombre
        self.period = []
        a = self.from_
        self.val = []
        for ww in range(nombre + 1):
            self.master.create_line(d0, self.y - 1, d0, self.y + 1, fill=self.fg)
            self.period.append(d0)
            self.val.append(a)
            a += self.step
            if a > self.to:
                a = self.to
            d0 += n
        if len(self.period) > 1:
            d = self.period[1] - self.period[0]
        else:
            d = 0
        d /= 2
        self.dict = {}
        for ww in self.period:
            for xx in range(int(ww - d), int(ww + d + 1)):
                self.dict[xx] = self.val[self.period.index(ww)]

        try:
            self.master.lift(self.button.square)
            self.master.lift(self.button.title)
        except:
            pass

    def default_position(self, event=None):
        # Set the default position of thumb
        self.setperiod()
        a = self.period[self.val.index(self.value)]
        x = a - self.posx
        self.posx = a
        self.master.move(self.button.title, x, 0)
        self.master.move(self.button.square, x, 0)
        self.master.move(self.square, x, 0)
        self.master.move(self.text, x, 0)
        self.button.text = str(self.value)
        self.button.x = self.posx
        self.master.itemconfigure(self.button.title, text=self.value)
        self.master.itemconfigure(self.text, text=self.value)
    
    def inmotion(self, event=None):
        # Adapts the scale value according to the position of your thumb
        if len(self.period) > 1:
            d = self.period[1] - self.period[0]
        else:
            d = 0
        d /= 2

        if self.posx < self.x - self.swdt / 2:
            x = self.x - self.swdt / 2 - self.posx
        elif self.posx > self.x + self.swdt:
            x = self.posx - self.x - self.swdt / 2
            self.master.move(self.button.title, x, 0)
            self.master.move(self.button.square, x, 0)
            self.master.move(self.square, x, 0)
            self.master.move(self.text, x, 0)
        
        if self.x - self.swdt / 2 <= event.x <= self.x + self.swdt / 2:
            x = event.x - self.posx
            self.master.itemconfigure(self.text, text=self.dict[int(event.x)])
            self.master.move(self.button.title, x, 0)
            self.master.move(self.button.square, x, 0)
            self.master.move(self.square, x, 0)
            self.master.move(self.text, x, 0)
            self.posx = event.x
            self.value = self.dict[int(event.x)]
            self.button.text = str(self.value)
            self.button.x = self.posx
            self.button.auto_size()
            if self.variable:
                self.variable.set(self.value)
            if self.son == True:
                if self.value % 4 == 0:
                    Sound('audio\\motioneffect4.mp3').play()
            self.execcommand()

    def outmotion(self, event=None):
        if self.motion == True:
            self.master.move(self.square, 0, self.y2)
            self.master.move(self.text, 0, self.y2)
            self.master.itemconfigure(self.button.title, text=self.value)
            self.motion = False
            self.ro(self.posx)

    def onclic(self, event=None):
        self.master.move(self.square, 0, -self.y2)
        self.master.move(self.text, 0, -self.y2)
        self.master.itemconfigure(self.button.title, text='')
        self.motion = True

    def ro(self, x):
        e, f = self.wdt / 2 + len(str(self.value)) * self.font[1] / 4, self.hgt / 2 / 2 + self.font[1] / 4
        self.master.coords(self.square, x - e, self.y - f, x + e, self.y + f)        

    def execcommand(self, event=None):
        if self.command:
            self.command()

#################################################################################################

#################################################################################################


class BubbleProgress(object):

    def __init__(self, master, x, y, bg='grey10', og='grey60', activebg='grey45',
                 width=200, height=6, infinity=False):
        """Similar to tkinter.ProgressBar"""
        self.master = master
        self.x, self.y = x, y
        self.bg, self.og, self.ag = bg, og, activebg
        self.wdt, self.hgt = width, height
        self.inf = infinity
        self.posx = self.x - self.wdt / 2
        self.dir = 'right'

        a = self.wdt / 2; b = self.hgt / 2

        self.barre = self.master.create_polygon(x - a - 3, y - b, x - a, y - b - 3, x + a, y - b - 3, x + a + 3, y - b,
                                                 x + a + 3, y + b, x + a, y + b + 3, x - a, y + b + 3, x - a - 3, y + b,
                                                fill=bg, outline=og, width=1)
        
        self.pbarre = self.master.create_polygon(x - a - 3, y - b, x - a, y - b - 3, x - a, y - b - 3, x - a + 3, y - b,
                                                 x - a + 3, y + b, x - a, y + b + 3, x - a, y + b + 3, x - a - 3, y + b,
                                                fill=activebg, width=0)

    def update(self, value=1):
            if self.inf == False:
                self.fini(value)
            elif self.inf == True:
                self.master.after(10, self.infini)

    def fini(self, value):
        # The effect of the bar if it has a % limit
        if self.posx < (self.x + (self.wdt / 2)):
            self.posx += value
            x = self.x; y = self.y
            a = self.wdt / 2; b = self.hgt / 2
            p = self.posx
            self.master.coords(self.pbarre, x - a - 3, y - b, x - a, y - b - 3, p, y - b - 3, p + 3, y - b,
                               p + 3, y + b, p + 3, y + b + 3, x - a, y + b + 3, x - a - 3, y - b)
            self.master.update_idletasks()

    def infini(self, value):
        # The effect of the bar if it does not have a % limit
        if self.posx >= self.x + self.wdt / 2:
            self.dir = 'left'
        if self.posx <= self.x - self.wdt / 2:
            self.dir = 'right'
        if self.dir == 'left':
            self.master.move(self.pbarre, -value, 0)
        else:
            self.master.move(self.pbarre, value, 0)
        self.master.update_idletasks()


class BubbleLabel(object):

    def __init__(self, master, x, y, bg='grey10', fg='light blue', og='grey20',
                 info=text, width=200, height=250, font=['helvetica', 10], line=10):
        """Similar to tkinter.Label"""
        self.master = master
        self.x, self.y = x, y
        self.wdt, self.hgt = width, height
        self.bg, self.fg, self.og = bg, fg, og
        self.font = font
        self.info = info
        self.line = 10

        f = ''
        for ww in self.font:
            f += str(ww)
            f += ' '

        a, b = self.wdt / 2, self.hgt / 2

        num = int(self.wdt / (self.font[1]))
        self.txt = ''
        for ww in range(len(self.info)):
            if ww % num == 0 and ww != 0:
                self.txt += '\n'
            self.txt += self.info[ww]

        self.square = self.master.create_polygon(x - a - 3, y - b, x - a, y - b - 3, x + a, y - b - 3, x + a + 3, y - b,
                                                x + a + 3, y + b, x + a, y + b + 3, x - a, y + b + 3, x - a - 3, y + b,
                                                fill=bg, outline=og, width=1)
        self.text = self.master.create_text(x, y, text=self.txt, fill=self.fg, font=f)

    def auto_size(self):
        x, y = self.x, self.y

        l = []
        m = []
        for ww in self.txt:
            if ww == '\n':
                l.append(m)
                del(m[:])
            else:
                m.append(ww)
        s = 0
        for ww in l:
            if int(len(ww)) > s:
                s = len(ww)
        
        a = s * self.font[1] / 1.5
        b = self.font[1] * self.txt.count('\n')

        self.master.coords(self.square, x - a - 3, y - b, x - a, y - b - 3, x + a, y - b - 3, x + a + 3, y - b,
                                                x + a + 3, y + b, x + a, y + b + 3, x - a, y + b + 3, x - a - 3, y + b)


class BubbleOval(object):

    def __init__(self, master, x, y, width=80, height=80, info=None, bg='', og='black',
                fg='black', command=None, font=['helvetica', 9, 'bold'], son=True):
        """A circular button"""
        self.master = master
        self.x, self.y = x, y
        self.wdt, self.hgt = width, height
        self.info = info
        self.bg, self.og, self.fg = bg, og, fg
        self.command = command
        self.font = font
        self.son = son

        f = ''
        for ww in font:
            f += str(ww)
            f += ' '

        a = self.wdt / 2; b = self.hgt / 2

        self.circle = self.master.create_oval(x - a, y - b, x + a, y + b, fill=self.bg, outline=self.og, width=1)
        self.square = self.circle

        if self.info:
            self.title = self.master.create_text(x, y, text=self.info, fill=self.fg, font=f)

        self.master.tag_bind(self.square, '<Enter>', self.inbubble)
        self.master.tag_bind(self.square, '<Leave>', self.outbubble)
        self.master.tag_bind(self.square, '<Button-1>', self.onclicbubble)

        if self.info:
            self.master.tag_bind(self.title, '<Leave>', self.outbubble)
            self.master.tag_bind(self.title, '<Enter>', self.inbubble)
            self.master.tag_bind(self.title, '<Button-1>', self.onclicbubble)

    def inbubble(self, event=None):
        f1 = self.font.copy()
        f1[1] = self.font[1] + 3
        f = ''
        for ww in f1:
            f += str(ww)
            f += ' '
        self.master.itemconfigure(self.square, width=2)
        if self.info:
            self.master.itemconfigure(self.title, font=f.strip())
        if self.son == True:
            Sound('audio\\motioneffect1.mp3').play()
        Cursor('media\\cursor\\hand.cur')

    def outbubble(self, event=None):
        f1 = self.font.copy()
        f = ''
        for ww in f1:
            f += str(ww)
            f += ' '
        self.master.itemconfigure(self.square, width=1)
        if self.info:
            self.master.itemconfigure(self.title, font=f.strip())
        if self.son == True:
            Sound('audio\\motioneffect2.mp3').play()
        Cursor('media\\cursor\\cursor.cur')

    def onclicbubble(self, event=None):
        if self.command:
            self.command()

    def auto_size(self):
        if self.info:
            a = len(self.info) * self.font[1] / 1.5
            b = self.font[1]
            x = self.x
            y = self.y
            
            self.master.coords(self.square, x - a, y - b, x + a, y + b)

            self.wdt, self.hgt = a, b

    def resize(self, width=80, height=80):
        self.wdt = width; self.hgt = height
        self.master.coords(self.square, self.x - self.wdt / 2, self.y - self.hgt / 2, self.x + self.wdt / 2, self.y + self.hgt / 2)

    def moveto(self, x=0, y=0):
        a, b = x - self.x, y - self.y
        self.x = x; self.y = y
        self.master.move(self.square, a, b)
        if self.info:
            self.master.move(self.title, a, b)


class BubbleTriangle(object):

    def __init__(self, master, x, y, width=80, height=80, length=1, text=text, bg='grey10', og='black',
                fg='white', command=None, font=['helvetica', 9, 'bold'], son=True, mode='right'):
        """A triangular button"""
        self.master = master
        self.x, self.y = x, y
        self.bg, self.fg, self.og = bg, fg, og
        self.text = text
        self.command = command
        self.wdt, self.hgt, self.lgt = width, height, length
        self.font = font
        self.mode = mode
        f = ''
        for ww in self.font:
            f += str(ww)
            f += ' '
        self.son = son

        # Point the triangle towards the specified direction
        if self.mode == 'left':
            self.square = self.master.create_polygon(x - self.wdt / 2, y - self.hgt / 2, x + self.wdt / 2, y, x - self.wdt / 2, y + self.hgt / 2,
                                                   width=self.lgt, fill=self.bg, outline=self.og)
            self.title = self.master.create_text(x - len(text) * 2, y, text=text, fill=fg, font=f.strip())
        else:
            self.square = self.master.create_polygon(x + self.wdt / 2, y - self.hgt / 2, x - self.wdt / 2, y, x + self.wdt / 2, y + self.hgt / 2,
                                                   width=self.lgt, fill=self.bg, outline=self.og)
            self.title = self.master.create_text(x + len(text) * 2, y, text=text, fill=fg, font=f.strip())

        self.master.tag_bind(self.square, '<Enter>', self.inbubble)
        self.master.tag_bind(self.title, '<Enter>', self.inbubble)
        self.master.tag_bind(self.square, '<Leave>', self.outbubble)
        self.master.tag_bind(self.title, '<Leave>', self.outbubble)
        self.master.tag_bind(self.square, '<Button-1>', self.onclicbubble)
        self.master.tag_bind(self.title, '<Button-1>', self.onclicbubble)

    def inbubble(self, event=None):
        f1 = self.font.copy()
        f1[1] = self.font[1] + 3
        f = ''
        for ww in f1:
            f += str(ww)
            f += ' '
        self.master.itemconfigure(self.square, width=self.lgt + 1)
        self.master.itemconfigure(self.title, font=f.strip())
        if self.son == True:
            Sound('audio\\motioneffect1.mp3').play()
        Cursor('media\\cursor\\hand.cur')

    def outbubble(self, event=None):
        f1 = self.font.copy()
        f = ''
        for ww in f1:
            f += str(ww)
            f += ' '
        self.master.itemconfigure(self.square, width=self.lgt)
        self.master.itemconfigure(self.title, font=f.strip())
        if self.son == True:
            Sound('audio\\motioneffect2.mp3').play()
        Cursor('media\\cursor\\cursor.cur')

    def onclicbubble(self, event=None):
        if self.command:
            self.command()

    def auto_size(self, event=None):
        wdt = len(self.text) * self.font[1] * 1.5
        hgt = self.font[1] + 15 + len(self.text)
        if self.mode == 'left':
            self.master.coords(self.square, self.x - wdt / 2, self.y - hgt / 2, self.x + wdt / 2, self.y, self.x - wdt / 2, self.y + hgt / 2)
        else:
            self.master.coords(self.square, self.x + wdt / 2, self.y - hgt / 2, self.x - wdt / 2, self.y, self.x + wdt / 2, self.y + hgt / 2)

        self.wdt, self.hgt = wdt, hgt


class BubbleBoard(object):

    def __init__(self, master, x, y, width=80, height=80, bg='pink', og='black'):
        """Similar to tkinter.Message"""
        self.master = master
        self.x, self.y = x, y
        self.wdt, self.hgt = width, height
        self.bg, self.og = bg, og

        a, b = self.wdt / 2, self.hgt / 2
        
        self.square = self.master.create_polygon(x - a - 3, y - b, x - a, y - b - 3, x + a, y - b - 3, x + a + 3, y - b,
                                                x + a + 3, y + b, x + a, y + b + 3, x - a, y + b + 3, x - a - 3, y + b,
                                                fill=bg, outline=og, width=1)

        self.lwdt = list(); self.lhgt = list()
        self.o = list()

    def add(self, obj, width, height):
        self.o.append(obj)
        self.lwdt.append(width); self.lhgt.append(height)
        print(self.lwdt)

        swd = self.lwdt.copy()
        swd.sort()
        self.wdt = swd[len(self.lwdt) - 1] + 30
       
        self.hgt = 0
        for ww in self.lhgt:
            self.hgt += 10
            self.hgt += ww
            self.hgt += 5 
            
        self.auto_size()
        
        a = obj.x - self.x; b = obj.y - self.y
        self.master.move(obj, a, b)

        for ww in self.o:
            a = ww.x - self.x - self.lwdt[self.object.index(ww)] / 2
            b = ww.y - self.y - self.lhgt[self.object.index(ww)] / 2 + 15
            self.master.move(ww, a, b)
            ww.x = ww.x + a; ww.y = ww.y + b

    def auto_size(self):
        x = self.x; y = self.y
        a, b = self.wdt / 2, self.hgt / 2

        self.master.coords(self.square, x - a - 3, y - b, x - a, y - b - 3, x + a, y - b - 3, x + a + 3, y - b,
                                                x + a + 3, y + b, x + a, y + b + 3, x - a, y + b + 3, x - a - 3, y + b)
        

class BubbleEmpty(object):

    def __init__(self, master, x, y, bg='grey10', og='black',
                 width=2, height=80, length=0):
        """Just an empty widget"""
        self.master = master
        self.x, self.y = x, y
        self.bg, self.og = bg, og
        self.wdt, self.hgt, self.lgt = width, height, length
        self.actbg, self.actog, self.actlgt = 'grey20', 'black', 0
        
        a, b = self.wdt / 2, self.hgt / 2
        x, y = self.x, self.y

        self.square = self.master.create_polygon(x - a - 3, y - b, x - a, y - b - 3, x + a, y - b - 3, x + a + 3, y - b,
                                                 x + a + 3, y + b, x + a, y + b + 3, x - a, y + b + 3, x - a - 3, y + b,
                                                 width=self.lgt, fill=self.bg, outline=self.og)
        
        self.master.tag_bind(self.square, '<Enter>', self.inobject)
        self.master.tag_bind(self.square, '<Leave>', self.outobject)
    
    def resize(self, width=2, height=80):
        self.wdt, self.hgt = width, height
        
        a, b = self.wdt / 2, self.hgt / 2
        x, y = self.x, self.y
        
        self.master.coords(self.square, x - a - 3, y - b, x - a, y - b - 3, x + a, y - b - 3, x + a + 3, y - b,
                                                 x + a + 3, y + b, x + a, y + b + 3, x - a, y + b + 3, x - a - 3, y + b)
    
    def modify(self, bg='grey10', og='black', length=0):
        self.bg, self.og = bg, og
        self.lgt = length
        
        self.master.itemconfigure(self.square, fill=self.bg, outline=self.og, width=self.lgt)
    
    def move(self, x=None, y=None):
        if x: tox = x
        else: tox = self.x
            
        if y: toy = y
        else: toy = self.y
        
        a = tox - self.x; b = toy - self.y
        
        self.master.move(self.square, a, b)
        self.x += a; self.y += b
    
    def active(self, bg='grey20', og='black', length=0):
        self.actbg, self.actog, self.actlgt = bg, og, length
    
    def inobject(self, event=None):
        self.master.itemconfigure(self.square, fill=self.actbg, outline=self.actog, width=self.actlgt)
    
    def outobject(self, event=None):
        self.master.itemconfigure(self.square, fill=self.bg, outline=self.og, width=self.lgt)


if __name__ == '__main__':
    fen = Tk()
    can = Canvas(fen, width=1000, height=600, bg='white')
    a = BubbleScale(can, 200, 100, from_=0, to=100, step=1, fg='blue', value=0)
            
    b = BubbleSquare(can, 200, 150, text='Bouton', og='purple')
    b.auto_size()

    c = BubbleSmoothSquare(can, x=200, y=210, text='Smooth', og='purple')
    c.auto_size()

    d = BubbleProgress(can, 200, 250, infinity=False)
    d.update(60)

    e = BubbleLabel(can, 200, 400, info="This is an example  of text displayed on a BubbleBoard")
    e.auto_size()

    f = BubbleOval(can, 500, 100, son=False, info='Oval')

    g = BubbleTriangle(can, 500, 200, text='Triangle', og='purple')
    g.auto_size()

    h = BubbleEmpty(can, 500, 300, width=80, height=2)
    
    can.pack()
    fen.mainloop()
    Cursor()

