# list - one variable can store multiple values
students =["priya","shivani","sanjana","priti","sneha"]
print(students[0]) #first element
print(students[1]) #second element
print(students[2]) #third element
print(students[3]) #fourth element
print(students[4]) #fifth element


#Loop - to print all the elements in the list
for student in students:
    print(f"Hello {student}", "WELCOME TO PYTHON CLASS")
          

marks = [85, 90, 78, 92, 88]

for mark in marks:
    if mark >= 90:
        print(f"Excellent! you scored {mark}")
    elif mark >= 80:
        print(f"Good job! you scored {mark}")
    elif mark >= 70:
        print(f"Fair! you scored {mark}")
    else:
        print(f"Needs improvement! you scored {mark}")


# Define function
def greet(name):
    print(f"Hello, {name}! welcome to Python class!")

     
  
for student in students:
        greet(student)

