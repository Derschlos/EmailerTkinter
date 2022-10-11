import tkinter as tk
##import pyautogui as ag
##import pyperclip
import time
##import win32gui
import os
import sqlite3
import json
from email import generator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from shutil import move
from tkinterdnd2 import DND_FILES, TkinterDnD
##import switch
import re
from PyInstaller.utils.hooks import collect_data_files, eval_statement
datas = collect_data_files('tkinterdnd2')



class SelectorPage(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
        self.pageName = 'SelectorPage'
##        self.root = root
        self.controller = controller
        self.kontakte = self.controller.kontakte
        self.kontChoices = list(self.kontakte.keys())
        self.kontaktVar = tk.StringVar(value=self.kontChoices)
        self.kontaktLBox = tk.Listbox(self, listvariable = self.kontaktVar)      
        self.startBut= tk.Button(self, text = 'create Mail/ablage', command = self.mail)
        self.drop_target_register(DND_FILES)

        self.files =[]
        self.dnd_bind('<<Drop>>',lambda e: self.cleanFiles(e.data))
        self.filePath = {}
        self.fileVar = tk.StringVar(value=self.files)
        self.fileLBox = tk.Listbox(self, listvariable = self.fileVar,width = 50)
        self.fileLBox.bind('<Double-Button-1>',lambda e:self.delFile())
        self.editKontaktsBut = tk.Button(self, text = 'Edit Contacts', command = lambda:(self.controller.showFrame('EditPage'),self.controller.setLastFrame(self.pageName)))
        self.editTextsBut = tk.Button(self, text = 'Edit Texts', command = lambda:(self.controller.showFrame('TextEditPage'),self.controller.setLastFrame(self.pageName)))
        
        self.kontaktLBox.grid(column=0, row=0, )
        self.fileLBox.grid(column=1, row=0)
        self.editKontaktsBut.grid(column=0, row=1)
        self.editTextsBut.grid(column=1, row=1)
##        self.startBut.grid(column=1, row=1, columnspan = 2)
        

    def onRaise(self):
        self.controller.root.title('Create E-Mail')
        self.controller.root.config()
        self.controller.root.geometry(self.controller.configVars['CreateMailDimensions'])
        self.config(bg = self.controller.configVars['CreateMailColor'])
         
    def update(self, *args):
        pass
    
    def cleanFiles(self, data):
        isolatedSpaces = []
        data = data.split('}')
        for dat in data:
            split = dat.split('{')
            isolatedSpaces+=[file for file in split if file != ' ']
        for dat in isolatedSpaces:
            if dat == '':
                continue
            if dat[0] == ' ':
                dat = dat[1:]
            if len(re.findall(':',dat))>1:
                dat = dat.split(' ')
                self.files += [file for file in dat if file !='']
            else:
                self.files.append(dat)
        self.insertLB()
    
    
    def insertLB(self):
        for file in self.files:
            fileName = os.path.split(file)[1]
            if fileName not in self.filePath.keys():
                self.filePath[fileName] = file
                self.fileLBox.insert(tk.END, fileName)


    def delFile(self):
        selctionIndex = self.fileLBox.curselection()
        if len(selctionIndex) != 1:
            return
        self.fileLBox.delete(selctionIndex)

    def createMail(self,name, dest, text,subj, files = None, link = None):
        msg = MIMEMultipart()
        msg['Subject'] = subj
        msg['To']      = dest
        msg.add_header('X-Unsent', '1')
        html = text
        html = '<font face="Verdana, monospace" size="10">'+ html
        if link:
            html += f'</div><a href = {link}>{link}</a>'
        html += f'Viele Grüße\n{self.controller.configData["Username"]}'
        html = html.replace('\n','<div>&nbsp;</div>')
        tml = html +'</font>'
        part = MIMEText(html, 'html')
        msg.attach(part)
        if files:
            for file in files:
                with open(file, 'rb') as f:
                    basename= os.path.basename(f)
                    part = MIMEApplication(f.read(),Name=basename)
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename
                msg.attach(part)
                
        outfile_name = f'{name}.eml'
        with open(outfile_name, 'w') as outfile:
            gen = generator.Generator(outfile)
            gen.flatten(msg)

            
##        
    def mail(self):
        pass
##        time.sleep(2)
##        selctionIndex = self.kontaktLBox.curselection()
##        if len(selctionIndex) != 1:
##            return
##        selectedPerson = self.kontaktLBox.get(selctionIndex[0])
##        adress, directory = self.kontakte[selectedPerson]
##        directory = directory.replace('\n','')
##        outlook = switch.switch('- Outlook')
##        navigate('rt')
##        time.sleep(1)
##        paste(adress)
##        tab(3)
##        paste(f'Neue Rechnung mit PE heute: {self.fileLBox.get(0)}')
##        tab(1)
##        rechnungstr = []
##        files = [os.path.split(f)[1] for f in self.files]
##        paste(f'''Hallo {selectedPerson},
##
##anbei ein Link zum Zahllaufordner wg. PE Rechnung {', '.join(files)}:\n\n''')
##        navigate('rzch1l')
##        time.sleep(0.1)
##        paste(directory)
##        ag.hotkey('enter')
##        ag.hotkey('enter')
##        paste('\nViele Grüße\n\nDavid')
##        navigate('rzcts')
##        down(3)
##        ag.hotkey('enter')
##        for file in self.files:
##            fname= os.path.split(file)[1]
##            move(file, f'{directory}\\{fname}')
##        self.files=[]
##        self.filePath = {}
##        self.fileLBox.delete(0, 'end')
##        os.startfile(directory)
##
