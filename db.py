import sqlite3


def connection():
    db = sqlite3.connect("db.sqlite3")
    sql = db.cursor()
    sql.execute("""CREATE TABLE IF NOT EXISTS users (
                                username TEXT PRIMARY KEY,
                                first_name TEXT,
                                last_name TEXT,
                                email TEXT,
                                password TEXT                            
                                )"""
                )
    sql.execute("""CREATE TABLE IF NOT EXISTS notes (
                                id     INTEGER PRIMARY KEY AUTOINCREMENT,
                                note   TEXT,
                                author TEXT    REFERENCES users (username)                         
                                )"""
                )
    db.commit()
    return sql, db
