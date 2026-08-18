import sqlite3
from flask import Flask,render_template,request,url_for,flash,redirect

app = Flask(__name__)
app.secret_key ="supersecretkey"

def get_db():
    conn = sqlite3.connect("practice.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll TEXT,
    marks INTEGER DEFAULT 0,
    subject TEXT,
    attendance INTEGER
)
''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = get_db() 
    students = conn.execute('SELECT * FROM students ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('home.html',students=students)
@app.route('/add', methods=['GET', 'POST'])
def add_students():
    if request.method == "POST":
        name = request.form["students_name"]
        score = request.form["score"]
        attempts= request.form["attempts"]
        status = request.form["status"]
        subjects = request.form["subjects"]

        if not name or not score:
            flash("Please provide both name and marks", "danger")
            return render_template("add_students.html")

        conn = get_db()
        conn.execute('''
            INSERT INTO students
            (name, roll, marks, subject, attendance)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, attempts, int(score), status, str (subjects)))

        conn.commit()
        conn.close()

        print(f"Received new student: {name} with marks: {score}")

        flash(f"Student {name} added successfully!", "success")
        return redirect(url_for('home'))

    return render_template("add_students.html")

@app.route('/delete/<int:id>')
def delete_student(id):
    conn = get_db()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash("Student deleted successfully!", "success")
    return redirect(url_for('home'))
    conn.commit()
    conn.close()
 
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
   




    