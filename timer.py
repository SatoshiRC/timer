from tkinter import *
from tkinter import ttk
import time
import tkinter.font as font
import math
from playsound import playsound
from mutagen.mp3 import MP3 as mp3
import pygame
import threading
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

#load audio file
singleBell = resource_path("./sei_ge_bell01.mp3")
doubleBell = resource_path("./sei_ge_bell01.mp3")

#main window configure
root = Tk()
root.title(u"timer")
root.state('zoomed')
root.option_add('*font', ('FixedSys', 14))
root.minsize(300, 200)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.configure(background='white')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

var = StringVar()
var.set('normal')

# menu command
start_time=0
def start():
    global flag6
    global flag7
    global start_time
    global isStart
    isStart = 1
    start_time = time.time()
    flag7 = 0
    flag6 = 0
    def_page.tkraise()

def reset_key(self):
    global flag6
    global flag7
    global start_time
    global isStart
    start_time = time.time()
    flag7 = 0
    flag6 = 0
    isStart = 0
    buff1.set("00:00")
    def_page.tkraise()

def reset():
    global flag6
    global flag7
    global start_time
    global isStart
    start_time = time.time()
    flag7 = 0
    flag6 = 0
    isStart = 0
    buff1.set("00:00")
    def_page.tkraise()

def stop():
    global isStart
    isStart = 0

def control_S(self):
    global isStart
    if isStart:
        stop()
    else:
        start()
        
def changeFontSize():
    global my_font
    my_font.config(size=15)

def fontSizeUp(self):
    global my_font
    my_font.config(size=my_font.cget("size")+2)

def fontSizeDown(self):
    global my_font
    my_font.config(size=my_font.cget("size")-2)

def playAudio(file):
    print(file)
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    mp3_length = mp3(file).info.length #音源の長さ取得
    pygame.mixer.music.play(1) #再生開始。1の部分を変えるとn回再生(その場合は次の行の秒数も×nすること)
    time.sleep(mp3_length + 0.25) #再生開始後、音源の長さだけ待つ(0.25待つのは誤差解消)
    pygame.mixer.music.stop()
    pygame.mixer.stop()

# メニューの設定
m0 = Menu(root)
root.configure(menu = m0)

m1 = Menu(m0, tearoff = False)
m0.add_command(label="start", command=start)
m0.add_command(label="stop", command=stop)
m0.add_command(label="reset", command=reset)
m0.add_command(label="font size", command=changeFontSize)

# key bind
root.bind_all('<r>',reset_key)
root.bind_all('<e>',control_S)
root.bind_all('<Control-,>',fontSizeUp)
root.bind_all('<Control-.>',fontSizeDown)

# フレーム
buff1 = StringVar()
buff1.set('')
my_font = font.Font(root,family="tahoma",size=400,weight="bold")

def_page = Frame(root,bg='black')
timeLabel = Label(def_page,textvariable=buff1,font=my_font,foreground="green",background='black').pack()
def_page.grid(row=0, column=0, sticky="nsew")

page6 = Frame(root,bg='black')
Label(page6,textvariable=buff1,font=my_font,foreground="yellow",background='black').pack()
page6.grid(row=0, column=0, sticky="nsew")

page7 = Frame(root,bg='black')
Label(page7,textvariable=buff1,font=my_font,foreground="red",background='black').pack()
page7.grid(row=0, column=0, sticky="nsew")

def_page.tkraise()

# 時刻の表示
flag6=0
flag7=0
isStart = 0
def show_time():
    global isStart
    if isStart:
        global flag6
        global flag7
        time_now = time.time()
        time_dif = math.floor(time_now) - math.floor(start_time)
        time_dif = time_dif * 1
        min = math.floor(time_dif/60)
        second = math.floor(time_dif)%60
        
        if min<10 and second<10:
            buff1.set("0"+str(min)+":"+"0"+str(second))
        elif min<10:
            buff1.set("0"+str(min)+":"+str(second))
        elif second<10:
            buff1.set(str(min)+":"+"0"+str(second))
        else:
            buff1.set(str(min)+":"+str(second))

        if (min>=6)and flag6!=1:
            flag6=1

            global singleBell
            playBell = threading.Thread(target=playAudio, args=(singleBell,))
            playBell.start()

            timeLabel.configure()

            page6.tkraise()
        elif (min>=7) and flag7 != 1:
            flag7 = 1

            global doubleBell
            playBell = threading.Thread(target=playAudio, args=(doubleBell,))
            playBell.start()

            page7.tkraise()
    my_font.configure


    root.after(200, show_time)




show_time()
root.mainloop()
