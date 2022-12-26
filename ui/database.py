import pymysql


def database_connection():
    try:
        conn = pymysql.connect(host='localhost', user='root', password='mysql')
        mycursor = conn.cursor()
    except:
        print("fail to connect database, please try again")
        return

    try:
        query = 'create database sign_language'
        mycursor.execute(query)
        query = 'use sign_language'
        mycursor.execute(query)
    except:
        query = 'use sign_language'
        mycursor.execute(query)
    return conn


conn = database_connection()


def close_database():
    conn.close()


def login(email, password):
    cur = conn.cursor()
    try:
        query = 'create table user(id int auto_increment primary key not null, email varchar(50) not null, password varchar(100) not null)'
        cur.execute(query)
    except:
        pass

    try:
        query = 'select id from user where email=%s and password=%s'
        cur.execute(query, (email, password))
        row = cur.fetchone()
        if row == None:
            return -1
        return row[0]
    except:
        return -1
    #false ve -1
    # true ve id

def insert_user(email, password):
    cur = conn.cursor()
    try:
        query = 'create table user(id int auto_increment primary key not null, email varchar(50) not null, password varchar(100) not null)'
        cur.execute(query)
    except:
        pass

    try:
        query = 'insert into user(email, password) values(%s,%s)'
        cur.execute(query, (email, password))
        conn.commit()
        return 1
    except:
        return -1

def change_path_trans(id, path):
    cur = conn.cursor()
    try:
        query = 'create table translation(id int auto_increment primary key not null, path varchar(100) not null, meaning nvarchar(200), user_id int not null, foreign key (user_id) references user(id), created_time datetime)'
        cur.execute(query)
    except:
        pass

    try:
        query = 'update translation set path = %s where id = %s'
        cur.execute(query, (path, id))
        conn.commit()
        return 1
    except:
        return -1


def change_meaning_trans(id, meaning):
    cur = conn.cursor()
    try:
        query = 'create table translation(id int auto_increment primary key not null, path varchar(100) not null, meaning nvarchar(200), user_id int not null, foreign key (user_id) references user(id), created_time datetime)'
        cur.execute(query)
    except:
        pass

    try:
        query = 'update translation set meaning = %s where id = %s'
        cur.execute(query, (meaning, id))
        conn.commit()
        return 1
    except:
        return -1

def insert_translation(path, meaning, user_id):
    cur = conn.cursor()
    try:
        query = 'create table translation(id int auto_increment primary key not null, path varchar(100) not null, meaning nvarchar(200), user_id int not null, foreign key (user_id) references user(id), created_time datetime)'
        cur.execute(query)
    except:
        pass

    try:
        query = 'insert into translation(path, meaning, user_id, created_time) values(%s, %s, %s, NOW())'
        cur.execute(query, (path, meaning, user_id))
        conn.commit()
        return 1
    except:
        return -1


def delete_translation(id):
    cur = conn.cursor()
    try:
        query = 'create table translation(id int auto_increment primary key not null, path varchar(100) not null, meaning nvarchar(200), user_id int not null, foreign key (user_id) references user(id), created_time datetime)'
        cur.execute(query)
    except:
        pass

    try:
        query = 'delete from translation where id = %s'
        cur.execute(query, id)
        conn.commit()
        return 1
    except:
        return -1


def get_all_translations():
    cur = conn.cursor()
    try:
        query = 'create table translation(id int auto_increment primary key not null, path varchar(100) not null, meaning nvarchar(200), user_id int not null, foreign key (user_id) references user(id), created_time datetime)'
        cur.execute(query)
    except:
        pass

    try:
        query = 'select * from translation order by created_time desc'
        cur.execute(query)
        row = cur.fetchall()
        return row
    except:
        return None


def get_translation(id):
    cur = conn.cursor()
    try:
        query = 'create table translation(id int auto_increment primary key not null, path varchar(100) not null, meaning nvarchar(200), user_id int not null, foreign key (user_id) references user(id), created_time datetime)'
        cur.execute(query)
    except:
        pass

    try:
        query = 'select * from translation where id = %s'
        cur.execute(query, id)
        row = cur.fetchone()
        return row
    except:
        return None



def change_path_fav(id, path):
    cur = conn.cursor()
    try:
        query = 'create table favourite(id int auto_increment primary key not null, path varchar(100) not null, meaning nvarchar(200), user_id int not null, foreign key (user_id) references user(id))'
        cur.execute(query)
    except:
        pass

    try:
        query = 'update favourite set path = %s where id = %s'
        cur.execute(query, (path, id))
        conn.commit()
        return 1
    except:
        return -1


def change_meaning_fav(id, meaning):
    cur = conn.cursor()
    try:
        query = 'create table favourite(id int auto_increment primary key not null, path varchar(100) not null, meaning nvarchar(200), user_id int not null, foreign key (user_id) references user(id))'
        cur.execute(query)
    except:
        pass

    try:
        query = 'update favourite set meaning = %s where id = %s'
        cur.execute(query, (meaning, id))
        conn.commit()
        return 1
    except:
        return -1

def insert_favourite(path, meaning, user_id):
    cur = conn.cursor()
    try:
        query = 'create table favourite(id int auto_increment primary key not null, path varchar(100) not null, meaning nvarchar(200), user_id int not null, foreign key (user_id) references user(id))'
        cur.execute(query)
    except:
        pass

    try:
        query = 'insert into favourite(path, meaning, user_id) values(%s, %s, %s)'
        cur.execute(query, (path, meaning, user_id))
        conn.commit()
        return 1
    except:
        return -1


def delete_favourite(id):
    cur = conn.cursor()
    try:
        query = 'create table favourite(id int auto_increment primary key not null, path varchar(100) not null, meaning nvarchar(200), user_id int not null, foreign key (user_id) references user(id))'
        cur.execute(query)
    except:
        pass

    try:
        query = 'delete from favourite where id = %s'
        cur.execute(query, id)
        conn.commit()
        return 1
    except:
        return -1


def get_all_favourites():
    cur = conn.cursor()
    try:
        query = 'create table favourite(id int auto_increment primary key not null, path varchar(100) not null, meaning nvarchar(200), user_id int not null, foreign key (user_id) references user(id))'
        cur.execute(query)
    except:
        pass

    try:
        query = 'select * from favourite order by meaning asc'
        cur.execute(query)
        row = cur.fetchall()
        return row
    except:
        return None


def get_favourite(id):
    cur = conn.cursor()
    try:
        query = 'create table favourite(id int auto_increment primary key not null, path varchar(100) not null, meaning nvarchar(200), user_id int not null, foreign key (user_id) references user(id))'
        cur.execute(query)
    except:
        pass

    try:
        query = 'select * from favourite where id = %s'
        cur.execute(query, id)
        row = cur.fetchone()
        return row
    except:
        return None

def get_translation_by_user_id(id):
    cur = conn.cursor()
    try:
        query = 'create table translation(id int auto_increment primary key not null, path varchar(100) not null, meaning nvarchar(200), user_id int not null, foreign key (user_id) references user(id), created_time datetime)'
        cur.execute(query)
    except:
        pass

    try:
        query = 'select * from translation where user_id = %s'
        cur.execute(query, id)
        row = cur.fetchall()
        return row
    except:
        return None


def get_favourite_by_user_id(id):
    cur = conn.cursor()
    try:
        query = 'create table favourite(id int auto_increment primary key not null, path varchar(100) not null, meaning nvarchar(200), user_id int not null, foreign key (user_id) references user(id))'
        cur.execute(query)
    except:
        pass

    try:
        query = 'select * from favourite where user_id = %s'
        cur.execute(query, id)
        row = cur.fetchall()
        return row
    except:
        return None

def delete_all_translation_by_user_id(id):
    cur = conn.cursor()
    try:
        query = 'create table translation(id int auto_increment primary key not null, path varchar(100) not null, meaning nvarchar(200), user_id int not null, foreign key (user_id) references user(id), created_time datetime)'
        cur.execute(query)
    except:
        pass

    try:
        query = 'delete from translation where user_id = %s'
        cur.execute(query, id)
        conn.commit()
        return 1
    except:
        return -1

def delete_all_favourite_by_user_id(id):
    cur = conn.cursor()
    try:
        query = 'create table favourite(id int auto_increment primary key not null, path varchar(100) not null, meaning nvarchar(200), user_id int not null, foreign key (user_id) references user(id))'
        cur.execute(query)
    except:
        pass

    try:
        query = 'delete from favourite where user_id = %s'
        cur.execute(query, id)
        conn.commit()
        return 1
    except:
        return -1



