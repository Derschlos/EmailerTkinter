class Kontakt:
    def __init__(self):
        self.idNum = ''
        self.display = ''
        self.mail =''
        self.textId = ''
        self.dir = ''
        self.person = ''
        self.attach = 0
        self.addInfo = ''
    def fill(self, idNum, display, mail, textId, directory, person, attach,addInfo):
        self.idNum = idNum
        self.display = display
        self.mail =mail
        self.textId = textId
        self.dir = directory
        self.person = person
        self.attach = attach
        self.addInfo = addInfo
    def saveToDB(self, connection):
        cursor = connection.cursor()
        if self.idNum == '':
            cursor.execute(
                "Insert into Kontakte (displayName,mail,textId,directory,personName,attachFiles,addInfo) VALUES (:displayName,:mail,:textId,:directory,:personName,:attachFiles,:addInfo)",
                {'displayName':self.display,
                 'mail': self.mail,
                 'textId':self.textId,
                 'directory':self.dir,
                 'personName':self.person,
                 'attachFiles':self.attach,
                 'addInfo':self.addInfo}
                )
            idNum = cursor.execute('SELECT MAX(id) from Kontakte').fetchone()[0]
            self.idNum = idNum
            connection.commit()
            return idNum
        else:
            idExist = cursor.execute('SELECT * FROM Kontakte WHERE id=:id',{'id':str(self.idNum)})
            if idExist:
                cursor.execute(
                    "UPDATE Kontakte SET displayName = :displayName, mail = :mail, textId = :textId, directory = :directory, personName = :personName, attachFiles = :attachFiles, addInfo = :addInfo WHERE id = :id",
                    {'id':str(self.idNum),
                     'displayName':self.display,
                     'mail': self.mail,
                     'textId':self.textId,
                     'directory':self.dir,
                     'personName':self.person,
                     'attachFiles':self.attach,
                     'addInfo':self.addInfo}
                    )
                connection.commit()
    def delete(self, connection):
        cursor = connection.cursor()
        if self.idNum:
            cursor.execute("DELETE FROM Kontakte WHERE id= :id",{"id": str(self.idNum)})
        connection.commit()
    
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
            connection.commit()
            return idNum
        else:
            idExist = cursor.execute('SELECT * FROM MailTexte WHERE id=:id',{'id':str(self.idNum)})
            if idExist:
                cursor.execute(
                    "UPDATE MailTexte SET text = :text, subject = :subj, title = :title WHERE id = :id",
                    {'id':str(self.idNum),'text':self.text, 'subj': self.subj, 'title':self.title}
                    )
        connection.commit()
            ###
    def delete(self, connection):
        cursor = connection.cursor()
        if self.idNum:
            cursor.execute("DELETE FROM MailTexte WHERE id=:id",{"id": str(self.idNum)})
        connection.commit()       
            
