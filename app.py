from flask import Flask, render_template

app = Flask(__name__)

quiz_records = [
    {"name": "Pallavi", "score": 85, "attempts": 3},
    {"name": "Smita", "score": 72, "attempts": 2},
    {"name": "Sneha", "score": 45, "attempts": 1},
    {"name": "Geeta", "score": 91, "attempts": 4},
    {"name": "Priya", "score": 60, "attempts": 2}
]
def get_status(score):
    if score >= 50:
        return "Pass"
    return "Fail"
@app.route("/")
def home():
    return render_template(
        "home.html",
        project_name="Student Quiz Hub"
    )
@app.route("/subjects")
def subjects():
    subjects = ["C", "C++", "Java", "Python", "JavaScript"]
    return render_template("subjects.html", subjects=subjects)
@app.route("/students")
def students():
    total_quizzes = len(quiz_records)
    return render_template("students.html",
        quiz_records=quiz_records,
        total_quizzes=total_quizzes,
        get_status=get_status
    )
@app.route("/about")
def about():    
    return render_template("about.html")
if __name__ == "__main__":
    app.run(debug=True)