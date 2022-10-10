import tkinter as tk
from tkinter import messagebox
from Models import Kontakt,MailText
import re

class TextEditPage(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
        self.pageName = 'TextEditPage'
        self.controller = controller
        self.savedChanges = True
        self.bg = self.controller.configVars['TextEditPageColor']
        self.textBlocks =self.controller.configVars['TextBlock']
        
        self.textChoices = self.controller.textChoices
        self.textIdByTitle = self.controller.textIdByTitle
##        self.textVar = tk.StringVar()
        self.textTitleVar = tk.StringVar()

        self.selectFrame = tk.Frame(self, bg=self.bg)
        self.textCombo= tk.ttk.Combobox(self.selectFrame, textvariable =self.textTitleVar)
        self.textCombo['values'] = self.textChoices
        self.textCombo.bind('<<ComboboxSelected>>', self.displayText)
        self.textComboLab= tk.Label(self.selectFrame, text = 'Chosen text:', bg = self.bg)

        self.returnBut = tk.Button(self, command = lambda:self.controller.returnToPrev(self.savedChanges, self.pageName), text = 'Return')
        self.saveBut = tk.Button(self, command = self.saveChanges, text = 'Save Changes')
    
        self.textFrame = tk.Frame(self, bg=self.bg)
        self.textField = tk.Text(self.textFrame, width = 70, height = 15)
        self.textYScroll = tk.ttk.Scrollbar(self.textFrame, orient="vertical", command= self.textField.yview)
        self.textXScroll = tk.ttk.Scrollbar(self.textFrame, orient='horizontal', command= self.textField.xview)
        self.textField['yscrollcommand'] = self.textYScroll.set
        self.textField['xscrollcommand'] = self.textXScroll.set
        
        self.textLBoxChoices = [] #list(self.controller.configVars['TextBlock'].keys())
        self.textLBoxVar = tk.StringVar(value=self.textLBoxChoices)
        self.textLBox = tk.Listbox(self.textFrame, listvariable = self.textLBoxVar, width = 30)
        self.textLBox.bind('<Double-Button-1>', self.insertTextBlock)
        self.insertLBoxVals()
        
                
        self.returnBut.grid(row = 1, column = 1, padx = 5, pady =5)
        #
        self.selectFrame.grid(row = 1, column =2)
        self.textComboLab.grid(row = 1, column = 1)
        self.textCombo.grid(row = 1, column = 2)
        #
        self.textFrame.grid(row = 2, column = 1, columnspan = 4, padx = 5, pady =5)
        self.textField.grid(row =1, column = 1)
        self.textYScroll.grid(row = 1, column = 2, sticky = 'ns')
        self.textXScroll.grid(row = 2, column = 1, sticky = 'we')
        self.textLBox.grid(row = 1, column= 3, sticky = 'ns', padx = 5 )
        #
        self.saveBut.grid(row = 4,column=2, padx = 5, pady =5)
        

    def onRaise(self):
        self.controller.root.title('Edit Texts')
        self.controller.root.geometry(self.controller.configVars['TextEditPageDimensions'])
        self.config(bg = self.controller.configVars['TextEditPageColor'])
    
    def update(self, *args):
        pass

    def saveChanges(self):
        self.savedChanges = True
        print('saved')

    def insertLBoxVals(self):
        for key, vals in self.textBlocks.items():
            self.textLBox.insert('end', key)
            self.textLBox.itemconfig('end', background = vals[1])
    def insertTextBlock(self, event):
        selectedIndex = self.textLBox.curselection()

##        self.textField.
    def displayText(self, event):
        self.textField.delete('1.0', 'end')
        selectedText = self.textCombo.get()
        if selectedText == '<New Text>':
            selectedText = MailText()
        else:
            selectedText = self.controller.texts[self.textIdByTitle[selectedText]]
        text = selectedText.text.replace(r'\n','\n')
        self.textField.insert('1.0',text)
        for key, vals in self.textBlocks.items():
            timesFound= len(re.findall(vals[0], text))
            
            start = '1.0'
            if timesFound:
                for i in range(timesFound):
                    countVar= tk.StringVar()
                    search  = self.textField.search(vals[0],start, count= countVar)
                    endChar = f'{search}+{countVar.get()}c'
                    self.textField.tag_add(key, search, endChar)
                    start = endChar
                self.textField.tag_config(key, background = vals[1])
            



























        
        
