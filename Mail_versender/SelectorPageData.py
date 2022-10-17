import tkinter as tk
import time
import os
import sqlite3
import json
from email import generator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from shutil import move
from tkinterdnd2 import DND_FILES, TkinterDnD
import re
from PyInstaller.utils.hooks import collect_data_files, eval_statement
datas = collect_data_files('tkinterdnd2')



class SelectorPage(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
        self.pageName = 'SelectorPage'
        self.controller = controller
        self.bg = self.controller.configVars['CreateMailColor']
        
        self.kontaktFrame = tk.Frame(self, bg = self.bg)
        self.kontChoices = list(self.controller.kontakts.keys())
        self.kontaktVar = tk.StringVar(value=self.kontChoices)
        self.kontaktLBox = tk.Listbox(self.kontaktFrame, listvariable = self.kontaktVar, height = 20, width =  30)
        self.kontaktLBox.bind('<Double-Button-1>',lambda e:self.editKontakts())
        self.kontaktYScroll = tk.ttk.Scrollbar(self.kontaktFrame, orient="vertical", command= self.kontaktLBox.yview)
        self.kontaktLBox['yscrollcommand'] = self.kontaktYScroll.set
        self.startBut= tk.Button(self, text = 'Create mail + move files', command = self.mail)
        self.drop_target_register(DND_FILES)
        
        self.files =[]
        self.dnd_bind('<<Drop>>',lambda e: self.cleanFiles(e.data))
        self.filePath = {}
        self.fileVar = tk.StringVar(value=self.files)
        self.fileLBox = tk.Listbox(self, listvariable = self.fileVar,width = 50, height = 20)
        self.fileLBox.bind('<Double-Button-1>',lambda e:self.delFile())
        self.editFrame = tk.Frame(self, bg = self.bg)
        self.editKontaktsBut = tk.Button(self.editFrame, text = 'Edit Contacts', command = self.editKontakts)
        self.editTextsBut = tk.Button(self.editFrame, text = 'Edit Texts', command = self.editTexts)

        #
        self.kontaktFrame.grid(row=1,column=1, pady = 5, padx = 5 )
        self.kontaktLBox.grid(row=1,column=1,)
        self.kontaktYScroll.grid(row = 1, column = 2, sticky = 'ns')
        #
        self.fileLBox.grid(row=1, column=2, )
        #
        self.editFrame.grid(row=2, column=1, sticky = 'w', padx =5)
        self.editKontaktsBut.grid(row=1, column=1,)
        self.editTextsBut.grid(row=1, column=2, padx= 2)
        #
        self.startBut.grid(row=2, column=2, sticky = 'e')
        

    def onRaise(self):
        self.controller.root.title('Create E-Mail')
        self.controller.root.config()
        self.controller.root.geometry(self.controller.configVars['CreateMailDimensions'])
        self.kontChoices = list(self.controller.kontakts.keys())
        self.kontaktVar.set(self.kontChoices)
        self.config(bg = self.bg)
         
    def update(self, *args):
        pass

    def editKontakts(self):
        selctionIndex = self.kontaktLBox.curselection()
        if len(selctionIndex) == 1:
            selectedKontakt = self.kontaktLBox.get(selctionIndex[0])
            kontakt = self.controller.kontakts[selectedKontakt]
            self.controller.frames['EditPage'].update(kontakt)
        self.controller.showFrame('EditPage')
        self.controller.setLastFrame(self.pageName)
            
    def editTexts(self):
        selctionIndex = self.kontaktLBox.curselection()
        if len(selctionIndex) == 1:
            selectedKontakt = self.kontaktLBox.get(selctionIndex[0])
            kontakt = self.controller.kontakts[selectedKontakt]
            self.controller.frames['TextEditPage'].update(kontakt)
        self.controller.showFrame('TextEditPage')
        self.controller.setLastFrame(self.pageName)

        
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

    def createMail(self, kontakt)#name, dest, text,subj, files = None, link = None):
        msg = MIMEMultipart()
        textMod = self.controller.texts[kontakt.textId]
        subj =  textMod.subj
        text = textMod.text
        person = kontakt.person
        link = f'<a href = {kontakt.directory}>{kontakt.directory}</a>'
        

##        html = text
####        html = '<strong>'+ html + '</strong>'
        html += f'Viele Grüße\n{self.controller.configData["Username"]}'
        html = html.replace('\n','<div>&nbsp;</div>')
        tml = html +'</font>'
        msg['Subject'] = subj
        msg['To']      = kontakt.mail
        msg.add_header('X-Unsent', '1')
        part = MIMEText(html, 'html')
        msg.attach(part)
        if kontakt.attach:
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
        selctionIndex = self.kontaktLBox.curselection()
        if len(selctionIndex) != 1:
            return
        selectedKontakt = self.kontaktLBox.get(selctionIndex[0])
        selectedKontakt = self.controller.kontakts[selectedKontakt]
        files = [os.path.split(f)[1] for f in self.files]
        self.createMail(selectedKontakt, files)
##        adress, directory = self.controller.kontakts[selectedPerson]
##        directory = directory.replace('\n','')
##        outlook = switch.switch('- Outlook')
##        navigate('rt')
##        time.sleep(1)
##        paste(adress)
##        tab(3)
##        paste(f'Neue Rechnung mit PE heute: {self.fileLBox.get(0)}')
##        tab(1)
##        rechnungstr = []
##        
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
