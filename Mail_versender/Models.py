class Kontakt:
    def __init__(self):
        self.idNum = ''
        self.display = ''
        self.mail =''
        self.textId = ''
        self.dir = ''
        self.person = ''
    def fill(self, idNum, display, mail, textId, directory, person):
        self.idNum = idNum
        self.display = display
        self.mail =mail
        self.textId = textId
        self.dir = directory
        self.person = person
    
class MailText:
    def __init__(self):
        self.idNum = ''
        self.text = ''
        self.subj = ''
        self.title = ''
    def fill(self, idNum, text,subj,title):
        self.idNum = idNum
        self.text = text
        self.subj = subj
        self.title = title
