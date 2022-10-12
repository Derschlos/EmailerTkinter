import tkinter as tk
from tkinter import messagebox
from Models import Kontakt,MailText
import re
import tkinter.font

class TextEditPage(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
        self.pageName = 'TextEditPage'
        self.controller = controller
        self.savedChanges = True
        self.bg = self.controller.configVars['TextEditPageColor']
        self.textBlocks =self.controller.configVars['TextBlock']
        self.selectedText = None
        
        self.textChoices = self.controller.textChoices
        self.textIdByTitle = self.controller.textIdByTitle
        self.textSubjVar = tk.StringVar()
        self.textTitleVar = tk.StringVar()

        self.selectFrame = tk.Frame(self, bg=self.bg)
        self.textCombo= tk.ttk.Combobox(self.selectFrame, textvariable =self.textTitleVar)#, width = 50)
        self.textCombo['values'] = self.textChoices
        self.textCombo.bind('<<ComboboxSelected>>', self.displayText)
        self.textComboLab= tk.Label(self.selectFrame, text = 'Title:', bg = self.bg)
        self.textSubjLab = tk.Label(self.selectFrame, text = 'Subject', bg = self.bg)
        self.textSubjEnt = tk.Entry(self.selectFrame, textvariable = self.textSubjVar)

        self.returnBut = tk.Button(self, command = lambda:self.controller.returnToPrev(self.savedChanges, self.pageName), text = 'Return')
        self.saveBut = tk.Button(self, command = self.saveChanges, text = 'Save Changes', state='disabled')
    
        self.textFrame = tk.Frame(self, bg=self.bg)
        self.textField = tk.Text(self.textFrame, width = 70, height = 15, wrap = 'none')
        self.textYScroll = tk.ttk.Scrollbar(self.textFrame, orient="vertical", command= self.textField.yview)
        self.textXScroll = tk.ttk.Scrollbar(self.textFrame, orient='horizontal', command= self.textField.xview)
        self.textField['yscrollcommand'] = self.textYScroll.set
        self.textField['xscrollcommand'] = self.textXScroll.set
        self.textBoldBut = tk.Button(self.textFrame, text = 'B', font ='bold', command =self.bolder)
        
        self.textLBoxChoices = [] #list(self.controller.configVars['TextBlock'].keys())
        self.textLBoxVar = tk.StringVar(value=self.textLBoxChoices)
        self.textLBox = tk.Listbox(self.textFrame, listvariable = self.textLBoxVar, width = 30)
        self.textLBox.bind('<Double-Button-1>', self.insertTextBlock)
        self.insertLBoxVals()

        bold_font=tk.font.Font(self.textField,self.textField.cget("font"))   #my_text is text box variable name 
        bold_font.configure(weight="bold")					
        self.textField.tag_configure("bold",font=bold_font)
                
        self.returnBut.grid(row = 1, column = 1, padx = 5, pady =7)
        #
        self.selectFrame.grid(row = 1, column =2, padx = 5, columnspan = 6)
        self.textComboLab.grid(row = 1, column = 1)
        self.textCombo.grid(row = 1, column = 2,sticky = 'we')
        self.textSubjLab.grid(row = 2, column = 1)
        self.textSubjEnt.grid(row = 2, column = 2,sticky = 'we')
        #
        self.textFrame.grid(row = 2, column = 1, columnspan = 4, padx = 5, pady =5)
        self.textField.grid(row =1, column = 1)
        self.textYScroll.grid(row = 1, column = 2, sticky = 'ns')
        self.textXScroll.grid(row = 2, column = 1, sticky = 'we')
        self.textLBox.grid(row = 1, column= 3, sticky = 'ns', padx = 5 )
        self.textBoldBut.grid(row = 3, column= 1, padx = 5 )
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
        subj = self.textSubjEnt.get()
        title= self.textCombo.get()
        text = self.textField.get('1.0','end')
        text = text.replace('\n', r'\n')
        boldRanges = self.textField.tag_ranges('bold')
        if boldRanges:
            for i in range(len(boldRanges),0,-2):
                self.textField.insert(boldRanges[i-1],'</b>')
                self.textField.insert(boldRanges[i-2],'<b>') 
                
##        self.selectedText.saveToBd(self.controller.cur)

        print('saved')

    def insertLBoxVals(self):
        for key, vals in self.textBlocks.items():
            self.textLBox.insert('end', key)
            self.textLBox.itemconfig('end', background = vals[1])
            self.textField.tag_config(key, background = vals[1])
            
     
    def insertTextBlock(self, event):
        selectedIndex = self.textLBox.curselection()
        selection = self.textLBox.get(selectedIndex)
        insertIndex=tk.INSERT
        self.textField.insert(tk.INSERT, self.textBlocks[selection][0])
        self.textField.tag_add(selection, f'{insertIndex}-{len(self.textBlocks[selection][0])}c',insertIndex)
        

    def displayText(self, event):
        self.textField.delete('1.0', 'end')
        self.saveBut['state'] = 'normal'
        self.selectedText = self.textCombo.get()
        if self.selectedText== '<New Text>':
            self.selectedText = MailText()
        else:
            self.selectedText = self.controller.texts[self.textIdByTitle[self.selectedText]]
        text = self.selectedText.text.replace(r'\n','\n')
        self.textField.insert('1.0',text)
        textMarkers = {'bold':['<b>','</b>'],'italic': ['<i>','</i>']}
        for key,vals in textMarkers.items():
            timesFound= len(re.findall(vals[0], text))
            startAt = 'end'
            if timesFound:
                for i in range(timesFound):
                    endTag=self.textField.search(vals[1], startAt, backwards= True)
                    startTag = self.textField.search(vals[0], startAt, backwards= True)
                    self.textField.delete(endTag, f'{endTag}+{len(vals[0])+1}c')
                    self.textField.delete(startTag, f'{startTag}+{len(vals[1])-1}c')
                    endTag = endTag.split('.')
                    endTag = f'{endTag[0]}.{int(endTag[1])-len(vals[0])}'
                    self.textField.tag_add(key, startTag, endTag)
        self.textSubjEnt.delete(0, 'end')
        self.textSubjEnt.insert(0, self.selectedText.subj)
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
##                self.textField.tag_config(key, background = vals[1])
            

    def bolder(self):
        current_tags=self.textField.tag_names("sel.first")
        if "bold" in current_tags:
            self.textField.tag_remove("bold","sel.first","sel.last")#my_text,my_text.cget
        else:
            self.textField.tag_add("bold","sel.first","sel.last")

        print(self.textField.tag_ranges('bold'))
        a = self.textField.tag_ranges('bold')
        print(self.textField.get('1.0'))
        print(self.textField.count('1.0',a[0]))
        b =self.textField.count('1.0',a[0])
        print(self.textField.get('1.0', 'end')[:b[0]])
        
##        print(self.textField.index('end'))

##























        
        
