#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
:name: Imgmanip
:author: Martin Piták
:version: 1.0
Semestrální práce k předmětu BI-PYT,
jejížm ukolem bylo rozpůlit obrázek v pulce
a schovat do něj další obrázek a textový soubor nebo wav soubor
"""

from PIL import Image
import struct
import sys
import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.constants
import tkinter.filedialog
import tkinter.font

MAGIC_NUMBER = -6
LENGTH = -10


class TkGui(tk.Frame):

    """
    GUI init class
    """

    def __init__(self, root):
        
        """
        Init method

            :param root: Tkinter root file
            :type root: Tk

        """

        tk.Frame.__init__(self, root)

        # options for buttons
        button_opt = {'pady': 0}

        # define Entries
        one = ttk.Entry(self, width=40, style="TEntry")
        one.insert(0, "Select Image To Insert to")
        one.grid(row=0, column=0, pady=10, padx=7)

        many = ttk.Entry(self, width=40, style="TEntry")
        many.insert(0, "Select Files to be inserted")
        many.grid(row=1, column=0, pady=0, padx=7)

        one2 = ttk.Entry(self, width=40, style="TEntry")
        one2.insert(0, "Select Image To Extract from")
        one2.grid(row=4, column=0, pady=0, padx=7)

        # define buttons
        ttk.Button(self, text='SELECT IMAGE', width=20, style="TButton",
                   command=lambda: self.select_filename(one)).grid(row=0, column=1, **button_opt)
        ttk.Button(self, text='SELECT FILES', width=20, style="TButton",
                   command=lambda: self.select_filenames(many)).grid(row=1, column=1, **button_opt)
        ttk.Button(self, text='CREATE', width=20, style="TButton",
                   command=lambda: self.create_file(one.get(), many.get()))\
            .grid(row=2, column=0, columnspan=2, padx=20, pady=10)
        ttk.Button(self, text='SELECT IMAGE', width=20, style="TButton",
                   command=lambda: self.select_filename(one2)).grid(row=4, column=1, **button_opt)
        ttk.Button(self, text='EXTRACT', width=20, style="TButton",
                   command=lambda: self.extract_files(one2.get())).grid(row=5, column=0, columnspan=2, padx=20, pady=10)

        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '.jpg'
        options['filetypes'] = [('img file', '*.jpg'), ('all files', '.*')]
        options['parent'] = root

    def select_filenames(self, entry):

        """
        Opens dialog for choosing multiple files.

            :param entry: Entry class to display/store the result in
        """

        self.file_opt['title'] = "Open file"
        self.file_opt['multiple'] = True

        # get filename
        filenames = tkinter.filedialog.askopenfilename(**self.file_opt)

        if filenames:
            entry.delete(0, len(entry.get())+1)
            entry.insert(0, filenames)

    def select_filename(self, entry):

        """
        Opens dialog for choosing one file.

            :param entry: Entry class to display/store the result in
        """

        self.file_opt['title'] = "Open file"
        self.file_opt['multiple'] = False

        # get filename
        filename = tkinter.filedialog.askopenfilename(**self.file_opt)

        if filename:
            entry.delete(0, len(entry.get())+1)
            entry.insert(0, filename)

    def create_file(self, source, files):

        """
        wrapper for adding files

            :param files: tk string list of files to add
            :param source: img to add items to
        """

        files = list(self.tk.splitlist(files))
        if check_if_files(files + [source]) == "":
            if source and files:
                test = open(source, 'rb+')
                test.seek(MAGIC_NUMBER, 2)
                if test.read(6) == b":31337":
                    test.close()
                    print("Already contains magic number", file=sys.stderr)
                    exit(1)
                test.close()
                try:
                    im = Image.open(source)
                except IOError:
                    print("File {0} is not and valid img".format(source), file=sys.stderr)
                    exit(1)
                new = cut_img(im)
                source = "{0}.secret.jpg".format(source)
                new.save(source)
                add_files(source, files)

    @staticmethod
    def extract_files(source):

        """
        wrapper for removing files

            :param source: img to remove files from
        """

        if check_if_files([source]) == "":
            remove_files(source)


def check_if_files(args, mode="RW"):

    """
    Return string of files that are not files.
    Cant read, write or access them.

        :param mode: string with perms to check W|R|WR
        :param args: files to check
        :returns: string of bad files separated by space
    """
    read = write = True
    broken = ""
    for file in args:
        for perm in mode:
            if perm == "R":
                if not os.path.exists(file) and not os.access(file, os.R_OK):
                    read = False
            if perm == "W":
                if not os.path.exists(file) and not os.access(file, os.W_OK):
                    write = False
        if not read or not write:
            if broken == "":
                broken += file
            else:
                broken += " " + file

    return broken


def usage():

    """
    Prints usage to stderr
    """

    print("IMGMANIP\n"
          "Simple tool that's cuts stereoscopic img in half\n"
          "and \"hides\" additional files in it.\n"
          "\n"
          "Usage: imgmanip source file...\n"
          "           Creates new file source.secret.jpg\n"
          "           where source is the file that is cut in half\n"
          "           and files are hidden files in it\n"
          "       imgmanip source\n"
          "           Extracts data from source\n"
          "       imgmanip -g\n"
          "           launches imgmanip in gui form\n", file=sys.stderr)


def cut_img(img):

    """
    Splits image in half.

        :param img: img to cut
        :returns: cropped img
    """

    box = (0, 0, img.width // 2, img.height)
    cropped = img.crop(box)
    return cropped


def add_files(img, files):

    """
    Appends files to image

        :format: :hidden:FILES:(NAMELENGTH:NAME:FILELENGTH:FILECONTENT:)...:STARTPOSS:31337
        :param img: source img to hide the data in
        :param files: list of filenames to hide in img
    """

    to = open(img, "ab+")
    ending = to.tell()
    to.seek(0, 2)
    to.write(b":hidden:")
    to.write(struct.pack("!l", len(files)))
    to.write(b":")
    for file in files:
        fh = open(file, "rb")
        fh.seek(0, 2)
        size = fh.tell()
        fh.seek(0)
        to.write(struct.pack("!l", len(bytes(os.path.basename(file).encode("utf-8")))))
        to.write(b":" + bytes(os.path.basename(file).encode("utf-8")) + b":")
        to.write(struct.pack("!l", size) + b":")
        to.write(fh.read())
        fh.close()
        to.write(b":")
    to.write(struct.pack("!l", ending))
    to.write(b":31337")
    to.close()


def remove_files(img):

    """
    Gets files from img.

        :param img: source img to the get files from
    """

    source = open(img, "rb+")
    source.seek(MAGIC_NUMBER, 2)
    if source.read(6) != b":31337":
        source.close()
        print("Does not contain magic number", file=sys.stderr)
        exit(1)
    source.seek(LENGTH, 2)
    start = struct.unpack("!l", source.read(4))[0]
    source.seek(start, 0)
    if source.read(8) != b":hidden:":
        source.close()
        print("Not file created by this app", file=sys.stderr)
        exit(1)
    files = struct.unpack("!l", source.read(4))[0]
    for i in range(files):
        source.read(1)
        namelenght = struct.unpack("!l", source.read(4))[0]
        source.read(1)
        name = source.read(namelenght).decode("utf-8")
        source.read(1)
        filelenght = struct.unpack("!l", source.read(4))[0]
        source.read(1)
        file = source.read(filelenght)
        tmp = open(os.path.dirname(os.path.abspath(img)) + "/" + name, "wb+")
        tmp.write(file)
        tmp.close()

    # delete the added stuff
    source.truncate(start)


def main_func(mode):

    """
    Main function of the program.
    Based on mode decides what to do

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
        test = open(source, 'rb+')
        test.seek(MAGIC_NUMBER, 2)
        if test.read(6) == b":31337":
            test.close()
            print("Already contains magic number", file=sys.stderr)
            exit(1)
        test.close()
        new = cut_img(im)
        source = "{0}.secret.jpg".format(os.path.basename(source))
        new.save(source)
        add_files(source, files)
    elif mode == "d":
        remove_files(source)
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
            notfiles = check_if_files(sys.argv[1:])
            if notfiles != "":
                print("Files {0} are not accessible files!".format(notfiles), file=sys.stderr)
                exit(1)
            else:
                sys.argv.pop(0)
                main_func('d')
    else:
        notfiles = check_if_files(sys.argv[1:])
        if notfiles != "":
            print("Files {0} are not accessible files!".format(notfiles), file=sys.stderr)
            exit(1)
        if not os.access(os.getcwd(), os.W_OK):
            print("Directory {0} not writable!".format(os.getcwd()), file=sys.stderr)
            exit(1)
        sys.argv.pop(0)
        main_func('c')
