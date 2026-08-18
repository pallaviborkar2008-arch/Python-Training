import sqlite3
from flask import Flask, flash, render_template, request, redirect, url_for

app = Flask(__name__)

conn = sqlite3.connect("student_quiz_hub.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS quiz_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    subject TEXT,
    score INTEGER NOT NULL,
    attempts INTEGER NOT NULL,
    status TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS quiz_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    student_name TEXT,
    subject TEXT,
    score INTEGER
)
""")
conn.commit()
conn.close()

print("Database initialized and quiz_records table created.")