# -*- coding: utf-8 -*-


#pyinstaller Kontoauszugversender.py -D -w --collect-all tkinterdnd2 --noconfirm
import tkinter as tk
import pyautogui as ag
import pyperclip
import time
import win32gui
import os
import sqlite3
import json
from tkinter import messagebox
from Models import Kontakt, MailText
from email import generator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from shutil import move
from tkinterdnd2 import DND_FILES, TkinterDnD
import switch
from SelectorPageData import SelectorPage
from EditPageData import EditPage
from TextEditData import TextEditPage

import re
from PyInstaller.utils.hooks import collect_data_files, eval_statement
datas = collect_data_files('tkinterdnd2')


def setupDB():
    db = 'Kontakte.db'
    if os.path.isfile(db):
        return
    con = sqlite3.connect('Kontakte.db')
    cur = con.cursor()
    kontaktTableCreate = """CREATE TABLE "Kontakte" (
	"id"	INTEGER NOT NULL UNIQUE,
	"displayName"	TEXT NOT NULL,
	"mail"	TEXT NOT NULL,
	"textId"	TEXT NOT NULL,
	"ordner"	TEXT,
	"personName"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
        )"""
    textTableCreate= """CREATE TABLE "MailTexte" (
                "id"	INTEGER NOT NULL UNIQUE,
                "text"	TEXT NOT NULL,
                "subject"	TEXT NOT NULL,
                "title"	TEXT,
                PRIMARY KEY("id" AUTOINCREMENT)
        )"""
    cur.execute(kontaktTableCreate)
    cur.execute(textTableCreate)
    return


def down(times = 1,extra = ''):
    ag.hotkey('numlock')
    for i in range(times):
        ag.hotkey('down', extra)
    ag.hotkey('numlock')

def tab(times = 1):
    for i in range(times):
        ag.hotkey('tab')
        time.sleep(0.1)
    return

def paste(text):
    pyperclip.copy(text)
    ag.hotkey('ctrl','v')
    time.sleep(0.3)

def navigate(instructionString):
    ag.hotkey('alt')
    ag.typewrite(instructionString, interval = 0.1)
    time.sleep(0.2)


        
class basedesk:
    def __init__(self,root, configString):
        self.root = root
        self.configString  = configString
        self.root.config()
        self.root.title('Base page')
        self.root.geometry('370x200')
        self.baseContainer = tk.Frame(self.root)
        self.baseContainer.pack(side = "top", fill = "both", expand = True)
        self.baseContainer.grid_rowconfigure(0, weight = 1)
        self.baseContainer.grid_columnconfigure(0, weight = 1)
        self.lastFrame =''
        self.kontakte = {}
        self.texts = {}
        
        self.con = sqlite3.connect('Kontakte.db')
        self.cur = self.con.cursor()
        self.initReadDB(self.cur)
        self.frames = {}
        for f in (SelectorPage,EditPage,TextEditPage):
            frame = f(self.baseContainer, self)
            self.frames[frame.pageName] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.showFrame('SelectorPage')
        
    def showFrame(self,frameName):
        frame= self.frames[frameName]
        frame.tkraise()
        frame.onRaise()

    def updateFrame(self, frameName,*args):
        try:
            self.frames[frameName].update(*args)
        except:
            pass
    def setLastFrame(self, frameName):
        self.lastFrame = frameName
        
    def returnToPrev(self, savedChanges, pageName):
        if savedChanges == False:
            message = messagebox.askyesnocancel(message = 'Do you want to save any changes?')
            if message == None:
                return
            elif message == True:
                self.frames[pageName].saveChanges()
            else:
                self.savedChanges = True        
        self.showFrame(self.lastFrame)
        
    def initReadDB(self, cur):
        existingData = self.cur.execute('SELECT * FROM Kontakte')
        for data in existingData:
            idNum, display, mail, textOptions, directory, person = data
            kontakt =Kontakt()
            kontakt.fill(idNum, display, mail, textOptions, directory, person)
            self.kontakte[display] = kontakt
        texts = self.cur.execute('SELECT * FROM MailTexte')
        for data in texts:
            idNum,text,subj, title = data
            textModel = MailText()
            textModel.fill(idNum, text, subj,title)
            self.texts[idNum] = textModel


if __name__ == '__main__':
    setupDB()
    configFile= 'Config.txt'
    configString = '''{"Username": "David Leon Schmidt",
                "baseColor" : "lightsalmon",
                "EditPageColor" : "lightsalmon",
                "EditPageDimensions" : "475x450",
                "CreateMailColor": "lightsalmon",
                "CreateMailDimensions" : "430x200",
                "TextEditPageColor" : "lightsalmon",
                "TextEditPageDimensions" : "500x500"}'''
    if os.path.isfile(configFile):
        with open(configFile, 'r') as f:
            configString = f.read()
    else:
        with open(configFile, 'w') as f:
            f.write(configString)
    configString= json.loads(configString)
    root= TkinterDnD.Tk()
    basedesk(root, configString)
    root.mainloop()
