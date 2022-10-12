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
    def saveToBd(self, cursor):
        if idNum == '':
            cursor.execute(
                "Insert into MailTexte (text,subject,title) VALUES (:text,:subj,:title)",
                {'text':self.text, 'subj': self.subj, 'title':self.title}
                )
        else:
            idExist = cursor.execute('SELECT * FROM MailTexte WHERE id=?',(idNum))
            if idExidt:
                cursor.execute(
                    "UPDATE MailTexte SET text = :text, subject = :subj, title = :title WHERE id = :id",
                    {'id':self.idNum,'text':self.text, 'subj': self.subj, 'title':self.title}
                    )
            ###
            
            
