#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Semestrální práce k předmětu BI-PYT,
jejížm ukolem bylo rozpůlit obrázek v pulce
a schovat do něj další obrázek a textový soubor nebo wav soubor"""

import PIL
import tkinter
import tkinter.constants
import tkinter.filedialog
import tkinter.font


class TkGui(tkinter.Frame):
    """"GUI init class"""

    def __init__(self, root):
        """"Init method

            :param root: Tkinter root file
            :type root: Tk

        """

        tkinter.Frame.__init__(self, root)

        # options for buttons
        button_opt = {'padx': 0, 'pady': 0,}

        # define buttons
        tkinter.Button(self, text='OPEN', width=7, bg="black", fg="white", font="Serif", command=self.openbasefilename).grid(row=0, **button_opt)
        tkinter.Button(self, text='CREATE', width=7, bg="black", fg="white", font="Serif", command=self.createfile).grid(row=1, **button_opt)

        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '.jpg'
        options['filetypes'] = [('img file', '*.jpg'), ('all files', '.*')]
        options['parent'] = root

    def openbasefilename(self):

        """Returns an opened file in read mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """

        self.file_opt['title'] = "Open file"
        # get filename
        filename = tkinter.filedialog.askopenfilename(**self.file_opt)

        # open file on your own
        if filename:
            print(filename)

    def createfile(self):

        """Returns an opened file in write mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """

        # get filename
        self.file_opt['title'] = "Save file as"
        self.file_opt['filetypes'] = [('img file', '*.jpg'), ('all files', '.*')]
        filename = tkinter.filedialog.asksaveasfilename(**self.file_opt)

        # open file on your own
        if filename:
            print(filename)


if __name__ == '__main__':
    root = tkinter.Tk()
    root.title("IMGMANIP")
    root.geometry("400x200")
    root.configure(background='#4B4E4F', )
    TkGui(root).grid()
    root.mainloop()
