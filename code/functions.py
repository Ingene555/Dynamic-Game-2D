from pyfunct import Assign, Cursor, Get
from bubblewidgets import BubbleEmpty
from tkinter import Frame, Canvas, Label, Message as Msg, Tk
from PIL import Image, ImageTk
from tkinter.font import Font


# class of squareImage
class SquareImage(Frame):

    def __init__(self, master, image, command=None, **kw):
        '''Image button'''  # button that contain image
        Frame.__init__(self, master, kw)  # the widget is based on a Frame widget
        self.config(bg='black', bd=0, highlightthickness=0, relief='flat')
        self.master = master
        self.command = command
        
        self.po = Image.open(image)  # load the image and create interface width Canvas, Label and Message
        po = self.po.resize((120, 70))
        self.photo = ImageTk.PhotoImage(po)
        self.po.close()
        self.can = Canvas(self)

        self.can.config(bg='black', bd=0, highlightthickness=0,
                    relief='flat', width=self.photo.width() + 5, height=self.photo.height() + 5)

        self.x = eval(str(self.can['width'])); self.y = eval(str(self.can['height']))
        self.q1 = self.can.create_rectangle(self.x, 0, self.x * 2, self.y, width=0,
                                            fill='blue')
        self.q2 = self.can.create_rectangle(-self.x, 0, 0, self.y, width=0,
                                            fill='blue')
        self.image = self.can.create_image(eval(str(self.can['width'])) / 2,
                                           eval(str(self.can['height'])) / 2, image=self.photo)

        self.label = Label(self, bg='black', bd=0, highlightthickness=0, fg='grey60',
                    relief='flat', font=Font(family='text\\font\\Gameplay.ttf', size=15, weight='bold'))
        
        self.text = Msg(self, bg='black', bd=0, highlightthickness=0, anchor='w', fg='grey50',
                    width=190, relief='flat', font=Font(family='gamecuben', size=7))

        self.can.grid(row=1, column=1, rowspan=2, sticky='nsew', pady=2)
        self.label.grid(row=1, column=2, sticky='ew')
        self.text.grid(row=2, column=2, sticky='nsew')

        self['height'] = self.can['height']  # keep frame same height as canvas of image
        self['width'] = eval(self.can['width']) + 100
        
        self.qx = self.x
        self.nx = 0

        self.can.tag_bind(self.image, '<Enter>', self.inimage)
        Assign(self.label, self.inimage, ['Enter'])

        self.can.tag_bind(self.image, '<Leave>', self.outimage)
        Assign(self.label, self.outimage, ['Leave'])

        self.can.tag_bind(self.image, '<Button-1>', self.onclic)
        Assign(self.label, self.onclic, ['Button-1'])

        self.id1 = None
        self.id2 = None
        
    def onimage(self):
        if self.id2:
            self.after_cancel(self.id2)
            self.id2 = None
        self.label['fg'] = 'purple'
        if int(self.qx) <= int(self.x) / 2:
            self.nx = 0
        else:
            self.nx = 1
            self.can.move(self.q1, -self.nx, 0)
            self.can.move(self.q2, self.nx, 0)
            self.qx -= self.nx
        if self.qx > self.x / 2:
            self.id1 = self.after(1, self.onimage)

    def inimage(self, event):
        self.cur = Cursor('media\\cursor\\hand.cur')
        self.onimage()
        
    def iutimage(self):
        if self.id1:
            self.after_cancel(self.id1)
            self.id1 = None
        self.label['fg'] = 'grey60'
        if int(self.qx) >= int(self.x):
            self.nx = 0
        else:
            self.nx = 1
            self.can.move(self.q1, self.nx, 0)
            self.can.move(self.q2, -self.nx, 0)
            self.qx += self.nx
        if self.qx < self.x:
            self.id2 = self.after(1, self.iutimage)
        
    def outimage(self, event):
        self.cur.setcursor('media\\cursor\\cursor.cur')
        self.iutimage()

    def onclic(self, event):
        try:
            self.command()
        except:
            pass


class Can(Canvas):

    def __init__(self, master, exception=[], **cnf):
        """A scrollable Canavs with designed scrollbar"""
        self.frame = Frame(master, bd=0, relief='flat', highlightthickness=0)
        Canvas.__init__(self, self.frame, **cnf)
        self.grid(row=1, column=1, sticky='nsew')
        self.can1 = Canvas(self.frame, **cnf)
        self.can2 = Canvas(self.frame, **cnf)
        self.can1['width'] = 10
        self.can2['height'] = 10
        self.can1.grid(row=1, column=2, sticky='ns')
        self.can2.grid(row=2, column=1, sticky='ew')
        self.exception = exception
        
        self.after(1, self.bar)
    
    def bar(self):
        self.yb = BubbleEmpty(self.can1, 5, 25, 'blue',
                              'light blue', height=50)
        self.xb = BubbleEmpty(self.can2, 25, 5, 'blue',
                              'light blue', width=50, height=2)
        self.yb.actbg = 'pink'
        self.xb.actbg = 'pink'
        
        self.posx, self.posy = 25, 25
        self.wdtx, self.hgty = 50, 50
        self.wdt, self.hgt = Get(self).x(), Get(self).y()
        
        Assign(self.can1, self.scrolly, ['Button1-Motion'])
        Assign(self.can2, self.scrollx, ['Button1-Motion'])
    
    def scrolly(self, event=None):
        if 25 <= event.y <= self.hgt - 25:
            self.yb.move(5, event.y)
            a = list(self.find_all())
            b = event.y - self.posy
            for ww in a:
                if ww in self.exception:
                    pass
                else:
                    self.move(ww, 0, -b)
            self.posy = event.y
    
    def scrollx(self, event=None):
        if 25 <= event.x <= self.wdt - 25:
            self.xb.move(event.x, 5)
            a = list(self.find_all())
            b = event.x - self.posx
            for ww in a:
                if ww in self.exception:
                    pass
                else:
                    self.move(ww, -b, 0)
            self.posx = event.x


if __name__ == '__main__':
    fen = Tk()
    can = Can(fen, width=500, height=500, bg='grey', bd=0, highlightthickness=0)
    can.frame.pack()
    for ww in range(15):
        can.create_line(0, ww * 50, 500, ww * 50)
        can.create_line(ww * 50, 0, ww * 50, 500)
    a = can.create_oval(240, 240, 260, 260, fill='red')
    can.exception = [a]
    
    fen.mainloop()
    Cursor()
