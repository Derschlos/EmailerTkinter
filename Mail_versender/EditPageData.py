import tkinter as tk
from tkinter import messagebox
from Models import Kontakt,MailText

class EditPage(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
        self.pageName = 'EditPage'
        self.controller = controller
        self.savedChanges = True
        self.bg = self.controller.configVars['EditPageColor']
        self.curKontakt = None
        self.kontakte = self.controller.kontakte
        self.texts = self.controller.texts
        self.kontChoices = self.controller.kontChoices
        self.kontaktVar = tk.StringVar()
        self.kontaktComb = tk.ttk.Combobox(self, textvariable =self.kontaktVar)
        self.kontaktComb['values'] = self.kontChoices
        self.kontaktComb.bind('<<ComboboxSelected>>', self.selectKontakt)
        self.kontaktLab = tk.Label(self, text = 'Contact:', bg = self.bg)
        
        self.kontaktInfoFrame = tk.Frame(self, bg= self.bg)
        self.displayLab = tk.Label(self.kontaktInfoFrame,text = 'Title for this Contact:', bg= self.bg)
        self.personLab = tk.Label(self.kontaktInfoFrame,text = 'Name of the Contact:', bg= self.bg)
        self.mailLab = tk.Label(self.kontaktInfoFrame, text = 'E-Mail Adress of the Contact:', bg= self.bg)
        self.displayVar = tk.StringVar()
        self.displayEnt = tk.Entry(self.kontaktInfoFrame, textvariable = self.displayVar, width = 50)
        self.personVar = tk.StringVar()
        self.personEnt = tk.Entry(self.kontaktInfoFrame, textvariable = self.personVar,width = 50)
        self.mailVar = tk.StringVar()
        self.mailEnt = tk.Entry(self.kontaktInfoFrame, textvariable = self.mailVar,width = 50)

        self.textFrame = tk.Frame(self, bg= self.bg)
        self.curText = None
        self.textVar = tk.StringVar()
        self.textTitleVar = tk.StringVar()
        self.textChoices = self.controller.textChoices
        self.textIdByTitle = self.controller.textIdByTitle
        self.textCombo = tk.ttk.Combobox(self.textFrame, textvariable =self.textTitleVar, state = 'disabled')
        self.textCombo['values'] = self.textChoices
        self.textCombo.bind('<<ComboboxSelected>>', self.displayText)
        self.textComboLab= tk.Label(self.textFrame, text = 'Chosen text:', bg = self.bg)
        self.textDisplay = tk.Label(self.textFrame,textvariable = self.textVar ,width = 65, height = 15,justify = 'left',anchor = ('nw'))
        self.editTextBut = tk.Button(self.textFrame, text = 'Edit Text', command = self.editText, state = 'disabled')
        
        self.testSelectorComb = tk.ttk.Combobox(self, textvariable =self.kontaktVar)
        self.saveChangesBut = tk.Button(self, text = 'Save changes', command = self.saveChanges)
        self.returnBut = tk.Button(self, text = 'Return', command = lambda: self.controller.returnToPrev(self.savedChanges, self.pageName))
        Separator = tk.ttk.Separator(self, orient='horizontal')
        

##      Grid:
        self.kontaktComb.grid(row = 1,column = 4)
        self.kontaktLab.grid(row = 1,column = 3)
        self.returnBut.grid(row = 1, column = 1, pady = 5)
        
        self.kontaktInfoFrame.grid(row = 2, column = 1, columnspan= 4)
        #(
        self.displayLab.grid(row = 1, column = 1, sticky = 'w')
        self.displayEnt.grid(row = 1, column = 2)
        self.personLab.grid(row = 2, column = 1, sticky = 'w')
        self.personEnt.grid(row = 2, column = 2)
        self.mailLab.grid(row = 3, column = 1, sticky = 'w')
        self.mailEnt.grid(row = 3, column = 2)
        #)
        Separator.grid(row =3, column = 1, columnspan = 4,pady = 15,padx = 5,sticky = ('E','W'))

        self.textFrame.grid(row = 4, column = 1, columnspan= 4,pady = 5)
        #
        self.textCombo.grid(row = 1, column = 2,)
        self.textComboLab.grid(row = 1, column = 1,)
        self.editTextBut.grid(row = 1, column = 3,)
        self.textDisplay.grid(row = 2, column = 1, columnspan= 4, pady = 3, padx=5)
        #
        
        self.saveChangesBut.grid(row = 5, column = 1, columnspan = 4)

        

##        username = 'David'
##        
##        a = self.controller.cur.execute("SELECT * FROM Kontakte WHERE displayName =  :displayName " ,{'displayName': "David Rechnung"})
##        a = self.controller.cur.execute("SELECT * FROM Kontakte WHERE displayName =  ? ", ["David Rechnung"]
##        print(a.fetchall())
##                                        
    
    def onRaise(self):
        self.controller.root.title('Edit Contacts')
        self.controller.root.geometry(self.controller.configVars['EditPageDimensions'])
        self.config(bg = self.controller.configVars['EditPageColor'])

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
            self.curKontakt = self.kontakte[kontaktName]
            self.curText = self.texts[self.curKontakt.textId]
            self.textCombo.set(self.curText.title)
        else:
            self.curKontakt = Kontakt()
            
        self.displayText('event')
        self.displayVar.set(self.curKontakt.display)
        self.personVar.set(self.curKontakt.person)
        self.mailVar.set(self.curKontakt.mail)
            
    def displayText(self, selectionEvent):
        textName = self.textTitleVar.get()
        if textName == '':
            return
        if textName == '<New Text>':
            self.editText()
            return
        curTextId = self.textIdByTitle[textName]
        self.curText = self.texts[curTextId]
        self.textVar.set(self.curText.text.replace(r'\n', '\n'))
    
    def editText(self):
        self.controller.setLastFrame(self.pageName)
        self.controller.showFrame('TextEditPage')
        pass
        
    
