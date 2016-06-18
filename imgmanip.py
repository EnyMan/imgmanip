#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Semestrální práce k předmětu BI-PYT,
jejížm ukolem bylo rozpůlit obrázek v pulce
a schovat do něj další obrázek a textový soubor nebo wav soubor"""

import PIL
import sys
import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.constants
import tkinter.filedialog
import tkinter.font


class TkGui(tk.Frame):
    """"GUI init class"""

    def __init__(self, root):
        """"Init method

            :param root: Tkinter root file
            :type root: Tk

        """

        tk.Frame.__init__(self, root)

        # options for buttons
        button_opt = {'pady': 0}

        # define buttons
        ttk.Button(self, text='OPEN', width=7, style="TButton", command=self.openbasefilename).grid(row=3, column=1,
                                                                                                    **button_opt)
        ttk.Button(self, text='CREATE', width=7, style="TButton", command=self.createfile).grid(row=3, column=3,
                                                                                                padx=20, **button_opt)

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


def checkiffiles(args):
    """Return string of files that are not files.
        Cant read, write or access them.

            :param args: files to check
            :returns: string of bad files separated by space
        """
    broken = ""
    for file in args:
        if not os.path.exists(file) and not os.access(file, os.R_OK):
            if broken == "":
                broken += file
            else:
                broken += " " + file

    return broken


def usage():
    print("IMGMANIP\n"
          "simple tool that's cuts stereoscopic img in half and \"hides\" additional files in it\n"
          "\n"
          "Usage: imgmanip source file...\n"
          "           creates new file source.secret where source is the file that is cut in half\n"
          "           and files are hidden files in it\n"
          "       imgmanip -g\n"
          "           launches imgmanip in gui form\n", file=sys.stderr)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Not enough argument!", file=sys.stderr)
        usage()
        exit(1)
    elif len(sys.argv) == 2 and sys.argv[1] == "-g":
        base = tk.Tk()
        base.title("IMGMANIP")
        base.geometry("400x200")
        TkGui(base).grid()
        base.mainloop()
    else:
        notfiles = checkiffiles(sys.argv[1:])
        if notfiles != "":
            print("Files {0} are not accessible files!".format(notfiles), file=sys.stderr)
            exit(1)
