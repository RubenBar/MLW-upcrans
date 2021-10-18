import sqlite3

from sqlite3 import Error

def create_table():
    con = sql_connection()
    create_table(con)


def sql_connection():
    try:
        con = sqlite3.connect('mydatabase.db')
        return con

    except Error:
        print(Error)


def create_table(con):
    cursorObj = con.cursor()
    command = """CREATE TABLE dataEncrypt(
        id_user integer PRIMARY KEY, 
        key_AES text NOT NULL, 
        publickey_RSA text NOT NULL,
        privatekey_RSA text NOT NULL,
        decrypted text)"""
    cursorObj.execute(command)
    con.commit()


def sql_insert(con, data):
    cursorObj = con.cursor()    
    cursorObj.execute('INSERT INTO dataEncrypt(id_user, key_AES, publickey_RSA, privatekey_RSA, decrypted) VALUES(?, ?, ?, ?, ?)', data)    
    con.commit()       


####################################################
def add_data(data):
     con = sql_connection()   
     sql_insert(con, data)


####################################################
def update_encrypted(decrypted, id):
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute('UPDATE dataEncrypt SET decrypted = "'+decrypted+'" where id_user = '+id)
    con.commit()


####################################################
def get_keyAES(id):
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute('SELECT key_AES FROM dataEncrypt where id_user='+str(id))
    rows = cursorObj.fetchall()
    return rows[0][0]


def get_decrypted(id):
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute('SELECT decrypted FROM dataEncrypt where id='+id)
    rows = cursorObj.fetchall()
    return rows[0][0]