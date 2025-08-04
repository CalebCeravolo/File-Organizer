# Application to sort through apps. Can delete, or move each file. Has a file previewer which can display
# text from a pdf, any plain text document, or images that PIL can read

import tkinter as tk
from tkinter.constants import *
import os.path
from tkinter.scrolledtext import ScrolledText
from tkinter import *
from tkinter import ttk
from PIL import (Image as Img, ImageTk)
import PyPDF2
from shutil import move
from organize import sorter
_location = os.path.expanduser("~")
test = _location[:3]
if ("\\" in test): delim = "\\"
else: delim = "/"
# ind = _location.find(delim)
# ind = _location.find(delim, ind+1)
# ind = _location.find(delim, ind+1)
starting_dir = _location
from numpy import linspace
import Organize_support
from tkinter.messagebox import askyesnocancel
import shutil
class OpenPage:
    def save_and_proceed(self, *args):
        source = self.source.get()
        dest = self.dest.get()
        trash = self.trash.get()
        if (len(source)>0): self.org.change_source(source)
        if (len(dest)>0):   self.org.change_dest(dest)
        if (len(trash)>0):  self.org.change_trash(trash)
        self.org.update()
        self.other.preview()
        self.top.destroy()
        
    def __init__(self, org, other, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        self.other = other
        self.source = ""
        self.dest = ""
        top.geometry("665x451+427+197")
        top.minsize(120, 1)
        top.maxsize(1444, 881)
        top.resizable(1,  1)
        top.title("Set Directories")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="#000000")
        self.org = org
        self.top = top
        self.source = tk.StringVar()
        self.dest = tk.StringVar()
        self.trash = StringVar()
        ypos = linspace(.3,.5,3)
        self.TLabel2 = ttk.Label(self.top)
        self.TLabel2.place(relx=0.340, rely=ypos[1], height=20, width=93, anchor = 'e')
        self.TLabel2.configure(font="-family {Segoe UI} -size 9")
        self.TLabel2.configure(relief="flat")
        self.TLabel2.configure(justify='left')
        self.TLabel2.configure(text='''Target Directory''')
        self.TLabel2.configure(compound='left')
        self.TLabel2.configure(background = "#d9d9d9")

        self.TEntry1 = ttk.Entry(self.top)
        self.TEntry1.place(relx=0.346, rely=ypos[1], relheight=0.042
                , relwidth=0.247, anchor = 'w')
        self.TEntry1.configure(font="-family {Courier New} -size 10")
        self.TEntry1.configure(textvariable=self.dest)
        self.TEntry1.configure(cursor="ibeam")

        
        self.TLabel1 = ttk.Label(self.top)
        self.TLabel1.place(relx=0.340, rely=ypos[0], height=20, width=93, anchor = 'e')
        self.TLabel1.configure(font="-family {Segoe UI} -size 9")
        self.TLabel1.configure(relief="flat")
        self.TLabel1.configure(justify='left')
        self.TLabel1.configure(text='''Source Directory''')
        self.TLabel1.configure(compound='left')
        self.TLabel1.configure(background = "#d9d9d9")

        self.Entry1 = ttk.Entry(self.top)
        self.Entry1.place(relx=0.346, rely=ypos[0], height=20, relwidth=0.247, anchor = 'w')
        self.Entry1.configure(font="-family {Courier New} -size 10")
        self.Entry1.configure(textvariable=self.source)
        self.Entry1.configure(cursor = "ibeam")

        self.T = ttk.Label(self.top)
        self.T.place(relx=0.340, rely=ypos[2], height=20, width=93, anchor = 'e')
        self.T.configure(font="-family {Segoe UI} -size 9")
        self.T.configure(relief="flat")
        self.T.configure(justify='left')
        self.T.configure(text='''Trash Directory''')
        self.T.configure(compound='left')
        self.T.configure(background = "#d9d9d9")

        self.Entry1 = ttk.Entry(self.top)
        self.Entry1.place(relx=0.346, rely=ypos[2], height=20, relwidth=0.247, anchor = 'w')
        self.Entry1.configure(font="-family {Courier New} -size 10")
        self.Entry1.configure(textvariable=self.trash)
        self.Entry1.configure(cursor = "ibeam")

        # self.TLabel1 = ttk.Label(self.top)
        # self.TLabel1.place(relx=0.340, rely=0.3, height=20, width=93, anchor = 'e')
        # self.TLabel1.configure(font="-family {Segoe UI} -size 9")
        # self.TLabel1.configure(relief="flat")
        # self.TLabel1.configure(justify='left')
        # self.TLabel1.configure(text='''Trash''')
        # self.TLabel1.configure(compound='left')
        # self.TLabel1.configure(background = "#d9d9d9")

        self.Entry1 = ttk.Entry(self.top)
        self.Entry1.place(relx=0.346, rely=ypos[0], height=20, relwidth=0.247, anchor = 'w')
        self.Entry1.configure(font="-family {Courier New} -size 10")
        self.Entry1.configure(textvariable=self.source)
        self.Entry1.configure(cursor = "ibeam")

        self.Confirm = tk.Button(self.top)
        self.Confirm.place(relx=0.4, rely=0.554, height=20, width=93)
        self.Confirm.configure(activebackground="#d9d9d9")
        self.Confirm.configure(activeforeground="black")
        self.Confirm.configure(background="#d9d9d9")
        self.Confirm.configure(command=self.save_and_proceed)
        self.Confirm.configure(disabledforeground="#a3a3a3")
        self.Confirm.configure(font="-family {Segoe UI} -size 9")
        self.Confirm.configure(foreground="#000000")
        self.Confirm.configure(highlightbackground="#d9d9d9")
        self.Confirm.configure(highlightcolor="#000000")
        self.Confirm.configure(text='''Confirm''')

class Toplevel1:
    def search(self, *args):
        pattern = self.entry.get()
        matches = self.org.search(pattern, self.recurse_content.get())
        top1 = Toplevel(self.top)
        Regex_window(matches, "Results", self, top1)
    def openf(self, *args):
        self.org.open()
        self.preview()
    def update(self, *args):
        self.org.update()
        self.preview()
    def moveto(self, *args):
        self.org.moveto(self.entry.get())
        # self.org.run(f"moveto {self.entry.get()}")
        self.preview()
    def regex(self, *args):
        pattern = self.entry.get()
        matches = self.org.regex(pattern, self.recurse_regex.get())
        top1 = tk.Toplevel(self.top)
        new= Regex_window(matches, "Matches", self,top1)
        self.updates.append(new)
    def newfolder(self, *args):
        self.org.newfolder(self.entry.get())
        # self.org.run(f"newfolder {self.entry.get()}")
        self.preview()
    def back(self, *args):
        self.org.back()
        self.preview()
    def delete(self, *args):
        self.org.delete()
        # self.org.run(f"remove")
        self.preview()
    def next(self, *args):
        self.org.next()
        self.preview()
    def preview(self, *args):
        self.org.update()
        file_name = self.org.full_path()
        self.Surrounding.set(self.org.surrounding_files(self.vars["Number of surrounding files show"]))
        self.currentD.set(self.org.pathto)
        self.currentS.set(self.org.path)
        self.trash_label.config(text = f"Trash location: {self.org.trash}")
        self.File.set(self.org.getCurrent())
        self.Preview.delete(1.0, tk.END)
        self.PictureFrame.image = 0
        self.PictureFrame.place_forget()
        for object in self.updates:
            if (object.top.winfo_exists()):
                object.update()
            else: self.updates.remove(object)
        if (os.path.isdir(file_name)):
            for i, file in enumerate(self.org.get_children()):
                self.Preview.insert(i+.0, f"{file}\n")
                if (i==self.vars["Number of subfiles shown (for directories)"]):
                    break
        else:
            try:
                with open(file_name, "r") as f:
                    content = f.read()
                    if (self.vars["Number of characters shown (plain text)"]==-1):
                        self.Preview.insert(0.0, content)
                    else:
                        self.Preview.insert(0.0, content[0:self.vars["Number of characters shown (plain text)"]])
            except:
                try:
                    image = Img.open(self.org.full_path())
                    width  = int(self.top.winfo_width()*(.557))
                    height  = int(self.top.winfo_height()*(.949))
                    ratio = height/image.size[1]
                    if (ratio*image.size[0]>width):
                        ratio = width/image.size[0]
                        image = image.resize((width, int(ratio*image.size[1])))
                    else:
                        image = image.resize((int(image.size[0]*ratio), height))
                    img = ImageTk.PhotoImage(image)
                    self.PictureFrame.config(image=img)
                    self.PictureFrame.image = img
                    self.PictureFrame.place(relx=0.425, rely=0.015, anchor = "nw")
                except: 
                    if (".pdf" in file_name):
                        with open(self.org.full_path(), "rb") as f:
                            reader = PyPDF2.PdfReader(f)
                            for i in range(min(self.vars["Number of pages shown (pdf)"], len(reader.pages))):
                                self.Preview.insert(i+0.0, reader.pages[i].extract_text())
    def openOther(self, *args):
        _top1 = tk.Toplevel(self.top)
        self.OtherPage = OpenPage(self.org, self, _top1)
    def open_settings(self, *args):
        top1 = tk.Toplevel(self.top)
        self.Settings = Settings_window(self.vars, self,top=top1)
    def move_into_current(self, *args):
        self.org.move_into()
        self.preview()
    def move_back(self, *args):
        self.org.move_back()
        self.preview()
    def open_preview(self, *args):
        top1 = tk.Toplevel(self.top)
        other_preview = Extra_preview(self.Surrounding,"Neighboring files", 'none',top1)
        self.updates.append(other_preview)
    def help_message(self, *args):
        top1 = tk.Toplevel(self.top)
        Extra_preview(self.helpMessage, "Help", "word",top1)
    def overwrite(self, *args):
        content = self.Preview.get(0.0, tk.END)
        self.org.save_current(content)
    def new_file(self, *args):
        name = self.entry.get()
        self.org.new_file(name)
        self.preview()
    def find(self, *args):
        pattern = self.entry.get()
        self.org.find(pattern, self.recurse_find.get())
        self.preview()
    def on_closing(self, *args):
        ans = askyesnocancel("Quit", "Would you like to delete your trash folder?")
        if (ans):
            shutil.rmtree(self.org.trash)
            self.top.destroy()
        elif (ans==False):
            self.top.destroy()
    def open_trash(self, *args):
        os.startfile(self.org.trash)
    def __init__(self, org, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        top.protocol("WM_DELETE_WINDOW", self.on_closing)
        top.geometry("1178x589+104+110")
        top.minsize(120, 1)
        top.maxsize(1444, 881)
        top.resizable(1,  1)
        top.title("Main")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="#000000")
        show_num_pages = 5
        show_num_characters = -1
        show_num_files = 20
        show_num_surrounding_files = 20
        self.vars = {"Number of pages shown (pdf)" : show_num_pages, 
                     "Number of characters shown (plain text)" : show_num_characters,
                     "Number of subfiles shown (for directories)" : show_num_files,
                     "Number of surrounding files show" : show_num_surrounding_files}
        self.top = top
        self.updates = []
        self.File = tk.StringVar()
        self.org = org
        self.Surrounding = StringVar()
        self.Regex_answers = StringVar()
        self.entry = tk.StringVar()
        self.currentS=tk.StringVar()
        self.currentD = tk.StringVar()
        self.recurse_find = tk.BooleanVar()
        self.recurse_regex = tk.BooleanVar()
        self.recurse_content = tk.BooleanVar()

        Label(self.top, text = "Recursive Find", background="#d9d9d9").place(relx=.01, rely=.3)
        Label(self.top, text = "Recursive Regex", background="#d9d9d9").place(relx=.01, rely=.34)
        Label(self.top, text = "Recursive Content", background = "#d9d9d9").place(relx=.01, rely=.38)
        self.RF_option = Checkbutton(self.top, variable = self.recurse_find, background="#d9d9d9")
        self.RF_option.place(relx=.10, rely=.3)
        
        self.RR_option = Checkbutton(self.top, variable = self.recurse_regex, background="#d9d9d9")
        self.RR_option.place(relx=.10, rely=.34)

        self.RC_option = Checkbutton(self.top, variable = self.recurse_content, background="#d9d9d9")
        self.RC_option.place(relx = .1, rely = .38)

        self.menubar = Menu(self.top)
        self.top.config(menu = self.menubar)
        self.File_menu = Menu(self.menubar, tearoff=False)
        self.File_menu.add_command(label='Settings',command=self.open_settings)
        self.Additional_options = Menu(self.menubar, tearoff = False)
        self.Additional_options.add_command(label="New Folder",command=self.newfolder)
        self.Additional_options.add_command(label="Open",command=self.openf)
        self.Additional_options.add_command(label="Save File Contents", command=self.overwrite)
        self.Additional_options.add_command(label="New File", command = self.new_file)
        self.Additional_options.add_command(label="Find", command = self.find)
        self.Additional_options.add_command(label="Open Trash", command = self.open_trash)
        self.Additional_options.add_command(label="Search Contents", command = self.search)
        self.menubar.add_cascade(label="Menu",menu=self.File_menu)
        self.menubar.add_cascade(label="Additional Options", menu = self.Additional_options)
        self.menubar.add_command(label = "Help", command=self.help_message)

        
        self.RegexB = tk.Button(self.top, activebackground="#d9d9d9", background="#d9d9d9")
        self.RegexB.configure(text='''Regex''')
        self.RegexB.configure(command = self.regex)

        self.Delete = tk.Button(self.top)
        self.Delete.configure(activebackground="#d9d9d9")
        self.Delete.configure(activeforeground="black")
        self.Delete.configure(background="#d9d9d9")
        self.Delete.configure(disabledforeground="#a3a3a3")
        self.Delete.configure(text='''Delete''')
        self.Delete.configure(command = self.delete)

        

        self.Moveto = tk.Button(self.top, activebackground="#d9d9d9", background="#d9d9d9")
        self.Moveto.configure(text='''Move to''')
        self.Moveto.configure(command = self.moveto)
        
        
        self.Next = tk.Button(self.top, activebackground="#d9d9d9", background="#d9d9d9")
        self.Next.configure(text='''Next''')
        self.Next.configure(command = self.next)

        self.Back = tk.Button(self.top, activebackground="#d9d9d9", background="#d9d9d9")
        self.Back.configure(text='''Back''')
        self.Back.configure(command = self.back)

        self.Enter = Button(self.top, activebackground="#d9d9d9", background="#d9d9d9")
        self.Enter.configure(command = self.move_into_current, text = "Move into current")

        self.Move_back = Button(self.top, activebackground="#d9d9d9", background="#d9d9d9")
        self.Move_back.configure(command = self.move_back, text = "Move into previous")
        

        self.ChangeDir = Button(self.top, activebackground="#d9d9d9", background="#d9d9d9")
        self.ChangeDir.configure(command = self.openOther, text = "Set Directories")

        self.Extra_preview = Button(self.top)
        self.Extra_preview.configure(command = self.open_preview, text = "View Surrounding Files")
        self.Extra_preview.configure(background="#d9d9d9")
        self.Extra_preview.configure(foreground="#000000")
        self.Extra_preview.configure(activebackground = "#d9d9d9")

       

        positions = linspace(.03, .35, 5)
        positions2 = linspace(.01, .29, 3)
        width = 67
        p1height = .64
        self.Next.place(relx=positions[1], rely=p1height, height=26, width=width)
        #self.Open.place(relx=positions[5], rely=0.537, height=26, width=width)
        self.Delete.place(relx=positions[3], rely=p1height, height=26, width=width)
        self.RegexB.place(relx=positions[4], rely=p1height, height=26, width=width)
        self.Moveto.place(relx=positions[2], rely=p1height, height=26, width=width)
        self.Back.place(relx=positions[0], rely=p1height, height=26, width=width)

        p2height = .56
        self.ChangeDir.place(relx = positions2[0], rely=p2height, width = width*2)
        self.Enter.place(relx = positions2[1], rely = p2height, height = 26, width=width*2)
        self.Move_back.place(relx = positions2[2], rely = p2height, height = 26, width=width*2)
        self.Extra_preview.place(relx = .420, rely = .01, anchor = 'ne', height = 26, width = width*2.5)
        self.helpMessage = r"""Welcome! 
This is a file organizer app. This help box gives info into how to use the buttons on the main screen. The regex window has further information into how to use regex.
You can use this organizer as a text editor by editing the preview box and selecting Save File Content from the Additional Options dropdown menu
___________________
The organizer defaults to operate within whatever directory this app was launched from, go to change directories to change this. Change Directories can take an absolute or relative path. Relative paths are relative to Target Directory
___________________
Some options take arguments from the command line input. Type into the command line and then select the desired option
___________________
Options that aren't buttons are in the Additonal Options pop down menu located next to the help button

Options:
___________________
Find:
Using Regex search, sets current file to the first match. For example, F.* locates the first file that starts with an F. Click on Help in regex for more regex info
___________________
Change Directories: 
Opens Change directories window. Used to change source or target directory. Takes relative or absolute path
___________________
Move into current/previous: 
Sets source directory into the current viewed directory or to one less than current source path
___________________
Move To [dest]: 
Moves file to destination directory typed in command line
___________________
New Folder [name]: 
Creates new folder in directory specified in the command line input and moves current file into it
___________________
New File [name]:
Creates new file in current directory with name in the command line. Can have any file extension
___________________
Save File Contents:
Saves the content of the preview box to the current file
___________________
Delete: 
Moves current file to Trash folder
___________________
Regex: 
Returns the files found by a regex search through the current source directory. These files pop up in a preview window which can then be viewed in detail. Takes in a regex pattern from the command line. Check out the regex popup window help menu for more info
"""
        # self.Text2 = tk.Text(self.top)
        # self.Text2.place(relx=0.013, rely=0.67, relheight=0.30, relwidth=0.357)
        # self.Text2.configure(background="#d9d9d9")
        # self.Text2.configure(font="TkTextFont")
        # self.Text2.configure(foreground="black")
        # self.Text2.configure(highlightbackground="#43f0fe")
        # self.Text2.configure(highlightcolor="#000000")
        # self.Text2.configure(insertbackground="#000000")
        # self.Text2.configure(selectbackground="#d9d9d9")
        # self.Text2.configure(selectforeground="black")
        # self.Text2.configure(wrap="word")
        # self.Text2.insert(1.0, helpMessage)

        self.Preview = ScrolledText(self.top)
        self.Preview.place(relx=0.425, rely=0.015, relheight=0.949
                , relwidth=0.558)
        self.Preview.configure(background="white", insertofftime = 800, insertontime = 700)
        self.Preview.configure(font="TkTextFont")
        self.Preview.configure(foreground="black")
        self.Preview.configure(highlightbackground="#d9d9d9")
        self.Preview.configure(highlightcolor="#000000")
        self.Preview.configure(insertbackground="#000000")
        self.Preview.configure(insertborderwidth="3")
        self.Preview.configure(selectbackground="#d9d9d9")
        self.Preview.configure(selectforeground="black")
        self.Preview.configure(wrap="word")

        self.PictureFrame = tk.Label(self.top)
        self.PictureFrame.place(relx=0.425, rely=0.015, height=23, width=81, anchor = "nw")
        self.PictureFrame.configure(activebackground="#d9d9d9")
        self.PictureFrame.configure(activeforeground="black")
        
        self.currentSource = tk.Label(self.top)
        self.currentSource.configure(background="#d9d9d9", text = "Current Source Directory:")
        self.labelSource = tk.Label(self.top)
        self.labelSource.configure(background="#d9d9d9", textvariable = self.currentS)

        self.currentDest = tk.Label(self.top)
        self.currentDest.configure(background="#d9d9d9", text = "Current Target Directory:")
        self.labelDest = tk.Label(self.top)
        self.labelDest.configure(background="#d9d9d9", textvariable = self.currentD)
        
        self.trash_label = tk.Label(self.top, text = f"Trash location: {org.trash}", background = "#d9d9d9")
    

        xpos_labels = .01
        ystart_labels = .15
        self.currentSource.place(relx = xpos_labels, rely = ystart_labels, anchor = "w")
        self.currentDest.place(relx = xpos_labels, rely = ystart_labels+.03, anchor = "w")
        self.labelSource.place(relx = xpos_labels+.12, rely = ystart_labels, anchor = "w")
        self.labelDest.place(relx = xpos_labels+.12, rely = ystart_labels+.03, anchor = "w")
        self.trash_label.place(relx=xpos_labels, rely = ystart_labels+.06, anchor = "w")
        
        self.TLabel3 = ttk.Label(self.top)
        self.TLabel3.place(relx=0.007, rely=0.071, height=20, width=29)
        self.TLabel3.configure(font="TkDefaultFont")
        self.TLabel3.configure(relief="flat")
        self.TLabel3.configure(anchor='w')
        self.TLabel3.configure(justify='left')
        self.TLabel3.configure(text='''File:''')
        self.TLabel3.configure(compound='left')
        self.TLabel3.configure(background = "#d9d9d9")

        self.TEntry2 = ttk.Entry(self.top)
        self.TEntry2.place(relx=0.076, rely=p1height+.1, height = 24
                , relwidth=0.25, anchor = "nw")
        self.TEntry2.configure(takefocus="")
        self.TEntry2.configure(cursor="ibeam")
        self.TEntry2.configure(textvariable = self.entry)

        self.TLabel4 = ttk.Label(self.top)
        self.TLabel4.place(relx=0.028, rely=0.071, height=20, relwidth = .38)
        self.TLabel4.configure(font="-family {Segoe UI} -size 9")
        self.TLabel4.configure(relief="flat")
        self.TLabel4.configure(anchor='w')
        self.TLabel4.configure(justify='left')
        self.TLabel4.configure(textvariable=self.File)
        self.TLabel4.configure(compound='left')
        self.TLabel4.configure(cursor="fleur")
        self.TLabel4.configure(background = "#d9d9d9")
        self.File.set(self.org.getCurrent())
        self.preview()
class Toplevel2(Toplevel1):
    def regex(self, *args):
        pattern = self.entry.get()
        matches = self.org.regex(pattern, False) #Regex search no recursion
        self.org.files=matches
        self.org.update()
        self.preview()
    # def search(self, *args):
    #     pattern = self.entry.get()
    #     matches = self.org.search(pattern)
    #     top1 = Toplevel(self.top)
    #     Regex_window(matches, "Results", self, top1)
    def __init__(self, org, top=None):
        # top.protocol("WM_DELETE_WINDOW", self.on_closing)
        top.geometry("1100x500+104+110")
        top.minsize(120, 1)
        top.maxsize(1444, 881)
        top.resizable(1,  1)
        top.title("Detailed Preview")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="#000000")
        show_num_pages = 5
        show_num_characters = -1
        show_num_files = 20
        show_num_surrounding_files = 20
        self.vars = {"Number of pages shown (pdf)" : show_num_pages, 
                     "Number of characters shown (plain text)" : show_num_characters,
                     "Number of subfiles shown (for directories)" : show_num_files,
                     "Number of surrounding files show" : show_num_surrounding_files}
        self.top = top
        self.updates = []
        self.File = tk.StringVar()
        self.org = org
        self.Surrounding = StringVar()
        self.Regex_answers = StringVar()
        self.entry = tk.StringVar()
        self.currentS=tk.StringVar()
        self.currentD = tk.StringVar()
        
        
        self.menubar = Menu(self.top)
        self.top.config(menu = self.menubar)
        self.File_menu = Menu(self.menubar, tearoff=False)
        self.File_menu.add_command(label='Settings',command=self.open_settings)
        self.Additional_options = Menu(self.menubar, tearoff = False)
        self.Additional_options.add_command(label="New Folder",command=self.newfolder)
        self.Additional_options.add_command(label="Open",command=self.openf)
        self.Additional_options.add_command(label="Save File Contents", command=self.overwrite)
        self.Additional_options.add_command(label="New File", command = self.new_file)
        self.Additional_options.add_command(label="Find", command = self.find)
        self.Additional_options.add_command(label="Open Trash", command = self.open_trash)
        self.Additional_options.add_command(label="Search Content", command = self.search)
        self.menubar.add_cascade(label="Menu",menu=self.File_menu)
        self.menubar.add_cascade(label="Additional Options", menu = self.Additional_options)
        self.menubar.add_command(label = "Help", command=self.help_message)

        
        self.RegexB = tk.Button(self.top, activebackground="#d9d9d9", background="#d9d9d9")
        self.RegexB.configure(text='''Regex''')
        self.RegexB.configure(command = self.regex)

        self.Delete = tk.Button(self.top)
        self.Delete.configure(activebackground="#d9d9d9")
        self.Delete.configure(activeforeground="black")
        self.Delete.configure(background="#d9d9d9")
        self.Delete.configure(disabledforeground="#a3a3a3")
        self.Delete.configure(text='''Delete''')
        self.Delete.configure(command = self.delete)

        self.Moveto = tk.Button(self.top, activebackground="#d9d9d9", background="#d9d9d9")
        self.Moveto.configure(text='''Move to''')
        self.Moveto.configure(command = self.moveto)
        
        self.Next = tk.Button(self.top, activebackground="#d9d9d9", background="#d9d9d9")
        self.Next.configure(text='''Next''')
        self.Next.configure(command = self.next)

        self.Back = tk.Button(self.top, activebackground="#d9d9d9", background="#d9d9d9")
        self.Back.configure(text='''Back''')
        self.Back.configure(command = self.back)

        self.Enter = Button(self.top, activebackground="#d9d9d9", background="#d9d9d9")
        self.Enter.configure(command = self.move_into_current, text = "Move into current")

        # self.Move_back = Button(self.top, activebackground="#d9d9d9", background="#d9d9d9")
        # self.Move_back.configure(command = self.move_back, text = "Move into previous")
        

        # self.ChangeDir = Button(self.top, activebackground="#d9d9d9", background="#d9d9d9")
        # self.ChangeDir.configure(command = self.openOther, text = "Set Directories")

        self.Extra_preview = Button(self.top)
        self.Extra_preview.configure(command = self.open_preview, text = "View Surrounding Files")
        self.Extra_preview.configure(background="#d9d9d9")
        self.Extra_preview.configure(foreground="#000000")
        self.Extra_preview.configure(activebackground = "#d9d9d9")

       

        positions = linspace(.03, .35, 5)
        positions2 = linspace(.01, .29, 3)
        width = 67
        p1height = .64
        self.Next.place(relx=positions[1], rely=p1height, height=26, width=width)
        #self.Open.place(relx=positions[5], rely=0.537, height=26, width=width)
        self.Delete.place(relx=positions[3], rely=p1height, height=26, width=width)
        self.RegexB.place(relx=positions[4], rely=p1height, height=26, width=width)
        self.Moveto.place(relx=positions[2], rely=p1height, height=26, width=width)
        self.Back.place(relx=positions[0], rely=p1height, height=26, width=width)

        p2height = .56
        #self.ChangeDir.place(relx = positions2[0], rely=p2height, width = width*2)
        self.Enter.place(relx = positions2[1], rely = p2height, height = 26, width=width*2)
        #self.Move_back.place(relx = positions2[2], rely = p2height, height = 26, width=width*2)
        self.Extra_preview.place(relx = .420, rely = .01, anchor = 'ne', height = 26, width = width*2.5)
        self.helpMessage = r"""Welcome! 
___________________
The organizer defaults to operate within whatever directory this app was launched from, go to change directories to change this. Change Directories can take an absolute or relative path. Relative paths are relative to Target Directory
___________________
Some options take arguments from the command line input. Type into the command line and then select the desired option
___________________
Options that aren't buttons are in the Additonal Options pop down menu located next to the help button

Options:
Find:
Using Regex search, sets current file to the first match. For example, F.* locates the first file that starts with an F. Click on Help in regex for more regex info
___________________
Change Directories: 
Opens Change directories window. Used to change source or target directory. Takes relative or absolute path
___________________
Move into current/previous: 
Sets source directory into the current viewed directory or to one less than current source path
___________________
Move To [dest]: 
Moves file to destination directory typed in command line
___________________
New Folder [name]: 
Creates new folder in directory specified in the command line input and moves current file into it
___________________
Delete: 
Moves current file to Trash folder
___________________
Regex: 
Returns the files found by a regex search through the current source directory. Takes in a regex pattern from the command line. Check out the regex popup window help menu for more info
"""
        # self.Text2 = tk.Text(self.top)
        # self.Text2.place(relx=0.013, rely=0.67, relheight=0.30, relwidth=0.357)
        # self.Text2.configure(background="#d9d9d9")
        # self.Text2.configure(font="TkTextFont")
        # self.Text2.configure(foreground="black")
        # self.Text2.configure(highlightbackground="#43f0fe")
        # self.Text2.configure(highlightcolor="#000000")
        # self.Text2.configure(insertbackground="#000000")
        # self.Text2.configure(selectbackground="#d9d9d9")
        # self.Text2.configure(selectforeground="black")
        # self.Text2.configure(wrap="word")
        # self.Text2.insert(1.0, helpMessage)

        self.Preview = ScrolledText(self.top)
        self.Preview.place(relx=0.425, rely=0.015, relheight=0.949
                , relwidth=0.558)
        self.Preview.configure(background="white", insertofftime = 800, insertontime = 700)
        self.Preview.configure(font="TkTextFont")
        self.Preview.configure(foreground="black")
        self.Preview.configure(highlightbackground="#d9d9d9")
        self.Preview.configure(highlightcolor="#000000")
        self.Preview.configure(insertbackground="#000000")
        self.Preview.configure(insertborderwidth="3")
        self.Preview.configure(selectbackground="#d9d9d9")
        self.Preview.configure(selectforeground="black")
        self.Preview.configure(wrap="word")

        self.PictureFrame = tk.Label(self.top)
        self.PictureFrame.place(relx=0.425, rely=0.015, height=23, width=81, anchor = "nw")
        self.PictureFrame.configure(activebackground="#d9d9d9")
        self.PictureFrame.configure(activeforeground="black")
        
        self.currentSource = tk.Label(self.top)
        self.currentSource.configure(background="#d9d9d9", text = "Current Source Directory:")
        self.labelSource = tk.Label(self.top)
        self.labelSource.configure(background="#d9d9d9", textvariable = self.currentS)

        self.currentDest = tk.Label(self.top)
        self.currentDest.configure(background="#d9d9d9", text = "Current Target Directory:")
        self.labelDest = tk.Label(self.top)
        self.labelDest.configure(background="#d9d9d9", textvariable = self.currentD)
        
        self.trash_label = tk.Label(self.top, text = f"Trash location: {org.trash}", background = "#d9d9d9")
    

        xpos_labels = .01
        ystart_labels = .15
        self.currentSource.place(relx = xpos_labels, rely = ystart_labels, anchor = "w")
        self.currentDest.place(relx = xpos_labels, rely = ystart_labels+.03, anchor = "w")
        self.labelSource.place(relx = xpos_labels+.12, rely = ystart_labels, anchor = "w")
        self.labelDest.place(relx = xpos_labels+.12, rely = ystart_labels+.03, anchor = "w")
        self.trash_label.place(relx=xpos_labels, rely = ystart_labels+.06, anchor = "w")
        
        self.TLabel3 = ttk.Label(self.top)
        self.TLabel3.place(relx=0.007, rely=0.071, height=20, width=29)
        self.TLabel3.configure(font="TkDefaultFont")
        self.TLabel3.configure(relief="flat")
        self.TLabel3.configure(anchor='w')
        self.TLabel3.configure(justify='left')
        self.TLabel3.configure(text='''File:''')
        self.TLabel3.configure(compound='left')
        self.TLabel3.configure(background = "#d9d9d9")

        self.TEntry2 = ttk.Entry(self.top)
        self.TEntry2.place(relx=0.076, rely=p1height+.1, height = 24
                , relwidth=0.25, anchor = "nw")
        self.TEntry2.configure(takefocus="")
        self.TEntry2.configure(cursor="ibeam")
        self.TEntry2.configure(textvariable = self.entry)

        self.TLabel4 = ttk.Label(self.top)
        self.TLabel4.place(relx=0.028, rely=0.071, height=20, relwidth = .38)
        self.TLabel4.configure(font="-family {Segoe UI} -size 9")
        self.TLabel4.configure(relief="flat")
        self.TLabel4.configure(anchor='w')
        self.TLabel4.configure(justify='left')
        self.TLabel4.configure(textvariable=self.File)
        self.TLabel4.configure(compound='left')
        self.TLabel4.configure(cursor="fleur")
        self.TLabel4.configure(background = "#d9d9d9")
        self.File.set(self.org.getCurrent())
        self.preview()

class Extra_preview:
    def update(self):
        if (isinstance(self.files, StringVar)):
            text = self.files.get()
        elif (isinstance(self.files, list)):
            text = ""
            for item in self.files:
                text = f"{text}\n{item}"
        elif (isinstance(self.files, str)):
            text = self.files
        else: text = "Can't show that :("
            
        self.preview.delete(0.0, tk.END)
        self.preview.insert(0.0, text)
            
    def __init__(self, files,name, wrap,top):
        top.geometry("500x800+104+30")
        self.top = top
        top.title(name)
        self.files = files
        self.preview = Text(top, wrap = wrap)
        top.attributes("-topmost", True)

        self.preview.place(relx = .01, rely = 0.01, relwidth = .98, relheight = .98)
        if (isinstance(self.files, StringVar)):
            text = self.files.get()
        elif (isinstance(self.files, list)):
            text = ""
            for item in self.files:
                text = f"{text}\n{item}"
        elif (isinstance(self.files, str)):
            text = self.files
        else: text = "Can't show that :("
        self.preview.insert(0.0, text)

class Regex_window:
    def move_all(self):
        dest = self.commandline.get()
        files = self.preview.get(0.0, tk.END).splitlines()
        path = self.master.org.path
        pathto = self.master.org.pathto
        if ("c:\\" in dest.lower() or dest.startswith(delim)):
            for file in files:
                if (len(file)):
                    move(os.path.join(path,file), dest)
        else:
            for file in files:
                if (len(file)):
                    move(os.path.join(path,file), os.path.join(pathto, dest))
        self.preview.delete(0.0, tk.END)
        self.master.preview()
    def delete_all(self):
        files = self.preview.get(0.0, tk.END).splitlines()
        path = self.master.org.path
        for file in files:
            if (len(file)):
                file_full = os.path.join(path, file)
                move(file_full,self.master.org.trash)
        self.preview.delete(0.0, tk.END)
        self.master.preview()
    def Preview(self):
        files = self.preview.get(0.0, tk.END).splitlines()
        for file in files:
            if not len(file):
                files.remove(file)
        top1 = tk.Toplevel(self.top)
        new_org = sorter(pathto=self.master.org.pathto, files=files, trash=self.master.org.trash)
        Toplevel2(org=new_org, top=top1)
    def help_menu(self):
        help = r"""
Regex help:
Used to search for files whose names follow a certain pattern avoiding folders and files that follow a pattern
use: [search pattern] --avoid [avoid pattern]
avoid is an optional field

When deleting all or moving all, the program looks
at what is left in the message box. Thus, delete any 
files from the textbox that you don't want to affect
New Folder creates a folder with whatever name you have
in the command line. It then moves all files left in the 
message box into the new folder. The name can be a path

Basic Guide: (go to https://docs.python.org/3/library/re.html for more)
 .  : Matches any character
 \  : Escape character. Place before a special character like ., ), or { to match the character
 ^  : Matches start of string
 $  : Matches end of string
 *  : Matches 0 or more repetitions of the pattern to the left
 +  : Matches 1 or more repetitionsof the pattern to the left
 ?  : Matches 0 or 1 repetitions of the pattern to the left
{m} : Matches m repetitions of pattern to the left
{m,n} : Matches m to n repetitions of pattern to the left
(a|b) : Matches a or b. a and b can be patterns Can be combined with more parenthesis for complex patterns or more | for more options

\d : Matches a digit
\D : Matches anything but a digit
\s : Matches whitespace
\S : Matches anything but whitespace

Examples:
.* matches any file
.*\(\d\).* matches any file name that has (digit), useful for locating duplicates
.*(l|L)ab.* matches any file name that contains lab or Lab
.*\.(exe|jpg|txt) matches any file that ends in .exe .txt or .jpg
""" 
        top1 = tk.Toplevel(self.top)
        Extra_preview(help, "Help", "word", top1)
    def update(self):
        if (isinstance(self.files, StringVar)):
            text = self.files.get()
        elif (isinstance(self.files, list)):
            text = ""
            for item in self.files:
                text = f"{text}\n{item}"
        else: text = "Can't show that :("
        self.preview.delete(0.0, tk.END)
        self.preview.insert(0.0, text)
    def newFolder(self):
        dest = self.commandline.get()
        files = self.preview.get(0.0, tk.END).splitlines()
        path = self.master.org.path
        pathto = self.master.org.pathto
        
        if (not ("c:\\" in dest.lower() or dest.startswith(delim))):
            dest = os.path.join(pathto, dest)
        if (not len(dest)):
            dest = "New"
        if (os.path.isdir(f"{dest}")):
            j=0
            while (os.path.isdir(f"{dest}({j})")):
                j+=1
            dest = f"{dest}({j})"
        os.makedirs(dest)
        for file in files:
                if (len(file)):
                    move(os.path.join(path,file), dest)
        self.master.org.change_source(dest)
        self.master.preview()
        self.top.destroy()
            
    def __init__(self, files ,name,master,top=None):
        top.geometry("500x800+104+30")
        self.top = top
        self.master = master
        top.title(name)
        self.files = files
        self.preview = Text(top, wrap = 'none', insertofftime = 800, insertontime = 700)
        top.attributes("-topmost", True)
        #self.menubar = Menu(top)
        

        self.preview.place(relx = .05, rely = .05, relwidth = .9, relheight = .7)
        
        if (isinstance(self.files, StringVar)):
            text = self.files.get()
        elif (isinstance(self.files, list)):
            text = ""
            for item in self.files:
                text = f"{text}\n{item}"
        else: text = "Can't show that :("
        self.preview.insert(0.0, text)
        self.Additional_options = Menu(top, tearoff = False)
        self.Additional_options.add_command(label = "Help",command =self.help_menu)
        self.Additional_options.add_command(label = "Detailed Preview", command = self.Preview)
        top.config(menu = self.Additional_options)
        #self.menubar.add_cascade(label="Help", menu = self.Additional_options)

        self.entry = StringVar()
        self.commandline = ttk.Entry(top)
        self.commandline.place(relx=.5, rely=.8, relwidth=0.8, anchor = "s")
        self.commandline.configure(textvariable = self.entry)

        self.Delete = tk.Button(top, activebackground="#d9d9d9", activeforeground="black", background="#d9d9d9")
        self.Delete.configure(disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 9", foreground="#000000")
        self.Delete.configure(highlightbackground="#d9d9d9", highlightcolor="#000000")
        self.Delete.configure(text='''Delete All''')
        self.Delete.configure(command = self.delete_all)

        self.Moveto = tk.Button(top, activebackground="#d9d9d9", activeforeground="black", background="#d9d9d9")
        self.Moveto.configure(disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 9", foreground="#000000")
        self.Moveto.configure(highlightbackground="#d9d9d9", highlightcolor="#000000")
        self.Moveto.configure(text='''Move All To''')
        self.Moveto.configure(command = self.move_all)
        self.Back = tk.Button(top)

        self.Folder  = tk.Button(top, activebackground="#d9d9d9", activeforeground="black", background="#d9d9d9")
        self.Folder.configure(disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 9", foreground="#000000")
        self.Folder.configure(highlightbackground="#d9d9d9", highlightcolor="#000000")
        self.Folder.configure(text='''New Folder''')
        self.Folder.configure(command = self.newFolder)

        self.Delete.place(relx = .1, rely = .9, anchor = "w")
        self.Moveto.place(relx = .5, rely = .9, anchor = "w")
        self.Folder.place(relx = .8, rely = .9, anchor = "w")

class message:
    def __init__(self, message, top):
        top.title("help")
        top.attributes("-topmost", True)
        label = tk.Text(master = top, wrap = "word")
        label.place(relx=0, rely=0, relwidth=1, relheight=1)
        label.insert(0.0, message)
        label.configure(state = 'disabled')

class Settings_window:
    def change_setting(self, item,*args):
        text = self.entries[item].get()
        self.settings[item] = int(text)
        self.setting_items[item].configure(text = f"{item}: {text}")
        self.main.preview()
    
    def __init__(self, vars, main,top=None):
        top.geometry("400x300")
        top.title("Settings")
        self.settings = vars
        self.entries = {}
        self.setting_items = {}
        self.buttons = {}
        self.main = main
        locx = .90
        locy = linspace(.1, .8, len(vars))
        buttonwidth = .1
        boxwidth = .1
        self.top = top
        buffer=.03
        for i, item in enumerate(self.settings):
            setting = tk.Label(self.top, text = f"{item}: {self.settings[item]}")
            entrybox = tk.Entry(self.top)
            button = ttk.Button(self.top, text = "Set",command = lambda i=item: self.change_setting(item = i))
            button.place(relx = locx, rely = locy[i],relwidth= buttonwidth, anchor = "e")
            setting.place(relx = locx-buttonwidth-boxwidth-2*buffer, rely = locy[i], anchor = "e")
            entrybox.place(relx = locx-buttonwidth-buffer, rely = locy[i], anchor = "e", relwidth = boxwidth)
            
            self.entries[item] = entrybox
            self.setting_items[item] = setting
            self.buttons[item] = button


### Generated by Page ###
# The following code is added to facilitate the Scrolled widgets
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)


def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledText(AutoScroll, tk.Text):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')
def start_up():
    Organize_support.main()

if __name__ == '__main__':
    Organize_support.main()
