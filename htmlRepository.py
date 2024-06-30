import db_auth as db_auth
import pymysql.cursors  # python과 mysql(mariadb) 연동
## 일주일에 한 번 씩 실행될 것임. ##

class HtmlRepository:
    def __init__(self) -> None:
        self.login = db_auth.db_login

    def getConnection(self):
        self.connection = pymysql.connect(host=self.login['host'],
                                     user=self.login['user'],
                                     password=self.login['password'],
                                     db=self.login['db'],
                                     charset=self.login['charset'],
                                     cursorclass=pymysql.cursors.DictCursor)

    def closeConnection(self):
        self.connection.close()

    # 원본 html 저장
    def saveOriginalHtml(self, documentNumber, html):  
        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        sql = "INSERT INTO original(document_number, html) VALUES(%s, %s)"
        cursor.execute(sql, (documentNumber, html))

        self.connection.commit() # 쿼리 적용
        self.connection.close() # db 연결해제

    # 번역본 html 저장
    def saveTranslateHtml(self, documentNumber, html):  
        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        cursor.execute(
            "INSERT INTO translated(document_number, content) VALUES(%s, %s)" % (documentNumber, html))

        self.connection.commit() # 쿼리 적용
        self.connection.close() # db 연결해제

    # 원본 html 가져오기
    def getOriginalHtml(self, number):
        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        cursor.execute(
            "INSERT INTO original(number, content) VALUES('%s', '%s')" % (number))

        self.connection.commit() # 쿼리 적용
        self.connection.close() # db 연결해제
        return ""

    # 번역본 html 가져오기
    def getTranslatedHtml(self, number):
        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        cursor.execute(
            "INSERT INTO original(number, content) VALUES('%s', '%s')" % (number))

        self.connection.commit() # 쿼리 적용
        self.connection.close() # db 연결해제
        return ""

    # 존재하는지    
    def isExist(self, number):
        self.getConnection() # db 연결
        cursor = self.connection.cursor() # control structure of database SQL 문장을 DB 서버에 전송하기 위한 객체

        cursor.execute(
            "SELECT EXISTS (SELECT 1 FROM original WHERE document_number = '%s') AS is_exist" % (number))

        self.connection.commit() # 쿼리 적용
        self.connection.close() # db 연결해제
        return ""

