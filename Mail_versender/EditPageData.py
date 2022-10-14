import tkinter as tk
from tkinter import messagebox
from Models import Kontakt,MailText
import re

class EditPage(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
        self.pageName = 'EditPage'
        self.controller = controller
        self.savedChanges = True
        self.bg = self.controller.configVars['EditPageColor']
        self.textMarkers = self.controller.configVars['TextMarkers']

        self.curText = None
        self.subjVar = tk.StringVar()
        self.textTitleVar = tk.StringVar()
##        self.controller.textChoices = self.controller.textChoices        
        self.curKontakt = None
##        self.controller.kontChoices = self.controller.kontChoices
        self.kontaktVar = tk.StringVar()
        
   
        boldFont=tk.font.Font(family = 'Verdana', weight = 'bold', size = 9) 				
        italicFont = tk.font.Font(family = 'Verdana', size = 9, slant = 'italic')
        underlinedFont = tk.font.Font(family = 'Verdana', size = 9, underline = 1)
        
        self.kontaktInfoFrame = tk.Frame(self, bg= self.bg)
        self.displayLab = tk.Label(self.kontaktInfoFrame,text = 'Title for this Contact:', bg= self.bg)
        self.personLab = tk.Label(self.kontaktInfoFrame,text = 'Name of the Contact:', bg= self.bg)
        self.mailLab = tk.Label(self.kontaktInfoFrame, text = 'E-Mail Adress of the Contact:', bg= self.bg)
##        self.displayVar = tk.StringVar()
##        self.displayEnt = tk.Entry(self.kontaktInfoFrame, textvariable = self.displayVar, width = 50)
        self.personVar = tk.StringVar()
        self.personEnt = tk.Entry(self.kontaktInfoFrame, textvariable = self.personVar,width = 50)
        self.mailVar = tk.StringVar()
        self.mailEnt = tk.Entry(self.kontaktInfoFrame, textvariable = self.mailVar,width = 50)
        self.attachFilesVar = tk.BooleanVar()
        self.attachFilesCheck = tk.Checkbutton(self.kontaktInfoFrame,text ='Attach files to mail', variable = self.attachFilesVar, bg = self.bg)
        self.dirVar = tk.StringVar()
        self.attachDirEnt = tk.Entry(self.kontaktInfoFrame, textvariable = self.dirVar,width = 50, disabledbackground = self.bg)
        self.attachDirVar = tk.StringVar()
        self.attachDirCheck = tk.Checkbutton(self.kontaktInfoFrame,
                                              text ='Save Files to Directory:',
                                              variable = self.attachDirVar,
                                              onvalue= 'normal', offvalue = 'disabled',
                                              command= lambda:self.attachDirEnt.configure(state = self.attachDirVar.get()),
                                              bg = self.bg)
        self.attachDirCheck.invoke()
        self.attachDirCheck.invoke()
        self.kontaktComb = tk.ttk.Combobox(self.kontaktInfoFrame, textvariable =self.kontaktVar, width = 47)
        self.kontaktComb['values'] = self.controller.kontChoices
        self.kontaktComb.bind('<<ComboboxSelected>>', self.selectKontakt)
        self.kontaktLab = tk.Label(self, text = 'Contact:', bg = self.bg)
        


##        self.sendMailFrame =tk.Frame(self, bg= self.bg)
##        self.sendMailVar = tk.BooleanVar()
##        self.Link = tk.Radiobutton(self.sendMailFrame,text ='Send Mail', variable = self.sendMailVar, value=True)
##        self.noLink = tk.Radiobutton(self.linkFrame,text ='', variable = self.sendMailVar, value=False)

        self.textFrame = tk.Frame(self, bg= self.bg)
        self.textCombo = tk.ttk.Combobox(self.textFrame, textvariable =self.textTitleVar, state = 'disabled')
        self.textCombo['values'] = self.controller.textChoices
        self.textCombo.bind('<<ComboboxSelected>>', self.displayText)
        self.textComboLab= tk.Label(self.textFrame, text = 'Chosen text:', bg = self.bg)
        self.textField = tk.Text(self.textFrame, width = 65, height = 15, wrap = 'none', font = tk.font.Font(family = 'Verdana', size = 9),state = 'disabled')
        self.textYScroll = tk.ttk.Scrollbar(self.textFrame, orient="vertical", command= self.textField.yview)
        self.textXScroll = tk.ttk.Scrollbar(self.textFrame, orient='horizontal', command= self.textField.xview)
        self.textField['yscrollcommand'] = self.textYScroll.set
        self.textField['xscrollcommand'] = self.textXScroll.set
        self.subDescLab = tk.Label(self.textFrame, text = 'Subject:', bg =self.bg)
        self.subjLab = tk.Label(self.textFrame,textvariable = self.subjVar ,width = 30,anchor = 'w', bg = self.bg)
        self.editTextBut = tk.Button(self.textFrame, text = 'Edit Text', command = self.editText, state = 'disabled')
        
        self.testSelectorComb = tk.ttk.Combobox(self, textvariable =self.kontaktVar)
        self.saveChangesBut = tk.Button(self, text = 'Save changes', command = self.saveChanges)
        self.returnBut = tk.Button(self, text = 'Return', command = lambda: self.controller.returnToPrev(self.savedChanges, self.pageName))
        Separator = tk.ttk.Separator(self, orient='horizontal')

            # text Tags
        self.textField.tag_configure("bold",font=boldFont)
        self.textField.tag_configure("italic",font=italicFont)
        self.textField.tag_configure("underlined",font=underlinedFont)

        

            # Grid:

##        self.kontaktLab.grid(row = 1,column = 3)
        self.returnBut.grid(row = 4, column = 1, pady = 5)
        
        self.kontaktInfoFrame.grid(row = 1, column = 1, columnspan= 4)
        #(
        self.displayLab.grid(row = 1, column = 1, sticky = 'w')
        self.kontaktComb.grid(row = 1,column = 2)
##        self.displayEnt.grid(row = 1, column = 2)
        self.personLab.grid(row = 2, column = 1, sticky = 'w')
        self.personEnt.grid(row = 2, column = 2)
        self.mailLab.grid(row = 3, column = 1, sticky = 'w')
        self.mailEnt.grid(row = 3, column = 2)
        self.attachDirCheck.grid(row = 4, column = 1, sticky = 'w')
        self.attachDirEnt.grid(row=4, column = 2)
        self.attachFilesCheck.grid(row =5, column = 1, sticky = 'w')
        #)
        Separator.grid(row =2, column = 1, columnspan = 4,pady = 15,padx = 5,sticky = ('E','W'))

        self.textFrame.grid(row = 3, column = 1, columnspan= 4,pady = 5)
        #
        self.textCombo.grid(row = 1, column = 2, sticky = 'we')
        self.textComboLab.grid(row = 1, column = 1,)
        self.editTextBut.grid(row = 1, column = 3,)
        self.subDescLab.grid(row = 2, column = 1)
        self.subjLab.grid(row = 2, column = 2, columnspan = 1, sticky = 'we')
        self.textField.grid(row = 3, column = 1, columnspan= 4, pady = 3, padx=5)
        #
        
        self.saveChangesBut.grid(row = 4, column = 3, columnspan = 2)

        

##        username = 'David'
##        
##        a = self.controller.cur.execute("SELECT * FROM Kontakte WHERE displayName =  :displayName " ,{'displayName': "David Rechnung"})
##        a = self.controller.cur.execute("SELECT * FROM Kontakte WHERE displayName =  ? ", ["David Rechnung"]
##        print(a.fetchall())
##                                        
    
    def onRaise(self):
        self.controller.root.title('Edit Contacts')
        self.controller.root.geometry(self.controller.configVars['EditPageDimensions'])
        self.bg= self.controller.configVars['EditPageColor']
        self.config(bg = self.bg)

    def update(self, textId,*args):
        pass
    
    def saveChanges(self):
        print('saved')
        self.savedChanges = True
        self.controller.showFrame('SelectorPage')
        
    def selectKontakt(self, selectionEvent):
        self.savedChanges= False
        kontaktName= self.kontaktComb.get()
        self.textCombo['state'] = 'normal'
        self.editTextBut['state'] = 'normal'
        if kontaktName != '<New Contact>':   
            self.curKontakt = self.controller.kontakte[kontaktName]
            self.curText = self.controller.texts[self.curKontakt.textId]
            self.textCombo.set(self.curText.title)
        else:
            self.curKontakt = Kontakt()
        
        self.displayText('event')
        if self.curKontakt.dir:
            self.attachDirCheck.select()
            self.attachDirEnt.configure(state = self.attachDirVar.get())
            self.dirVar.set(self.curKontakt.dir)
        else:
            self.attachDirCheck.deselect()
            self.attachDirEnt.configure(state = self.attachDirVar.get())
            self.dirVar.set('')
##        self.displayVar.set(self.curKontakt.display)
        self.personVar.set(self.curKontakt.person)
        self.mailVar.set(self.curKontakt.mail)
            
    def displayText(self, selectionEvent):
        self.textField['state']='normal'
        self.textField.delete('1.0', 'end')
        textName = self.textTitleVar.get()
        if textName == '':
            return
        if textName == '<New Text>':
            self.editText()
            return
        self.curText = self.controller.texts[self.controller.textIdByTitle[textName]]
        text = self.curText.text.replace(r'\n','\n')
        self.textField.insert('1.0',text)
        for marker, htmlMarkers in self.textMarkers.items():
            timesFound= len(re.findall(htmlMarkers[0], text))
            startAt = 'end'
            if timesFound:
                for i in range(timesFound):
                    endTag=self.textField.search(htmlMarkers[1], startAt, backwards= True)
                    startTag = self.textField.search(htmlMarkers[0], startAt, backwards= True)
                    self.textField.delete(endTag, f'{endTag}+{len(htmlMarkers[0])+1}c')
                    self.textField.delete(startTag, f'{startTag}+{len(htmlMarkers[1])-1}c')
                    endTag = endTag.split('.')
                    endTag = f'{endTag[0]}.{int(endTag[1])-len(htmlMarkers[0])}'
                    self.textField.tag_add(marker, startTag, endTag)
        self.textField['state']='disabled'
        self.subjVar.set(self.curText.subj)
    
    def editText(self):
        self.controller.setLastFrame(self.pageName)
        self.controller.showFrame('TextEditPage')
        pass
        
    
