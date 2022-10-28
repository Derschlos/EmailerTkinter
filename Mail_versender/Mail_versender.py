# -*- coding: utf-8 -*-

import tkinter as tk
import pyautogui as ag
import os
import sqlite3
import json
from tkinter import messagebox
from Models import Kontakt, MailText
from tkinterdnd2 import DND_FILES, TkinterDnD
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
	"textId"	INTEGER NOT NULL,
	"directory"	TEXT,
	"personName"	TEXT NOT NULL,
	"attachFiles"	INTEGER,
	"addInfo"       TEXT,
	"cc"            TEXT,
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
        self.configVars  = configString
        self.root.config()
        self.root.title('Base page')
        self.root.geometry('370x200')
        self.baseContainer = tk.Frame(self.root)
        self.baseContainer.pack(side = "top", fill = "both", expand = True)
        self.baseContainer.grid_rowconfigure(0, weight = 1)
        self.baseContainer.grid_columnconfigure(0, weight = 1)
        self.lastFrame =''
        self.kontakts = {}
        self.texts = {}
        self.kontChoices = []
        self.textChoices = []
        self.textIdByTitle = {}
        self.con = sqlite3.connect('Kontakte.db')
        self.cur = self.con.cursor()

        self.initReadDB(self.cur)
        self.updateCombos()
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
        self.frames[pageName].resetVals()
        if self.frames[self.lastFrame].pageName==pageName:
            self.showFrame('SelectorPage')
            return
        if pageName == 'TextEditPage' and self.lastFrame == 'EditPage':
            self.frames['EditPage'].update(self.frames['TextEditPage'].selectedText)
        self.showFrame(self.lastFrame)
        
    def initReadDB(self, cur):
        existingData = self.cur.execute('SELECT * FROM Kontakte')
        for data in existingData:
            idNum, display, mail, textOptions, directory, person, attach, addInfo, cc = data
            kontakt =Kontakt()
            kontakt.fill(idNum, display, mail, textOptions, directory, person, attach, addInfo,cc)
            self.kontakts[display] = kontakt
        texts = self.cur.execute('SELECT * FROM MailTexte')
        for data in texts:
            idNum,text,subj, title = data
            textModel = MailText()
            textModel.fill(idNum, text, subj,title)
            self.texts[idNum] = textModel

    def updateCombos(self):
        self.kontChoices = list(self.kontakts.keys())
        self.kontChoices.append('<New Contact>')
        self.textChoices = [text.title for idNum,text in self.texts.items()]
        self.textChoices.append('<New Text>')
        self.textIdByTitle = {textMod.title:idNum for idNum, textMod in self.texts.items()}

        

if __name__ == '__main__':
    setupDB()
    configFile= 'Config.txt'
    configString = '''{"Username": "David Leon Schmidt",
                "baseColor" : "lightsalmon",
                "EditPageColor" : "lightsalmon",
                "EditPageDimensions" : "535x520",
                "CreateMailColor": "lightsalmon",
                "CreateMailDimensions" : "587x365",
                "TreeColors": {
                                "Text":"sea green",
                                "Kontakt":"paleturquoise"
                                },
                "TextEditPageColor" : "lightsalmon",
                "TextEditPageDimensions" : "780x365",
                "TextBlock": {
                                "Contact person": ["{selectedPerson}", "lightgreen"],
                                "File" : ["{file}", "lightblue"],
                                "All Files" : ["{allFiles}", "indian red"], 
                                "Link" : ["{link}", "lightyellow"],
                                "Additional Info": ["{addInfo}", "lightgreen"]
                            },
                "TextMarkers": {
                                "bold":["<b>","</b>"],
                                "italic": ["<i>","</i>"],
                                "underlined":["<u>","</u>"]
                                },
                "MailConfig":{
                                "LinkColor": "DodgerBlue",
                                "TextColor": "#002367",
                                "Font":"Verdana",
                                "FontSize":10
                                }
                        }'''
    #textcolor "MidnightBlue",
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
