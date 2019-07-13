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

def get_db():
    if 'db' not in g:
        g.db = db_connect()

def close_db():
    db = g.pop('db', None)
    if db is not None:
        if db.open:
            db.close()

def init_db():
    #DB연결
    db = server_connect()
    
    #DB 생성
    try:
        with db.cursor() as cursor:
            sql = "CREATE DATABASE IF NOT EXISTS modakbul"
            cursor.execute(sql)
        db.commit()
    except:
        print("DB init Failed")

    db.select_db('modakbul')
    #DB 테이블 생성
    with db.cursor() as cursor:
        sql = open("database/table/table_user.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_notice.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_post.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_attachments.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_user_like.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_comment.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_blacklist.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_vote_title.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_vote_content.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_vote_select.sql").read()
        cursor.execute(sql)
    db.commit()
    db.close()


