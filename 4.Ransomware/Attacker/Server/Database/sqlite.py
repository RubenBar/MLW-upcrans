import sqlite3

from sqlite3 import Error

def sql_connection():
    try:
        con = sqlite3.connect('Database/keys.db')
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


#Generate the file keys.db -> BBDD
def create_BBDD():
    con = sql_connection()
    create_table(con)


#Obtain the last inserted ID_USER
def last_insert_id():
    con = sql_connection()
    cursorObj = con.cursor()    
    cursorObj.execute('select MAX(id_user) from dataEncrypt')    
    rows = cursorObj.fetchall()
    return rows[0][0]


#Insert "data" in BBDD
def sql_insert(data):
    con = sql_connection()
    prevID = last_insert_id()
    if prevID == None:
        id_user = 1 
    else:
        id_user = prevID + 1 
    data = (id_user,) + data
    cursorObj = con.cursor()    
    cursorObj.execute('INSERT INTO dataEncrypt(id_user, key_AES, publickey_RSA, privatekey_RSA, decrypted) VALUES(?, ?, ?, ?, ?)', data)    
    con.commit() 

    return id_user


####################################################
def update_encrypted(decrypted, id):
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute('UPDATE dataEncrypt SET decrypted = "'+decrypted+'" where id_user = '+id)
    con.commit()

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