from MySQLdb import *
from flask import g

###################################
DB_IP = 'localhost'
DB_ID = "root"
DB_PW = "imlisgod"
###################################

#MySQL 서버에 로그인하고 연결하는 작업
def server_connect():
    db = connect(host=DB_IP , user=DB_ID, password=DB_PW, charset='utf8mb4')
    return db
#MySQL 서버에 로그인하고 모닥불 DB와 연결하는 작업
def db_connect():
    db = connect(host=DB_IP, user=DB_ID, password=DB_PW, db='modakbul', charset='utf8mb4', cursorclass=cursors.DictCursor)
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
    except Exception as ex:
        print("Db init Failed")
        print(ex)

    db.select_db('modakbul')
    #DB 테이블 생성
    with db.cursor() as cursor:
        sql = open("database/table/table_board.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_tag.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_user.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_user_tag.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_post.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_post_tag.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_post_comment.sql").read()
        cursor.execute(sql)
        #post_like는 유저가 삭제되도 라이크 유지시키려 했으나 프라이머리키를 해야해서 낫 널을 못시킴.
        sql = open("database/table/table_post_like.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_post_attach.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_vote.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_vote_tag.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_vote_content_type.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_vote_que.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_vote_select.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_vote_attach.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_account.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_account_tag.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_account_form.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_account_attach.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_view_post.sql").read()
        cursor.execute(sql)

    db.commit()
    db.close()




