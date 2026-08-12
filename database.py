import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Zxcvbnm@7890#",
        database="ats_db"
    )