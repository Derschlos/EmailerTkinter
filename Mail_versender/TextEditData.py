import tkinter as tk
from tkinter import messagebox
from Models import Kontakt,MailText

class TextEditPage(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
        self.pageName = 'TextEditPage'
        self.controller = controller
        self.savedChanges = True
        


    def onRaise(self):
        self.controller.root.title('Edit Texts')
        self.controller.root.geometry(self.controller.configString['TextEditPageDimensions'])
        self.config(bg = self.controller.configString['TextEditPageColor'])

    def update(self, *args):
        pass

    def returnToPrev(self):
        if self.savedChanges == False:
            message = messagebox.askyesnocancel(message = 'Do you want to save any changes?')
            if message == None:
                return
            elif message == True:
                self.saveChanges()
            else:
                self.savedChanges = True
                
        self.controller.showFrame(self.controller.lastFrame)
