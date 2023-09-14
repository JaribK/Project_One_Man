import tkinter as tk
import pytz #pip3 install pytz
import codecs

############################################################################################################################################################################

from tkinter import *
from tkinter import messagebox
from googletrans import Translator #pip3 install googletrans
from datetime import datetime

############################################################################################################################################################################

app = tk.Tk()
app.title('miniTranslate')

############################################################################################################################################################################

def clear_history():
    with codecs.open('history_trans.csv','w','utf-8') as file :
        file.write('History translation')
        file.close()
    exit_app(window0)
    show_history()

def show_history():
    global window0
    window0 = tk.Tk()
    window0.title('History translation')

    with codecs.open('history_trans.csv','r','utf-8') as file :
        Label(window0,text=f'{file.read()}').pack()

    my_menu = Menu(window0)
    window0.config(menu = my_menu)

    menuitem2 = Menu(my_menu)
    menuitem2.add_command(label='Clear historys',command=clear_history)
    menuitem2.add_command(label='Openfile Historys')

    my_menu.add_cascade(label='Options',menu=menuitem2)
    
    window0.geometry('500x500')
    window0.mainloop()

def exit_app(self):
    self.destroy()

def show_version():
    messagebox.showinfo(title='Notifications',message='Version alpha 1.0')

def show_developer():
    messagebox.showinfo(title='Notifications',message='this Programme develop by Yor-in Udomwattanakul')

def save_history_trans(text : str):
    with codecs.open('history_trans.csv','a',"utf-8") as file :
        file.write(text)
        file.close()

def translate_to_Th():
    tz = pytz.timezone('Asia/Bangkok')
    datetime_TH = datetime.now(tz)
    text = txt.get()
    if text.isdigit():
        Label(app,text='please type the letter.').pack()
    else:
        translator = Translator()
        translate_text_to_th = translator.translate(text, src='auto', dest='th').text
        Label(app,text=f'[{datetime_TH.strftime("%H:%M:%S")}] ' + f'{text}' + ' ในภาษาไทยคือ '+ f'{translate_text_to_th}',font='Itim').pack()
        save_history_trans('\n'+f'วันที่ [{datetime_TH.strftime("%d/%m/%Y")}]' + f' เวลา [{datetime_TH.strftime("%H:%M:%S")}] มีการแปลคำว่า '+ f'{text}' + ' ให้เป็นภาษาไทย คือ '+ f'{translate_text_to_th}')

def translate_to_Eng():
    tz = pytz.timezone('Asia/Bangkok')
    datetime_TH = datetime.now(tz)
    text = txt.get()
    translator = Translator()
    translate_text_to_en = translator.translate(text, src='auto', dest='en').text
    Label(app,text=f'[{datetime_TH.strftime("%H:%M:%S")}] ' + f'{text}' +' ในภาษาอังกฤษคือ ' + f'{translate_text_to_en}',font='Itim').pack()
    save_history_trans('\n'+f'วันที่ [{datetime_TH.strftime("%d/%m/%Y")}]' + f' เวลา [{datetime_TH.strftime("%H:%M:%S")}] มีการแปลคำว่า '+ f'{text}' + ' ให้เป็นภาษาอังกฤษ คือ '+ f'{translate_text_to_en}')

############################################################################################################################################################################
myMenu = Menu()
app.config(menu = myMenu)
############################################################################################################################################################################
menuitem0 = Menu()
menuitem0.add_command(label='Historys',command=show_history)
menuitem0.add_command(label='Exit',command=exit_app)
############################################################################################################################################################################
menuitem1 = Menu()
menuitem1.add_command(label='How to use?')
menuitem1.add_command(label='Developer',command=show_developer)
menuitem1.add_command(label='Version',command=show_version)
############################################################################################################################################################################
myMenu.add_cascade(label='Options',menu=menuitem0)
myMenu.add_cascade(label='Helps',menu=menuitem1)

# row แถวนอน col หลักตั้ง
title0 = tk.Label(text='What language do you want to translate?',font='Itim 11').pack()
txt = StringVar()
entry0 = tk.Entry(app,textvariable=txt,width=70,font='Itim').pack(pady=10)
button0 = tk.Button(app,text='Translate to Thai',command=translate_to_Th,font='Itim 11').pack()
button1 = tk.Button(app,text='Translate to Eng',command=translate_to_Eng,font='Itim 11').pack()
app.geometry('500x500')
app.mainloop()