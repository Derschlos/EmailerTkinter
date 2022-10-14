class Kontakt:
    def __init__(self):
        self.idNum = ''
        self.display = ''
        self.mail =''
        self.textId = ''
        self.dir = ''
        self.person = ''
        self.attach = 0
    def fill(self, idNum, display, mail, textId, directory, person, attach):
        self.idNum = idNum
        self.display = display
        self.mail =mail
        self.textId = textId
        self.dir = directory
        self.person = person
        self.attach = attach
    
    
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
    def saveToDB(self, connection):
        cursor = connection.cursor()
        if self.idNum == '':
            cursor.execute(
                "Insert into MailTexte (text,subject,title) VALUES (:text,:subj,:title)",
                {'text':self.text, 'subj': self.subj, 'title':self.title}
                )
            idNum = cursor.execute('SELECT MAX(id) from MailTexte').fetchone()[0]
            self.idNum = idNum
            return idNum
        else:
            idExist = cursor.execute('SELECT * FROM MailTexte WHERE id=?',(str(self.idNum)))
            if idExist:
                cursor.execute(
                    "UPDATE MailTexte SET text = :text, subject = :subj, title = :title WHERE id = :id",
                    {'id':self.idNum,'text':self.text, 'subj': self.subj, 'title':self.title}
                    )
        connection.commit()
            ###
            
            
