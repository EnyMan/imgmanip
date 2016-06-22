#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Semestrální práce k předmětu BI-PYT,
jejížm ukolem bylo rozpůlit obrázek v pulce
a schovat do něj další obrázek a textový soubor nebo wav soubor"""

from PIL import Image
import ntpath
import struct
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

MAGIC_NUMBER = -6
LENGTH = -10


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
    """Prints usage to stderr"""

    print("IMGMANIP\n"
          "Simple tool that's cuts stereoscopic img in half and \"hides\" additional files in it.\n"
          "\n"
          "Usage: imgmanip source file...\n"
          "           creates new file source.secret.jpg where source is the file that is cut in half\n"
          "           and files are hidden files in it\n"
          "       imgmanip -g\n"
          "           launches imgmanip in gui form\n", file=sys.stderr)


def cutimg(img):
    box = (0, 0, img.width/2, img.height)
    cropped = img.crop(box)
    return cropped


# :hidden:FILES:NAMELENGTH:NAME:FILELENGTH:FILECONTENT:...:STARTPOSS:31337
def addfiles(img, files):
    to = open(img, "ab+")
    ending = to.tell()
    to.write(b":hidden:")
    to.write(struct.pack("l", len(files)))
    to.write(b":")
    for file in files:
        fh = open(file, "rb")
        fh.seek(0, 2)
        size = fh.tell()
        fh.seek(0)
        to.write(struct.pack("l", len(ntpath.basename(file))))
        to.write(b":" + bytes(ntpath.basename(file).encode()) + b":")
        to.write(struct.pack("l", size) + b":")
        to.write(fh.read())
        fh.close()
        to.write(b":")
    to.write(struct.pack("l", ending))
    to.write(b":31337")
    to.close()


# :hidden:FILES:NAMELENGTH:NAME:FILELENGTH:FILECONTENT:...:STARTPOSS:31337
def removefiles(img):
    source = open(img, "rb+")
    source.seek(MAGIC_NUMBER, 2)
    if source.read(6) != b":31337":
        print("some error", file=sys.stderr)
        exit(1)
    source.seek(LENGTH, 2)
    start = struct.unpack("l", source.read(4))[0]
    source.seek(start, 0)
    if source.read(8) != b":hidden:":
        print("some error", file=sys.stderr)
        exit(1)
    files = struct.unpack("l", source.read(4))[0]
    for i in range(files):
        a = source.read(1)
        namelenght = struct.unpack("l", source.read(4))[0]
        a = source.read(1)
        name = source.read(namelenght)
        a = source.read(1)
        filelenght = struct.unpack("l", source.read(4))[0]
        a = source.read(1)
        file = source.read(filelenght)
        tmp = open(name, "wb+")
        tmp.write(file)
        tmp.close()

    # delete the added stuff
    source.truncate(start)


def mainfunc(mode):
    """"
    Main function of the program

        :param mode: chooses if hide 'c' or unhide 'd'
        :type mode: string
    """

    source = sys.argv.pop(0)
    files = sys.argv

    try:
        im = Image.open(source)
    except IOError:
        print("File {0} is not and valid img".format(source), file=sys.stderr)
        exit(1)
    if mode == "c":
        new = cutimg(im)
        new.save("{0}.secret.jpg".format(ntpath.basename(source)))
        addfiles(source, files)
    elif mode == "d":
        removefiles(source)
    else:
        raise SystemError("{0} is not valid mode.".format(mode))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Not enough argument!", file=sys.stderr)
        usage()
        exit(1)
    elif len(sys.argv) == 2:
        if sys.argv[1] == "-g":
            base = tk.Tk()
            base.title("IMGMANIP")
            base.geometry("400x200")
            TkGui(base).grid()
            base.mainloop()
        elif sys.argv[1].find("-") != -1:
            print("Unknown argument! {0}".format(sys.argv[1]), file=sys.stderr)
            usage()
            exit(1)
        else:
            notfiles = checkiffiles(sys.argv[1:])
            if notfiles != "":
                print("Files {0} are not accessible files!".format(notfiles), file=sys.stderr)
                exit(1)
            else:
                sys.argv.pop(0)
                mainfunc('d')
    else:
        notfiles = checkiffiles(sys.argv[1:])
        if notfiles != "":
            print("Files {0} are not accessible files!".format(notfiles), file=sys.stderr)
            exit(1)
        if not os.access(os.getcwd(), os.W_OK):
            print("Directory {0} not writable!".format(os.getcwd()), file=sys.stderr)
            exit(1)
        sys.argv.pop(0)
        mainfunc('c')
