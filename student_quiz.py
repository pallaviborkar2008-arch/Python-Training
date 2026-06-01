#list of menu options for the student quiz application
menu = ["1. Start Quiz", "2. View Subjects", "3. MCQ Questions", "4. View Score", "5. Leaderboard", "6. Exit"]
    
def show_menu():
    print("\n===== STUDENT QUIZ HUB =====")
    for item in menu:
        print(item)
    while True:
        show_menu()
  
    choice = input("\nEnter your choice: ")

    if choice == "1":
        print("Quiz Started...")
    elif choice == "2":
 
        print("Subjects: Math, Science, English")
    elif choice == "3":
        print("MCQ Questions Section")
    elif choice == "4":
        print("Your Score: 8/10")
    elif choice == "5":
        print("Leaderboard")
        print("1. Rahul - 95")
        print("2. Priya - 90")
        print("3. Amit - 85")
    elif choice == "6":
        print("Thank You!")
    else:
        print("Invalid Choice!")
 
 #Define function 
def greet(name):
    print("Hello, " + name + "! Welcome to the Student Quiz Hub.")







