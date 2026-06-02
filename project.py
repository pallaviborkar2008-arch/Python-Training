# Main Entity Dictionary (Student Quiz Record)
quiz_records = [
    {
        "student_id": 101,
        "name": "Pallavi",
        "subject": "Python",
        "score": 85,
        "attempts": 3,
        "status": "Pass"
    },
    {
        "student_id": 102,
        "name": "Rahul",
        "subject": "Maths",
        "score": 72,
        "attempts": 2,
        "status": "Pass"
    },
    {
        "student_id": 103,
        "name": "Sneha",
        "subject": "Science",
        "score": 45,
        "attempts": 1,
        "status": "Fail"
    },
    {
        "student_id": 104,
        "name": "Amit",
        "subject": "English",
        "score": 91,
        "attempts": 4,
        "status": "Pass"
    },
    {
        "student_id": 105,
        "name": "Priya",
        "subject": "Computer",
        "score": 67,
        "attempts": 2,
        "status": "Pass"
    }
]

def get_status(score):
    if score >= 50:
        return "Pass"
    else:
        return "Fail"

def search_student(student_id):
    for record in quiz_records:
        if record["student_id"] == student_id:
            return record

for record in quiz_records:
    record["status"] = get_status(record["score"])

leaderboard = {
    "Pallavi": 85,
    "Rahul": 72,
    "Sneha": 45,
    "Amit": 91,
    "Priya": 67
}

print("\nLeaderboard")
for name, score in leaderboard.items():
    print(name, ":", score)

