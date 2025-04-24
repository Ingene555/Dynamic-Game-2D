from pyfunct import  Assign, Cursor
from tkinter.font import Font
from tkinter import Frame, Canvas, Label, Message as Msg
from PIL import Image, ImageTk

print('calling <SquareImage>...')


# class of squareImage
class SquareImage(Frame):

    def __init__(self, master, image, command=None, **kw):
        '''Image button'''  # button that contain image
        Frame.__init__(self, master, kw)  # the widget is based on a Frame widget
        self.config(bg='black', bd=0, highlightthickness=0, relief='flat')
        self.master = master
        self.command = command
        
        self.po = Image.open(image)  # load the image and create interface width Canvas, Label and Message
        self.photo = ImageTk.PhotoImage(self.po)
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
                    relief='flat', font=Font(family='helvetica', size=15, weight='bold'))
        
        self.text = Msg(self, bg='black', bd=0, highlightthickness=0, anchor='w', fg='grey50',
                    width=190, relief='flat', font=Font(family='helvetica', size=7))

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
