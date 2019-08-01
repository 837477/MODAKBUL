from MySQLdb import *
from flask import g
from global_func import *

###################################
DB_IP = 'localhost'
DB_ID = "root"
DB_PW = "imlisgod"
###################################

def get_db():
    if 'db' not in g:
        g.db = connect(host=DB_IP, user=DB_ID, password=DB_PW, db='modakbul', charset='utf8mb4', cursorclass=cursors.DictCursor)

def close_db():
    db = g.pop('db', None)
    if db is not None:
        if db.open:
            db.close()

def init_db():
    #DB연결
    db = connect(host=DB_IP , user=DB_ID, password=DB_PW, charset='utf8mb4', cursorclass=cursors.DictCursor)
    
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
        sql = open("database/table/table_post_like.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_post_attach.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_vote.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_vote_que.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_vote_select.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_vote_user_answer.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_view_post.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_variable.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_department.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_log.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_today_visitor.sql").read()
        cursor.execute(sql)
        sql = open("database/table/table_everyday_analysis.sql").read()
        cursor.execute(sql)
        #sql = open("database/init_database.sql").read()
        #cursor.execute(sql) 

    db.commit()
    db.close()




