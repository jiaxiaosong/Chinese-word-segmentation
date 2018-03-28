#-*- coding: utf-8 -*-
import re
import os
import sys
path = os.getcwd()
sys.path.append('{}/foo'.format(path))
import dict_process
import segmentation
from tkinter.messagebox import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import *
from tkinter import simpledialog
from tkinter.filedialog import *

#Main Window
root = Tk()
root.title('Chinese Word Segment')
root.geometry('1270x550')
root.resizable(False, False)
path = os.getcwd()
lex_name = '{}/doc/word_dict.txt'.format(path)
lex = dict_process.load_dict(lex_name)
lex_inverse = {}
for key in lex:
    lex_inverse[key[::-1]] = lex[key]
algorithm = 'inverse'



# Background
background = PhotoImage(file='{}/background/background.gif'.format(path))
pic1 = PhotoImage(file='{}/background/logo1.gif'.format(path))
pic2 = PhotoImage(file='{}/background/logo2.gif'.format(path))
pic3 = PhotoImage(file='{}/background/logo3.gif'.format(path))
background_label = Label(root, image=background)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
logo1 = Label(root, text='CHINESE', relief=SUNKEN, borderwidth=0,  bg='#1B1A3B', image=pic1, compound='center',
              fg='Snow', font=('Monotype Corsiva', 25, 'normal')).grid(row=1, column=1)
logo2 = Label(root, text='WORD', relief=SUNKEN, borderwidth=0, bg='#373A95', image=pic2, compound='center', fg='Snow',
              font=('Monotype Corsiva', 30, 'normal')).grid(row=2, column=1)
logo3 = Label(root, text='SEGMENT', relief=SUNKEN, borderwidth=0, bg='#33AACC', image=pic3, compound='center',
              fg='Snow', font=('Monotype Corsiva', 25, 'normal')).grid(row=3, column=1)


# Input entry
def save_source_as():
    content = source.get(1.0, END)
    filetypes = [('Text Files', '*.txt', 'TEXT')]
    fobj = asksaveasfile(filetype=filetypes, initialfil="未命名.txt", defaultextension=".txt",initialdir='{}/save'.format(path))
    if fobj:
        fobj.write(content)


Label(root, text='Input', bg='#131125', fg='red', font=('Monotype Corsiva', 25, 'normal')).grid(row=0, column=2)
source = ScrolledText(root, width=28, height=37)
source.grid(row=1, column=2, rowspan=3)
Button(root, text='Save the\n source text as...', bg='black', fg='orange', width=10, height=3,
       font=('Monotype Corsiva', 18, 'normal'), command=save_source_as).grid(row=3, column=4, padx=13, sticky=E)


# Segment sentence UI
def seg_sent():
    sent = source.get(0.0, END)
    sent = sent[0:-1]
    well_seg = segmentation.seg_sentence(sent)
    if well_seg == '':
        showinfo(title='Segment sentences', message='The input text is empty!')
    else:
        sen_seged.delete(1.0, END)
        sen_seged.insert(END, well_seg)


def save_sent_as():
    content = sen_seged.get(1.0, END)
    filetypes = [('Text Files', '*.txt', 'TEXT')]
    fobj = asksaveasfile(filetype=filetypes, initialfil="未命名.txt", defaultextension=".txt", initialdir='{}/save'.format(path))
    if fobj:
        fobj.write(content)

Label(root, text='Segmented sentences', bg='#242245', fg='red', font=('Monotype Corsiva', 25, 'normal')).grid(row=0, column=5)
sen_seged = ScrolledText(root, width=28, height=37)
sen_seged.grid(row=1, column=5, rowspan=3)
Button(root, text='segment\nsentence', bg='black', fg='orange',width=10, height=2,
       font=('Monotype Corsiva', 18, 'normal'), command=seg_sent).grid(row=1, column=4, padx=13,sticky=E)
Button(root, text='Save the\n segmented\nsentences as...', bg='black', fg='orange', width=10, height=3,
       font=('Monotype Corsiva', 18, 'normal'), command=save_sent_as).grid(row=2, column=4, padx=13, sticky=E)


# Segment words UI
def seg_words():
    global lex
    global lex_inverse
    sent = sen_seged.get(0.0, END)
    sent = sent[0:-1]
    if algorithm == 'inverse':
        well_sent = segmentation.seg_inverse(sent, lex_inverse)
    elif algorithm == 'forward':
        well_sent = segmentation.seg_forward(sent, lex)
    if well_sent == '':
        showinfo(title='Segment words', message='The segmented sentences text is empty!')
    else:
        word_seged.delete(1.0, END)
        word_seged.insert(END, well_sent)

def save_word_as():
    content = word_seged.get(1.0, END)
    filetypes = [('Text Files', '*.txt', 'TEXT')]
    fobj = asksaveasfile(filetype=filetypes, initialfil="未命名.txt", defaultextension=".txt",initialdir='{}/save'.format(path))
    if fobj:
        fobj.write(content)

def copyright():
    showinfo(title='Copyright', message='''Author: Xiaosong Jia, Mingze Li,Zhenghao Chai.
    \nCopyright © 2016 Three's Company.All rights reserved.''')
    return
Label(root, text='Segmented words', bg='#131125', fg='red',
      font=('Monotype Corsiva', 25, 'normal')).grid(row=0, column=8)
Button(root, text='segment\nwords', bg='black', fg='orange', width=10, height=2,
       font=('Monotype Corsiva', 18, 'normal'),command=seg_words).grid(row=1, column=6, padx=13)
Button(root, text='Save the \nsegmented\nwords as...', bg='black', width=10, height=3, fg='orange',
       font=('Monotype Corsiva', 18, 'normal'),command=save_word_as).grid(row=2, column=6, padx=13)
Button(root, text='About us', bg='black', width=10, height=3, fg='orange',
       font=('Monotype Corsiva', 18, 'normal'),command=copyright).grid(row=3, column=6, padx=13)
word_seged = ScrolledText(root,  width=28, height=37)
word_seged.grid(row=1, column=8, rowspan=3)


#Menu
main_menu = Menu(root)
root['menu'] = main_menu


#File menu
File_menu = Menu(main_menu)
main_menu.add_cascade(label='File', menu=File_menu)

def open_a_file():
    filetypes = [('Text Files', '*.txt', 'TEXT')]
    filename = askopenfilename(filetype=filetypes,initialdir='{}/doc'.format(path))
    if filename == '':
        filename = None
    else:
        try:
            with open(filename, 'r') as f:
                 text = f.read()
                 source.delete(1.0, END)
                 source.insert(1.0, text)
        except:
            showinfo(title='Open file', message='Fail to open the file(Tips:encoding should be utf8)')


def Exit():
    root.destroy()

File_menu.add_command(label='Open', command=open_a_file)
File_menu.add_command(label='Save source text as...', command=save_source_as)
File_menu.add_command(label='Save segmented sentences as...', command=save_sent_as)
File_menu.add_command(label='Save segmented words as...', command=save_word_as)
File_menu.add_command(label='Exit', command=Exit)



#Edit menu
Edit_menu = Menu(main_menu)
main_menu.add_cascade(label='Edit', menu=Edit_menu)


# Let edit menu can be used to all text
def seteditor(event=None):
    global editor
    editor = event.widget
root.bind_class("Text", "<Any-KeyPress>", seteditor, add=True)
root.bind_class("Text", "<Button-1>", seteditor, add=True)


def cut():
    try:
        editor.event_generate('<<Cut>>')
        return
    except:
        pass
def copy():
    try:
        editor.event_generate('<<Copy>>')
        return
    except:
        pass
def paste():
    try:
        editor.event_generate('<<Paste>>')
        return
    except:
        pass


def input_sentence():
    sentence=simpledialog.askstring('input sentence', 'Please input the sentence')
    if isinstance(sentence, str):
        source.insert(END, sentence)
    return

Edit_menu.add_command(label='Cut', command=cut)
Edit_menu.add_command(label='Copy', command=copy)
Edit_menu.add_command(label='Paste', command=paste)
Edit_menu.add_command(label='Input sentence into input text', command=input_sentence)


#Popupmenu
def popmenu(event):
        Edit_menu.post(event.x_root, event.y_root)
root.bind('<Button-3>', popmenu)


#Segmentation menu
Seg_menu=Menu(main_menu)
main_menu.add_cascade(label='Segmentation', menu=Seg_menu)


def inverse():
    global algorithm
    algorithm = 'inverse'
def forward():
    global algorithm
    algorithm = 'forward'
Seg_menu.add_radiobutton(label='Algorithm: Inverse', command=inverse)
Seg_menu.add_radiobutton(label='Algorithm: Forward ', command=forward)
Seg_menu.add_separator()
Seg_menu.add_command(label='Segment sentences', command=seg_sent)
Seg_menu.add_command(label='Segment words', command=seg_words)


#Lexicon menu
Lex_menu = Menu(main_menu)
main_menu.add_cascade(label='Lexicon', menu=Lex_menu)


def load_lex():
    global lex
    global lex_name
    global lex_inverse
    try:
        lex_new_name = askopenfilename(initialdir='{}/doc'.format(path))
        lex = dict_process.load_dict(lex_new_name)
        lex_inverse = {}
        for key in lex:
            lex_inverse[key[::-1]] = lex[key]
        lex_name = lex_new_name
        showinfo(title='Load the lexicon', message='Load the lexicon successfully!')
    except:
        showinfo(title='Load the lexicon', message='Fail to load the lexicon!')
    return


def add_word():
    global lex
    global lex_name
    global lex_inverse
    tip='''Input the words you want to add. Format:(words only) or (words with frequency '一个 818357166') '''
    word = simpledialog.askstring('Add words', tip)
    if isinstance(word, str):
        result, lex = dict_process.add_words(word, lex, lex_name)
        lex_inverse = {}
        for key in lex:
            lex_inverse[key[::-1]] = lex[key]
        showinfo(message=result, title='Add words')
        return
    else:
        return


def modify_word():
    global lex
    global lex_name
    global lex_inverse
    old = simpledialog.askstring('Old word', 'Please input the word you want to modify')
    if isinstance(old, str):
        new = simpledialog.askstring('New word', 'Please input the word you want to add')
        if isinstance(old, str) and isinstance(new, str):
            result, lex = dict_process.revise_words(old, new, lex, lex_name)
            showinfo(message=result, title='Modify words')
            lex_inverse = {}
            for key in lex:
                lex_inverse[key[::-1]] = lex[key]
    else:
        return


def del_word():
    global lex
    global lex_name
    global lex_inverse
    tip = '''format of the words you want to delete: '大家 你好' (words separated by space) '''
    word = simpledialog.askstring('Delete words', tip)
    if isinstance(word, str):
        result, lex = dict_process.delete_words(word, lex, lex_name)
        showinfo(message=result, title='Add words')
        lex_inverse = {}
        for key in lex:
            lex_inverse[key[::-1]] = lex[key]
    else:
        return


def look_up():
    global lex_name
    os.system(lex_name)
    return

Lex_menu.add_command(label='Load the lexicon', command=load_lex)
Lex_menu.add_command(label='Add words into the lexicon', command=add_word)
Lex_menu.add_command(label='Modify a word in the lexicon', command=modify_word)
Lex_menu.add_command(label='Delete a word in the lexicon', command=del_word)
Lex_menu.add_command(label='Look up the lexicon', command=look_up)


#Help menu
Help_menu = Menu(main_menu)
main_menu.add_cascade(label='Help', menu=Help_menu)


def instruction():
    os.system('readme.txt')
    return


Help_menu.add_command(label='Instruction', command=instruction)
Help_menu.add_command(label='Copyright', command=copyright)

root.mainloop()
