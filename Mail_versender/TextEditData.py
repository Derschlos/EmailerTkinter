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
        boldFont=tk.font.Font(family = 'Verdana', weight = 'bold', size = 9) 				
        italicFont = tk.font.Font(family = 'Verdana', size = 9, slant = 'italic')
        underlinedFont = tk.font.Font(family = 'Verdana', size = 9, underline = 1)
        self.textMarkers = {'bold':['<b>','</b>'],'italic': ['<i>','</i>'],'underlined':['<u>','</u>']}


        self.selectFrame = tk.Frame(self, bg=self.bg)
        self.textCombo= tk.ttk.Combobox(self.selectFrame, textvariable =self.textTitleVar, width = 49)
        self.textCombo['values'] = self.textChoices
        self.textCombo.bind('<<ComboboxSelected>>', self.displayText)
        self.textComboLab= tk.Label(self.selectFrame, text = 'Title:', bg = self.bg)
        self.textSubjLab = tk.Label(self.selectFrame, text = 'Subject', bg = self.bg)
        self.textSubjEnt = tk.Entry(self.selectFrame, textvariable = self.textSubjVar, width = 49)
        self.saveBut = tk.Button(self.selectFrame, command = self.saveChanges, text = 'Save Changes', state='disabled')
##        self.spacerLab = tk.Label(self.selectFrame, text = '', bg = self.bg, width = 10)


        self.returnBut = tk.Button(self, command = lambda:self.controller.returnToPrev(self.savedChanges, self.pageName), text = 'Return')
        
        self.textFrame = tk.Frame(self, bg=self.bg)
        self.textField = tk.Text(self.textFrame, width = 70, height = 15, wrap = 'none', font = tk.font.Font(family = 'Verdana', size = 10))
        self.textYScroll = tk.ttk.Scrollbar(self.textFrame, orient="vertical", command= self.textField.yview)
        self.textXScroll = tk.ttk.Scrollbar(self.textFrame, orient='horizontal', command= self.textField.xview)
        self.textField['yscrollcommand'] = self.textYScroll.set
        self.textField['xscrollcommand'] = self.textXScroll.set
        
        self.tagFrame = tk.Frame(self.textFrame, bg = self.bg)
        self.textBoldBut = tk.Button(self.tagFrame, text = 'B', font =boldFont, command =lambda:self.tagger('bold'))
        self.textItalBut = tk.Button(self.tagFrame, text = 'I', font =italicFont, command =lambda:self.tagger('italic'))
        self.textUnderBut = tk.Button(self.tagFrame, text = 'U', font =underlinedFont, command =lambda:self.tagger('underlined'))

        self.textLBoxChoices = [] #list(self.controller.configVars['TextBlock'].keys())
        self.textLBoxVar = tk.StringVar(value=self.textLBoxChoices)
        self.textLBox = tk.Listbox(self.textFrame, listvariable = self.textLBoxVar, width = 30)
        self.textLBox.bind('<Double-Button-1>', self.insertTextBlock)
        self.insertLBoxVals()

        
        self.textField.tag_configure("bold",font=boldFont)
        self.textField.tag_configure("italic",font=italicFont)
        self.textField.tag_configure("underlined",font=underlinedFont)



                
        self.returnBut.grid(row = 1, column = 1, padx = 5, pady =5)
        #
        self.selectFrame.grid(row = 1, column =3, padx = 5, columnspan = 3)
        self.textComboLab.grid(row = 1, column = 1)
        self.textCombo.grid(row = 1, column = 2, pady = 5, sticky = 'we', padx = 10 )
##        self.spacerLab.grid(row = 1, column = 8)
        self.textSubjLab.grid(row = 2, column = 1)
        self.textSubjEnt.grid(row = 2, column = 2,columnspan =1, sticky = 'we', padx = 10 )
        self.saveBut.grid(row = 1,column=3, padx = 50, pady =0, rowspan = 2,columnspan = 2)
        #
        self.textFrame.grid(row = 2, column = 1, columnspan = 3, padx = 5, pady =5)
        self.textField.grid(row =1, column = 1, rowspan = 15)
        self.textYScroll.grid(row = 1, column = 2, sticky = 'ns',rowspan = 16)
        self.textXScroll.grid(row = 16, column = 1, sticky = 'we')
        self.textLBox.grid(row = 2, column= 3, sticky = 'ns', padx = 5,rowspan = 15)
        #
        self.tagFrame.grid(row = 1, column= 3)
        self.textBoldBut.grid(row = 1, column= 1, padx = 1)
        self.textItalBut.grid(row = 1, column= 2, padx = 1)
        self.textUnderBut.grid(row = 1, column= 3, padx = 1)

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
        for marker, htmlMarkers in self.textMarkers.items():
            ranges = self.textField.tag_ranges(marker)
            if ranges:
                for i in range(len(ranges),0,-2):
                    self.textField.insert(ranges[i-1],htmlMarkers[1])
                    self.textField.insert(ranges[i-2],htmlMarkers[0])
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
        self.textSubjEnt.delete(0, 'end')
        self.textSubjEnt.insert(0, self.selectedText.subj)
        for title, placeholder in self.textBlocks.items():
            timesFound= len(re.findall(placeholder[0], text))
            start = '1.0'
            if timesFound:
                for i in range(timesFound):
                    countVar= tk.StringVar()
                    search  = self.textField.search(placeholder[0],start, count= countVar)
                    endChar = f'{search}+{countVar.get()}c'
                    self.textField.tag_add(title, search, endChar)
                    start = endChar
##                self.textField.tag_config(key, background = vals[1])
            
    def tagger(self, tagName):
        current_tags=self.textField.tag_names("sel.first")
        if f"{tagName}" in current_tags:
            self.textField.tag_remove(f"{tagName}","sel.first","sel.last")
        else:
            self.textField.tag_add(f"{tagName}","sel.first","sel.last")



    
##    def bolder(self):
####        if not self.textField.sel:
####            return
##        current_tags=self.textField.tag_names("sel.first")
##        if "bold" in current_tags:
##            self.textField.tag_remove("bold","sel.first","sel.last")#my_text,my_text.cget
##        else:
##            self.textField.tag_add("bold","sel.first","sel.last")
##
##    def italicer(self):
##        current_tags=self.textField.tag_names("sel.first")
##        if "italic" in current_tags:
##            self.textField.tag_remove("italic","sel.first","sel.last")#my_text,my_text.cget
##        else:
##            self.textField.tag_add("italic","sel.first","sel.last")
####        print(self.textField.tag_ranges('bold'))
####        a = self.textField.tag_ranges('bold')
####        print(self.textField.get('1.0'))
####        print(self.textField.count('1.0',a[0]))
####        b =self.textField.count('1.0',a[0])
####        print(self.textField.get('1.0', 'end')[:b[0]])
####        
####        print(self.textField.index('end'))
##
####























        
        
