import tkinter as tk
from tkinter import messagebox
from Models import Kontakt,MailText

class FrameName(tk.Frame):
    def __init__(self,parent, controller):
        tk.Frame.__init__(self, parent)
        self.pageName = 'FrameName'
        self.controller = controller
        self.savedChanges = True
        


    def onRaise(self):
        self.controller.root.title('FrameName')
        self.controller.root.geometry(self.controller.configString['TextEditPageDimensions'])
        self.config(bg = self.controller.configString['TextEditPageColor'])

    def update(self, *args):
        pass
    def saveChanges(self):
        print('saved')
