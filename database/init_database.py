from MySQLdb import connect
from flask import g

IP = 'localhost'
ID = "root"
PW = "imlisgod"

#MySQL 서버에 로그인하고 연결하는 작업
def server_connect():
    db = connect(host=IP , user=ID, password=PW, charset='utf8mb4')
    return db
#MySQL 서버에 로그인하고 모닥불 DB와 연결하는 작업
def db_connect():
    db = connect(host=IP, user=ID, password=PW, db='modakbul', charset='utf8mb4')
    return db

def init_db():
    #DB연결
    db = server_connect()
    
    #DB 생성
    try:
        with db.cursor() as cursor:
            query = "CREATE DATABASE IF NOT EXISTS modakbul"
            cursor.execute(query)
        db.commit()
    except:
        print("DB init Failed")

    #DB 테이블 생성
    #with db.cursor() as cursor:
    db.close()


