import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

os.environ["PYTHONUTF8"] = "1"

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
from google import genai

app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
QUIZZES = {

    "Python": [
        {
            "question": "Python is a ______ language.",
            "options": ["Programming", "Database", "Browser", "Operating System"],
            "answer": "Programming"
        },
        {
            "question": "Which symbol is used for comments?",
            "options": ["//", "#", "/*", "--"],
            "answer": "#"
        },
        {
            "question": "Which keyword is used to define a function?",
            "options": ["fun", "define", "def", "function"],
            "answer": "def"
        },
        {
            "question": "Which function is used to display output?",
            "options": ["print()", "display()", "show()", "echo()"],
            "answer": "print()"
        },
        {
            "question": "Which data type is used for decimal numbers?",
            "options": ["int", "float", "string", "bool"],
            "answer": "float"
        },
        {
            "question": "Which symbol is used for assignment?",
            "options": ["=", "==", "!=", ":"],
            "answer": "="
        },
        {
            "question": "Which keyword is used for loops?",
            "options": ["repeat", "for", "loop", "iterate"],
            "answer": "for"
        },
        {
            "question": "Which collection type stores multiple values?",
            "options": ["list", "int", "float", "bool"],
            "answer": "list"
        },
        {
            "question": "Python files have which extension?",
            "options": [".py", ".java", ".cpp", ".html"],
            "answer": ".py"
        },
        {
            "question": "Which function is used to take input from the user?",
            "options": ["scan()", "input()", "read()", "get()"],
            "answer": "input()"
        },
        # Python Questions 11-50

        {
            "question": "Which keyword is used to create a class in Python?",
            "options": ["class", "object", "struct", "define"],
            "answer": "class"
        },
        {
            "question": "Which function returns the length of a list?",
            "options": ["length()", "len()", "size()", "count()"],
            "answer": "len()"
        },
        {
            "question": "Which data type stores True or False?",
            "options": ["bool", "int", "str", "float"],
            "answer": "bool"
        },
        {
            "question": "Which brackets are used to create a list?",
            "options": ["[]", "{}", "()", "<>"],
            "answer": "[]"
        },
        {
            "question": "Which brackets are used to create a tuple?",
            "options": ["()", "[]", "{}", "<>"],
            "answer": "()"
        },
        {
            "question": "Which symbol is used for exponentiation?",
            "options": ["**", "//", "^^", "%%"],
            "answer": "**"
        },
        {
            "question": "Which operator gives the remainder?",
            "options": ["%", "/", "//", "**"],
            "answer": "%"
        },
        {
            "question": "Which operator performs floor division?",
            "options": ["//", "/", "%", "**"],
            "answer": "//"
        },
        {
            "question": "Which keyword is used for conditional statements?",
            "options": ["if", "when", "check", "condition"],
            "answer": "if"
        },
        {
            "question": "Which keyword is used when the if condition is false?",
            "options": ["else", "otherwise", "false", "elif"],
            "answer": "else"
        },
        {
            "question": "Which keyword checks another condition?",
            "options": ["elif", "else", "elseif", "check"],
            "answer": "elif"
        },
        {
            "question": "Which keyword is used to exit a loop?",
            "options": ["break", "stop", "exit", "end"],
            "answer": "break"
        },
        {
            "question": "Which keyword skips the current iteration?",
            "options": ["continue", "skip", "pass", "next"],
            "answer": "continue"
        },
        {
            "question": "Which keyword does nothing when executed?",
            "options": ["pass", "skip", "null", "empty"],
            "answer": "pass"
        },
        {
            "question": "Which function converts a value to an integer?",
            "options": ["int()", "integer()", "num()", "convert()"],
            "answer": "int()"
        },
        {
            "question": "Which function converts a value to a string?",
            "options": ["str()", "string()", "text()", "convert()"],
            "answer": "str()"
        },
        {
            "question": "Which function converts a value to a floating-point number?",
            "options": ["float()", "decimal()", "double()", "number()"],
            "answer": "float()"
        },
        {
            "question": "Which keyword is used to import a module?",
            "options": ["import", "include", "using", "require"],
            "answer": "import"
        },
        {
            "question": "Which keyword is used to create an alias while importing?",
            "options": ["as", "alias", "with", "name"],
            "answer": "as"
        },
        {
            "question": "Which function returns the type of an object?",
            "options": ["type()", "typeof()", "kind()", "datatype()"],
            "answer": "type()"
        },
        {
            "question": "Which function returns the maximum value?",
            "options": ["max()", "maximum()", "high()", "top()"],
            "answer": "max()"
        },
        {
            "question": "Which function returns the minimum value?",
            "options": ["min()", "minimum()", "low()", "bottom()"],
            "answer": "min()"
        },
        {
            "question": "Which function returns the sum of values?",
            "options": ["sum()", "total()", "add()", "plus()"],
            "answer": "sum()"
        },
        {
            "question": "Which function rounds a number?",
            "options": ["round()", "approx()", "near()", "format()"],
            "answer": "round()"
        },
        {
            "question": "Which method adds an element to the end of a list?",
            "options": ["append()", "add()", "insert()", "push()"],
            "answer": "append()"
        },
        {
            "question": "Which method removes the last element from a list?",
            "options": ["pop()", "remove()", "delete()", "last()"],
            "answer": "pop()"
        },
        {
            "question": "Which method sorts a list?",
            "options": ["sort()", "order()", "arrange()", "sortedlist()"],
            "answer": "sort()"
        },
        {
            "question": "Which method reverses a list?",
            "options": ["reverse()", "backward()", "invert()", "flip()"],
            "answer": "reverse()"
        },
        {
            "question": "Which method removes a specific value from a list?",
            "options": ["remove()", "delete()", "erase()", "discard()"],
            "answer": "remove()"
        },
        {
            "question": "Which collection stores unique values?",
            "options": ["set", "list", "tuple", "string"],
            "answer": "set"
        },
        {
            "question": "Which collection stores key-value pairs?",
            "options": ["dictionary", "list", "tuple", "set"],
            "answer": "dictionary"
        },
        {
            "question": "Which brackets are used for a dictionary?",
            "options": ["{}", "[]", "()", "<>"],
            "answer": "{}"
        },
        {
            "question": "Which keyword is used to handle exceptions?",
            "options": ["try", "catch", "error", "handle"],
            "answer": "try"
        },
        {
            "question": "Which keyword handles an exception?",
            "options": ["except", "catch", "error", "handle"],
            "answer": "except"
        },
        {
            "question": "Which keyword is executed whether an exception occurs or not?",
            "options": ["finally", "always", "last", "end"],
            "answer": "finally"
        },
        {
            "question": "Which keyword is used to raise an exception?",
            "options": ["raise", "throw", "error", "exception"],
            "answer": "raise"
        },
        {
            "question": "Which keyword is used to define an anonymous function?",
            "options": ["lambda", "anonymous", "function", "def"],
            "answer": "lambda"
        },
        {
            "question": "Which function creates a sequence of numbers?",
            "options": ["range()", "sequence()", "numbers()", "series()"],
            "answer": "range()"
        },
        {
            "question": "Which function returns an iterable with index values?",
            "options": ["enumerate()", "index()", "number()", "counter()"],
            "answer": "enumerate()"
        },
        {
            "question": "Which keyword is used to return a value from a function?",
            "options": ["return", "send", "output", "result"],
            "answer": "return"
        }
    ],


    "C": [
        {
            "question": "Who developed the C language?",
            "options": ["Dennis Ritchie", "James Gosling", "Bjarne Stroustrup", "Guido van Rossum"],
            "answer": "Dennis Ritchie"
        },
        {
            "question": "Which symbol is used to end a statement in C?",
            "options": [";", ".", ":", ","],
            "answer": ";"
        },
        {
            "question": "Which function is the starting point of a C program?",
            "options": ["start()", "main()", "begin()", "run()"],
            "answer": "main()"
        },
        {
            "question": "Which header file is used for printf()?",
            "options": ["stdio.h", "math.h", "string.h", "stdlib.h"],
            "answer": "stdio.h"
        },
        {
            "question": "Which function is used to take input in C?",
            "options": ["scanf()", "input()", "read()", "cin"],
            "answer": "scanf()"
        },
        {
            "question": "Which data type stores whole numbers?",
            "options": ["int", "float", "char", "double"],
            "answer": "int"
        },
        {
            "question": "Which symbol is used for comments in C?",
            "options": ["//", "#", "<!-- -->", "--"],
            "answer": "//"
        },
        {
            "question": "Which loop is available in C?",
            "options": ["for", "repeat", "foreach", "loop"],
            "answer": "for"
        },
        {
            "question": "Which operator is used for addition?",
            "options": ["+", "-", "*", "/"],
            "answer": "+"
        },
        {
            "question": "Which keyword is used to return a value from a function?",
            "options": ["return", "break", "exit", "continue"],
            "answer": "return"
        },
                {
            "question": "Which data type is used to store a single character in C?",
            "options": ["char", "string", "character", "text"],
            "answer": "char"
        },
        {
            "question": "Which data type is used to store decimal values?",
            "options": ["float", "int", "char", "void"],
            "answer": "float"
        },
        {
            "question": "Which data type provides double precision?",
            "options": ["double", "float", "int", "long"],
            "answer": "double"
        },
        {
            "question": "Which operator is used for multiplication?",
            "options": ["*", "+", "/", "%"],
            "answer": "*"
        },
        {
            "question": "Which operator is used for subtraction?",
            "options": ["-", "+", "*", "/"],
            "answer": "-"
        },
        {
            "question": "Which operator is used for division?",
            "options": ["/", "*", "%", "-"],
            "answer": "/"
        },
        {
            "question": "Which operator gives the remainder?",
            "options": ["%", "/", "//", "*"],
            "answer": "%"
        },
        {
            "question": "Which operator is used for equality comparison?",
            "options": ["==", "=", "!=", "==="],
            "answer": "=="
        },
        {
            "question": "Which operator means not equal to?",
            "options": ["!=", "==", "=", "<>"],
            "answer": "!="
        },
        {
            "question": "Which operator represents logical AND?",
            "options": ["&&", "||", "!", "&"],
            "answer": "&&"
        },
        {
            "question": "Which operator represents logical OR?",
            "options": ["||", "&&", "!", "|"],
            "answer": "||"
        },
        {
            "question": "Which operator represents logical NOT?",
            "options": ["!", "&&", "||", "~"],
            "answer": "!"
        },
        {
            "question": "Which keyword is used for a conditional statement?",
            "options": ["if", "when", "check", "condition"],
            "answer": "if"
        },
        {
            "question": "Which keyword is used when the if condition is false?",
            "options": ["else", "otherwise", "false", "default"],
            "answer": "else"
        },
        {
            "question": "Which statement is used to test multiple conditions?",
            "options": ["else if", "switch", "repeat", "check"],
            "answer": "else if"
        },
        {
            "question": "Which statement is used for multiple fixed choices?",
            "options": ["switch", "if", "loop", "select"],
            "answer": "switch"
        },
        {
            "question": "Which keyword is used inside a switch statement?",
            "options": ["case", "option", "choice", "value"],
            "answer": "case"
        },
        {
            "question": "Which keyword is used to exit a switch case?",
            "options": ["break", "exit", "stop", "return"],
            "answer": "break"
        },
        {
            "question": "Which loop checks the condition before execution?",
            "options": ["while", "do-while", "repeat", "loop"],
            "answer": "while"
        },
        {
            "question": "Which loop executes at least once?",
            "options": ["do-while", "while", "for", "repeat"],
            "answer": "do-while"
        },
        {
            "question": "Which loop is commonly used when the number of iterations is known?",
            "options": ["for", "while", "do-while", "switch"],
            "answer": "for"
        },
        {
            "question": "Which keyword skips the current iteration of a loop?",
            "options": ["continue", "skip", "pass", "next"],
            "answer": "continue"
        },
        {
            "question": "Which keyword exits a loop immediately?",
            "options": ["break", "exit", "stop", "return"],
            "answer": "break"
        },
        {
            "question": "What is an array?",
            "options": [
                "Collection of similar data types",
                "Collection of different programs",
                "A function",
                "A keyword"
            ],
            "answer": "Collection of similar data types"
        },
        {
            "question": "Array indexing in C starts from:",
            "options": ["0", "1", "-1", "2"],
            "answer": "0"
        },
        {
            "question": "Which symbol is used to access the address of a variable?",
            "options": ["&", "*", "#", "@"],
            "answer": "&"
        },
        {
            "question": "Which symbol is used to dereference a pointer?",
            "options": ["*", "&", "#", "->"],
            "answer": "*"
        },
        {
            "question": "Which variable stores the address of another variable?",
            "options": ["Pointer", "Array", "Structure", "Constant"],
            "answer": "Pointer"
        },
        {
            "question": "Which keyword is used to define a constant value?",
            "options": ["const", "constant", "define", "fixed"],
            "answer": "const"
        },
        {
            "question": "Which preprocessor directive is used to define a macro?",
            "options": ["#define", "#include", "#macro", "#const"],
            "answer": "#define"
        },
        {
            "question": "Which preprocessor directive is used to include a header file?",
            "options": ["#include", "#define", "#header", "#import"],
            "answer": "#include"
        },
        {
            "question": "Which header file contains string functions?",
            "options": ["string.h", "stdio.h", "math.h", "stdlib.h"],
            "answer": "string.h"
        },
        {
            "question": "Which header file contains mathematical functions?",
            "options": ["math.h", "stdio.h", "string.h", "stdlib.h"],
            "answer": "math.h"
        },
        {
            "question": "Which function is used to find the length of a string?",
            "options": ["strlen()", "strlength()", "length()", "size()"],
            "answer": "strlen()"
        },
        {
            "question": "Which function copies one string to another?",
            "options": ["strcpy()", "strcopy()", "copy()", "stringcopy()"],
            "answer": "strcpy()"
        },
        {
            "question": "Which function compares two strings?",
            "options": ["strcmp()", "compare()", "strcompare()", "equal()"],
            "answer": "strcmp()"
        },
        {
            "question": "Which function joins two strings?",
            "options": ["strcat()", "join()", "concat()", "strjoin()"],
            "answer": "strcat()"
        },
        {
            "question": "Which keyword is used to define a structure?",
            "options": ["struct", "structure", "record", "class"],
            "answer": "struct"
        },
        {
            "question": "Which keyword is used to define an enumeration?",
            "options": ["enum", "enumeration", "list", "set"],
            "answer": "enum"
        },
        {
            "question": "Which keyword is used to specify that a function returns no value?",
            "options": ["void", "null", "empty", "none"],
            "answer": "void"
        },
        {
            "question": "Which function is used to allocate memory dynamically?",
            "options": ["malloc()", "alloc()", "memory()", "new()"],
            "answer": "malloc()"
        }
    ],


    "C++": [
        {
            "question": "Who developed C++?",
            "options": ["Dennis Ritchie", "James Gosling", "Bjarne Stroustrup", "Guido van Rossum"],
            "answer": "Bjarne Stroustrup"
        },
        {
            "question": "C++ is a ______ programming language.",
            "options": ["Object-Oriented", "Database", "Markup", "Assembly"],
            "answer": "Object-Oriented"
        },
        {
            "question": "Which function is the starting point of a C++ program?",
            "options": ["main()", "start()", "run()", "begin()"],
            "answer": "main()"
        },
        {
            "question": "Which operator is used to access members of an object?",
            "options": [".", "->", "::", "#"],
            "answer": "."
        },
        {
            "question": "Which header file is used for cout and cin?",
            "options": ["iostream", "stdio.h", "string.h", "math.h"],
            "answer": "iostream"
        },
        {
            "question": "Which keyword is used to create a class?",
            "options": ["class", "struct", "object", "new"],
            "answer": "class"
        },
        {
            "question": "Which keyword is used to inherit a class?",
            "options": ["extends", "inherits", ":", "super"],
            "answer": ":"
        },
        {
            "question": "Which keyword is used for dynamic memory allocation?",
            "options": ["malloc", "new", "alloc", "create"],
            "answer": "new"
        },
        {
            "question": "Which symbol is used to end a statement?",
            "options": [";", ".", ":", ","],
            "answer": ";"
        },
        {
            "question": "Which keyword is used to return a value from a function?",
            "options": ["return", "break", "continue", "exit"],
            "answer": "return"
        },
                {
            "question": "What does OOP stand for?",
            "options": ["Object-Oriented Programming", "Object Operating Program", "Open Object Programming", "Object Order Process"],
            "answer": "Object-Oriented Programming"
        },
        {
            "question": "Which concept binds data and functions together?",
            "options": ["Encapsulation", "Inheritance", "Polymorphism", "Abstraction"],
            "answer": "Encapsulation"
        },
        {
            "question": "Which concept allows a class to acquire properties of another class?",
            "options": ["Inheritance", "Encapsulation", "Abstraction", "Compilation"],
            "answer": "Inheritance"
        },
        {
            "question": "Which concept allows one interface to have multiple forms?",
            "options": ["Polymorphism", "Inheritance", "Encapsulation", "Abstraction"],
            "answer": "Polymorphism"
        },
        {
            "question": "Which concept hides unnecessary implementation details?",
            "options": ["Abstraction", "Inheritance", "Encapsulation", "Polymorphism"],
            "answer": "Abstraction"
        },
        {
            "question": "Which access specifier makes members accessible from anywhere?",
            "options": ["public", "private", "protected", "internal"],
            "answer": "public"
        },
        {
            "question": "Which access specifier makes members accessible only inside the class?",
            "options": ["private", "public", "protected", "internal"],
            "answer": "private"
        },
        {
            "question": "Which access specifier allows access inside the class and derived classes?",
            "options": ["protected", "private", "public", "internal"],
            "answer": "protected"
        },
        {
            "question": "What is an object?",
            "options": ["Instance of a class", "Function", "Variable type", "Header file"],
            "answer": "Instance of a class"
        },
        {
            "question": "What is a constructor?",
            "options": ["Special member function", "Normal variable", "Header file", "Loop"],
            "answer": "Special member function"
        },
        {
            "question": "Which function is automatically called when an object is created?",
            "options": ["Constructor", "Destructor", "main()", "start()"],
            "answer": "Constructor"
        },
        {
            "question": "Which symbol is used before a destructor name?",
            "options": ["~", "!", "#", "*"],
            "answer": "~"
        },
        {
            "question": "Which function is automatically called when an object is destroyed?",
            "options": ["Destructor", "Constructor", "delete()", "destroy()"],
            "answer": "Destructor"
        },
        {
            "question": "Which keyword is used to create an object dynamically?",
            "options": ["new", "malloc", "create", "alloc"],
            "answer": "new"
        },
        {
            "question": "Which keyword releases dynamically allocated memory?",
            "options": ["delete", "free", "remove", "release"],
            "answer": "delete"
        },
        {
            "question": "Which operator is used with a pointer to access an object member?",
            "options": ["->", ".", "::", "*"],
            "answer": "->"
        },
        {
            "question": "Which operator is used to access a class member through an object?",
            "options": [".", "->", "::", "#"],
            "answer": "."
        },
        {
            "question": "Which operator is called the scope resolution operator?",
            "options": ["::", ".", "->", ":"],
            "answer": "::"
        },
        {
            "question": "Which keyword is used to declare a constant?",
            "options": ["const", "constant", "fixed", "static"],
            "answer": "const"
        },
        {
            "question": "Which keyword is used to create a reference variable?",
            "options": ["&", "ref", "reference", "*"],
            "answer": "&"
        },
        {
            "question": "Which feature allows functions to have the same name with different parameters?",
            "options": ["Function Overloading", "Function Overriding", "Inheritance", "Encapsulation"],
            "answer": "Function Overloading"
        },
        {
            "question": "Which feature allows a derived class to redefine a base class function?",
            "options": ["Function Overriding", "Function Overloading", "Encapsulation", "Abstraction"],
            "answer": "Function Overriding"
        },
        {
            "question": "Which keyword is used to declare a virtual function?",
            "options": ["virtual", "dynamic", "override", "abstract"],
            "answer": "virtual"
        },
        {
            "question": "Which keyword can be used to explicitly override a virtual function?",
            "options": ["override", "virtual", "extends", "redefine"],
            "answer": "override"
        },
        {
            "question": "Which keyword is used to prevent a class from being inherited?",
            "options": ["final", "sealed", "stop", "private"],
            "answer": "final"
        },
        {
            "question": "Which container stores elements in a dynamic array?",
            "options": ["vector", "stack", "queue", "map"],
            "answer": "vector"
        },
        {
            "question": "Which header file is required for vector?",
            "options": ["<vector>", "<array>", "<list>", "<container>"],
            "answer": "<vector>"
        },
        {
            "question": "Which container follows LIFO?",
            "options": ["stack", "queue", "vector", "map"],
            "answer": "stack"
        },
        {
            "question": "Which container follows FIFO?",
            "options": ["queue", "stack", "vector", "set"],
            "answer": "queue"
        },
        {
            "question": "Which container stores key-value pairs?",
            "options": ["map", "vector", "stack", "queue"],
            "answer": "map"
        },
        {
            "question": "Which header file is commonly used for strings in C++?",
            "options": ["<string>", "<cstring>", "<text>", "<str>"],
            "answer": "<string>"
        },
        {
            "question": "Which object is used for standard output?",
            "options": ["cout", "cin", "cerr", "output"],
            "answer": "cout"
        },
        {
            "question": "Which object is used for standard input?",
            "options": ["cin", "cout", "input", "scan"],
            "answer": "cin"
        },
        {
            "question": "Which operator is used with cout?",
            "options": ["<<", ">>", "->", "::"],
            "answer": "<<"
        },
        {
            "question": "Which operator is used with cin?",
            "options": [">>", "<<", "->", "::"],
            "answer": ">>"
        },
        {
            "question": "Which keyword is used to define a namespace?",
            "options": ["namespace", "package", "module", "scope"],
            "answer": "namespace"
        },
        {
            "question": "Which keyword is used to bring names into the current scope?",
            "options": ["using", "include", "import", "with"],
            "answer": "using"
        },
        {
            "question": "Which C++ feature allows generic programming?",
            "options": ["Templates", "Pointers", "Classes", "Namespaces"],
            "answer": "Templates"
        },
        {
            "question": "Which keyword is used to define a template?",
            "options": ["template", "generic", "typename", "class"],
            "answer": "template"
        },
        {
            "question": "Which keyword can specify a type parameter in a template?",
            "options": ["typename", "type", "generic", "template"],
            "answer": "typename"
        }
    ],


    "Java": [
        {
            "question": "Who developed Java?",
            "options": ["Dennis Ritchie", "James Gosling", "Bjarne Stroustrup", "Guido van Rossum"],
            "answer": "James Gosling"
        },
        {
            "question": "Java is a ______ programming language.",
            "options": ["Object-Oriented", "Markup", "Database", "Assembly"],
            "answer": "Object-Oriented"
        },
        {
            "question": "Which method is the starting point of a Java program?",
            "options": ["main()", "start()", "run()", "begin()"],
            "answer": "main()"
        },
        {
            "question": "Which keyword is used to create an object?",
            "options": ["new", "class", "object", "create"],
            "answer": "new"
        },
        {
            "question": "Which package is imported by default in Java?",
            "options": ["java.lang", "java.util", "java.io", "java.sql"],
            "answer": "java.lang"
        },
        {
            "question": "Which keyword is used to inherit a class?",
            "options": ["extends", "implements", "inherits", "super"],
            "answer": "extends"
        },
        {
            "question": "Which keyword is used to define a class?",
            "options": ["class", "struct", "object", "new"],
            "answer": "class"
        },
        {
            "question": "Which operator is used for string concatenation?",
            "options": ["+", "-", "*", "/"],
            "answer": "+"
        },
        {
            "question": "Which keyword is used to stop a loop?",
            "options": ["break", "continue", "exit", "stop"],
            "answer": "break"
        },
        {
            "question": "Java source files have which extension?",
            "options": [".java", ".class", ".py", ".cpp"],
            "answer": ".java"
        },
                {
            "question": "Which keyword is used to define a constant in Java?",
            "options": ["final", "const", "static", "constant"],
            "answer": "final"
        },
        {
            "question": "Which data type is used to store whole numbers in Java?",
            "options": ["int", "float", "char", "boolean"],
            "answer": "int"
        },
        {
            "question": "Which data type is used to store decimal numbers?",
            "options": ["double", "int", "char", "boolean"],
            "answer": "double"
        },
        {
            "question": "Which data type stores a single character?",
            "options": ["char", "string", "character", "text"],
            "answer": "char"
        },
        {
            "question": "Which data type stores true or false?",
            "options": ["boolean", "bool", "bit", "logical"],
            "answer": "boolean"
        },
        {
            "question": "Which keyword is used to create a subclass?",
            "options": ["extends", "inherits", "super", "implements"],
            "answer": "extends"
        },
        {
            "question": "Which keyword is used to implement an interface?",
            "options": ["implements", "extends", "interface", "inherits"],
            "answer": "implements"
        },
        {
            "question": "Which keyword refers to the current object?",
            "options": ["this", "self", "current", "object"],
            "answer": "this"
        },
        {
            "question": "Which keyword refers to the parent class?",
            "options": ["super", "parent", "base", "this"],
            "answer": "super"
        },
        {
            "question": "Which access modifier allows access from anywhere?",
            "options": ["public", "private", "protected", "default"],
            "answer": "public"
        },
        {
            "question": "Which access modifier allows access only within the same class?",
            "options": ["private", "public", "protected", "default"],
            "answer": "private"
        },
        {
            "question": "Which access modifier allows access in the same package and subclasses?",
            "options": ["protected", "private", "public", "static"],
            "answer": "protected"
        },
        {
            "question": "Which keyword is used to create an interface?",
            "options": ["interface", "implements", "abstract", "class"],
            "answer": "interface"
        },
        {
            "question": "Which keyword is used to create an abstract class?",
            "options": ["abstract", "interface", "virtual", "extends"],
            "answer": "abstract"
        },
        {
            "question": "Which keyword is used to prevent inheritance?",
            "options": ["final", "stop", "private", "sealed"],
            "answer": "final"
        },
        {
            "question": "Which concept means hiding implementation details?",
            "options": ["Abstraction", "Inheritance", "Encapsulation", "Polymorphism"],
            "answer": "Abstraction"
        },
        {
            "question": "Which concept combines data and methods into one unit?",
            "options": ["Encapsulation", "Inheritance", "Polymorphism", "Abstraction"],
            "answer": "Encapsulation"
        },
        {
            "question": "Which concept allows one method to behave differently?",
            "options": ["Polymorphism", "Encapsulation", "Inheritance", "Compilation"],
            "answer": "Polymorphism"
        },
        {
            "question": "Which concept allows a class to inherit properties from another class?",
            "options": ["Inheritance", "Abstraction", "Encapsulation", "Overloading"],
            "answer": "Inheritance"
        },
        {
            "question": "What is an object?",
            "options": ["Instance of a class", "Method", "Package", "Keyword"],
            "answer": "Instance of a class"
        },
        {
            "question": "What is a constructor?",
            "options": ["Special method used to initialize objects", "Normal method", "Variable", "Package"],
            "answer": "Special method used to initialize objects"
        },
        {
            "question": "Does a constructor have a return type?",
            "options": ["No", "Yes", "Only int", "Only void"],
            "answer": "No"
        },
        {
            "question": "Can constructors be overloaded?",
            "options": ["Yes", "No", "Only once", "Only in abstract classes"],
            "answer": "Yes"
        },
        {
            "question": "Which keyword is used to create an object?",
            "options": ["new", "create", "object", "make"],
            "answer": "new"
        },
        {
            "question": "Which method is the entry point of a Java program?",
            "options": ["main()", "start()", "run()", "execute()"],
            "answer": "main()"
        },
        {
            "question": "Which keyword is used to define a method?",
            "options": ["There is no special keyword", "method", "function", "define"],
            "answer": "There is no special keyword"
        },
        {
            "question": "Which keyword is used to inherit a class?",
            "options": ["extends", "inherits", "super", "implements"],
            "answer": "extends"
        },
        {
            "question": "Which keyword is used to handle exceptions?",
            "options": ["try", "catch", "handle", "error"],
            "answer": "try"
        },
        {
            "question": "Which block handles an exception?",
            "options": ["catch", "handle", "except", "error"],
            "answer": "catch"
        },
        {
            "question": "Which block is executed whether an exception occurs or not?",
            "options": ["finally", "always", "last", "default"],
            "answer": "finally"
        },
        {
            "question": "Which keyword is used to explicitly throw an exception?",
            "options": ["throw", "throws", "raise", "error"],
            "answer": "throw"
        },
        {
            "question": "Which keyword declares that a method may throw exceptions?",
            "options": ["throws", "throw", "exception", "raise"],
            "answer": "throws"
        },
        {
            "question": "Which class is the superclass of all Java classes?",
            "options": ["Object", "Class", "Main", "System"],
            "answer": "Object"
        },
        {
            "question": "Which package contains the Scanner class?",
            "options": ["java.util", "java.lang", "java.io", "java.sql"],
            "answer": "java.util"
        },
        {
            "question": "Which class is commonly used to take input from the keyboard?",
            "options": ["Scanner", "Input", "Reader", "Keyboard"],
            "answer": "Scanner"
        },
        {
            "question": "Which method is used to compare the contents of two strings?",
            "options": ["equals()", "==", "compare()", "same()"],
            "answer": "equals()"
        },
        {
            "question": "Which operator compares object references?",
            "options": ["==", "equals()", "=", "==="],
            "answer": "=="
        },
        {
            "question": "Which method returns the length of a String?",
            "options": ["length()", "size()", "count()", "strlen()"],
            "answer": "length()"
        },
        {
            "question": "Which method converts a String to lowercase?",
            "options": ["toLowerCase()", "lower()", "lowerCase()", "toLower()"],
            "answer": "toLowerCase()"
        },
        {
            "question": "Which method converts a String to uppercase?",
            "options": ["toUpperCase()", "upper()", "upperCase()", "toUpper()"],
            "answer": "toUpperCase()"
        }
    ],


    "JavaScript": [
        {
            "question": "JavaScript is mainly used for ______.",
            "options": ["Web Development", "Database", "Operating System", "Networking"],
            "answer": "Web Development"
        },
        {
            "question": "Which tag is used to include JavaScript in HTML?",
            "options": ["<script>", "<style>", "<js>", "<javascript>"],
            "answer": "<script>"
        },
        {
            "question": "Which keyword is used to declare a variable?",
            "options": ["var", "int", "string", "float"],
            "answer": "var"
        },
        {
            "question": "Which function is used to display a message box?",
            "options": ["alert()", "print()", "display()", "show()"],
            "answer": "alert()"
        },
        {
            "question": "Which method is used to write output in the browser?",
            "options": ["document.write()", "console.log()", "print()", "alert()"],
            "answer": "document.write()"
        },
        {
            "question": "Which symbol is used for single-line comments?",
            "options": ["//", "/*", "#", "--"],
            "answer": "//"
        },
        {
            "question": "Which keyword is used to define a function?",
            "options": ["function", "def", "fun", "define"],
            "answer": "function"
        },
        {
            "question": "Which operator is used for comparison?",
            "options": ["==", "=", "+", "*"],
            "answer": "=="
        },
        {
            "question": "Which loop is commonly used in JavaScript?",
            "options": ["for", "repeat", "loop", "foreach"],
            "answer": "for"
        },
        {
            "question": "JavaScript files have which extension?",
            "options": [".js", ".java", ".py", ".cpp"],
            "answer": ".js"
        },
                {
            "question": "Which keyword can be used to declare a block-scoped variable?",
            "options": ["let", "var", "int", "define"],
            "answer": "let"
        },
        {
            "question": "Which keyword is used to declare a constant?",
            "options": ["const", "constant", "final", "fixed"],
            "answer": "const"
        },
        {
            "question": "Which function is used to print output in the browser console?",
            "options": ["console.log()", "print()", "display()", "write()"],
            "answer": "console.log()"
        },
        {
            "question": "Which operator is used for strict equality?",
            "options": ["===", "==", "=", "!="],
            "answer": "==="
        },
        {
            "question": "Which operator is used for strict inequality?",
            "options": ["!==", "!=", "==", "<>"],
            "answer": "!=="
        },
        {
            "question": "Which symbol is used for a single-line comment?",
            "options": ["//", "#", "/*", "<!--"],
            "answer": "//"
        },
        {
            "question": "Which symbols are used for multi-line comments?",
            "options": ["/* */", "//", "<!-- -->", "# #"],
            "answer": "/* */"
        },
        {
            "question": "Which data type represents true or false?",
            "options": ["Boolean", "Number", "String", "Object"],
            "answer": "Boolean"
        },
        {
            "question": "Which data type is used for text?",
            "options": ["String", "Text", "Character", "Words"],
            "answer": "String"
        },
        {
            "question": "Which data type is used for numbers?",
            "options": ["Number", "Integer", "Numeric", "Digit"],
            "answer": "Number"
        },
        {
            "question": "Which value represents an intentionally empty value?",
            "options": ["null", "empty", "void", "none"],
            "answer": "null"
        },
        {
            "question": "Which value indicates that a variable has not been assigned a value?",
            "options": ["undefined", "null", "empty", "none"],
            "answer": "undefined"
        },
        {
            "question": "Which method converts a string to uppercase?",
            "options": ["toUpperCase()", "upper()", "uppercase()", "toUpper()"],
            "answer": "toUpperCase()"
        },
        {
            "question": "Which method converts a string to lowercase?",
            "options": ["toLowerCase()", "lower()", "lowercase()", "toLower()"],
            "answer": "toLowerCase()"
        },
        {
            "question": "Which property returns the length of a string?",
            "options": ["length", "size", "count", "len"],
            "answer": "length"
        },
        {
            "question": "Which method adds an element to the end of an array?",
            "options": ["push()", "add()", "append()", "insert()"],
            "answer": "push()"
        },
        {
            "question": "Which method removes the last element of an array?",
            "options": ["pop()", "remove()", "delete()", "last()"],
            "answer": "pop()"
        },
        {
            "question": "Which method removes the first element of an array?",
            "options": ["shift()", "removeFirst()", "deleteFirst()", "pop()"],
            "answer": "shift()"
        },
        {
            "question": "Which method adds an element to the beginning of an array?",
            "options": ["unshift()", "push()", "prepend()", "addFirst()"],
            "answer": "unshift()"
        },
        {
            "question": "Which method creates a new array by applying a function to each element?",
            "options": ["map()", "filter()", "reduce()", "forEach()"],
            "answer": "map()"
        },
        {
            "question": "Which method creates an array containing elements that pass a test?",
            "options": ["filter()", "map()", "find()", "search()"],
            "answer": "filter()"
        },
        {
            "question": "Which method executes a function for each array element?",
            "options": ["forEach()", "each()", "loop()", "iterate()"],
            "answer": "forEach()"
        },
        {
            "question": "Which method finds the first element that satisfies a condition?",
            "options": ["find()", "search()", "filter()", "locate()"],
            "answer": "find()"
        },
        {
            "question": "Which keyword is used to define a class?",
            "options": ["class", "object", "struct", "define"],
            "answer": "class"
        },
        {
            "question": "Which keyword is used to create an object?",
            "options": ["new", "create", "object", "make"],
            "answer": "new"
        },
        {
            "question": "Which keyword refers to the current object?",
            "options": ["this", "self", "current", "object"],
            "answer": "this"
        },
        {
            "question": "Which keyword is used to define a function?",
            "options": ["function", "def", "fun", "method"],
            "answer": "function"
        },
        {
            "question": "Which type of function has no name?",
            "options": ["Anonymous function", "Main function", "Default function", "Private function"],
            "answer": "Anonymous function"
        },
        {
            "question": "What is an arrow function represented by?",
            "options": ["=>", "->", "::", "==>"],
            "answer": "=>"
        },
        {
            "question": "Which statement is used to make a decision?",
            "options": ["if", "for", "while", "switchOnly"],
            "answer": "if"
        },
        {
            "question": "Which statement is used for multiple possible cases?",
            "options": ["switch", "multiple", "choose", "select"],
            "answer": "switch"
        },
        {
            "question": "Which keyword is used inside a switch statement?",
            "options": ["case", "option", "choice", "condition"],
            "answer": "case"
        },
        {
            "question": "Which keyword stops execution of a switch case?",
            "options": ["break", "stop", "exit", "end"],
            "answer": "break"
        },
        {
            "question": "Which loop repeats while a condition is true?",
            "options": ["while", "repeat", "loop", "during"],
            "answer": "while"
        },
        {
            "question": "Which loop executes its body at least once?",
            "options": ["do...while", "while", "for", "foreach"],
            "answer": "do...while"
        },
        {
            "question": "Which keyword skips the current loop iteration?",
            "options": ["continue", "skip", "next", "pass"],
            "answer": "continue"
        },
        {
            "question": "Which method converts JSON text into a JavaScript object?",
            "options": ["JSON.parse()", "JSON.convert()", "JSON.object()", "JSON.read()"],
            "answer": "JSON.parse()"
        },
        {
            "question": "Which method converts a JavaScript object into JSON text?",
            "options": ["JSON.stringify()", "JSON.convert()", "JSON.text()", "JSON.encode()"],
            "answer": "JSON.stringify()"
        },
        {
            "question": "Which object represents the browser window?",
            "options": ["window", "browser", "screen", "document"],
            "answer": "window"
        },
        {
            "question": "Which object represents the HTML document?",
            "options": ["document", "html", "page", "window"],
            "answer": "document"
        }
    ],


    "HTML": [
        {
            "question": "HTML stands for ______.",
            "options": [
                "Hyper Text Markup Language",
                "High Text Machine Language",
                "Hyperlink Text Markup Language",
                "Home Tool Markup Language"
            ],
            "answer": "Hyper Text Markup Language"
        },
        {
            "question": "Which tag is used to create a paragraph?",
            "options": ["<p>", "<para>", "<text>", "<paragraph>"],
            "answer": "<p>"
        },
        {
            "question": "Which tag is used to create a hyperlink?",
            "options": ["<a>", "<link>", "<href>", "<url>"],
            "answer": "<a>"
        },
        {
            "question": "Which tag is used to display an image?",
            "options": ["<img>", "<image>", "<src>", "<pic>"],
            "answer": "<img>"
        },
        {
            "question": "Which tag is used for the largest heading?",
            "options": ["<h1>", "<h6>", "<head>", "<heading>"],
            "answer": "<h1>"
        },
        {
            "question": "Which tag is used to create an unordered list?",
            "options": ["<ul>", "<ol>", "<li>", "<list>"],
            "answer": "<ul>"
        },
        {
            "question": "Which attribute is used to provide an image path?",
            "options": ["src", "href", "link", "path"],
            "answer": "src"
        },
        {
            "question": "Which tag is used to create a table row?",
            "options": ["<tr>", "<td>", "<th>", "<row>"],
            "answer": "<tr>"
        },
        {
            "question": "Which tag is used to create a line break?",
            "options": ["<br>", "<break>", "<lb>", "<line>"],
            "answer": "<br>"
        },
        {
            "question": "HTML files usually have which extension?",
            "options": [".html", ".htm", ".web", ".page"],
            "answer": ".html"
        },
                {
            "question": "Which tag is used to create the main heading?",
            "options": ["<h1>", "<heading>", "<head>", "<title>"],
            "answer": "<h1>"
        },
        {
            "question": "Which tag is used to create a horizontal line?",
            "options": ["<hr>", "<line>", "<horizontal>", "<br>"],
            "answer": "<hr>"
        },
        {
            "question": "Which tag is used to make text bold?",
            "options": ["<b>", "<bold>", "<stronger>", "<bl>"],
            "answer": "<b>"
        },
        {
            "question": "Which tag gives strong importance to text?",
            "options": ["<strong>", "<important>", "<bolder>", "<em>"],
            "answer": "<strong>"
        },
        {
            "question": "Which tag is used to italicize text?",
            "options": ["<i>", "<italic>", "<it>", "<emphasis>"],
            "answer": "<i>"
        },
        {
            "question": "Which tag is used for emphasized text?",
            "options": ["<em>", "<i>", "<strong>", "<italic>"],
            "answer": "<em>"
        },
        {
            "question": "Which tag is used to create an ordered list?",
            "options": ["<ol>", "<ul>", "<li>", "<list>"],
            "answer": "<ol>"
        },
        {
            "question": "Which tag represents an item in a list?",
            "options": ["<li>", "<item>", "<list>", "<ul>"],
            "answer": "<li>"
        },
        {
            "question": "Which tag is used to create a table?",
            "options": ["<table>", "<tab>", "<tbl>", "<data>"],
            "answer": "<table>"
        },
        {
            "question": "Which tag is used to create a table cell?",
            "options": ["<td>", "<cell>", "<tc>", "<data>"],
            "answer": "<td>"
        },
        {
            "question": "Which tag is used to create a table heading cell?",
            "options": ["<th>", "<thead>", "<heading>", "<td>"],
            "answer": "<th>"
        },
        {
            "question": "Which tag defines the table header section?",
            "options": ["<thead>", "<header>", "<th>", "<head>"],
            "answer": "<thead>"
        },
        {
            "question": "Which tag defines the table body?",
            "options": ["<tbody>", "<body>", "<tablebody>", "<main>"],
            "answer": "<tbody>"
        },
        {
            "question": "Which attribute specifies the destination of a hyperlink?",
            "options": ["href", "src", "link", "url"],
            "answer": "href"
        },
        {
            "question": "Which attribute specifies alternative text for an image?",
            "options": ["alt", "title", "text", "description"],
            "answer": "alt"
        },
        {
            "question": "Which attribute specifies the width of an image?",
            "options": ["width", "size", "image-width", "w"],
            "answer": "width"
        },
        {
            "question": "Which attribute specifies the height of an image?",
            "options": ["height", "size", "image-height", "h"],
            "answer": "height"
        },
        {
            "question": "Which tag is used to create a form?",
            "options": ["<form>", "<input>", "<fieldset>", "<data>"],
            "answer": "<form>"
        },
        {
            "question": "Which tag is used to accept user input?",
            "options": ["<input>", "<text>", "<field>", "<form-input>"],
            "answer": "<input>"
        },
        {
            "question": "Which input type is used for passwords?",
            "options": ["password", "pass", "secure", "hidden-password"],
            "answer": "password"
        },
        {
            "question": "Which input type is used for selecting one option?",
            "options": ["radio", "checkbox", "select", "option"],
            "answer": "radio"
        },
        {
            "question": "Which input type allows multiple selections?",
            "options": ["checkbox", "radio", "multiple", "select"],
            "answer": "checkbox"
        },
        {
            "question": "Which tag creates a drop-down list?",
            "options": ["<select>", "<dropdown>", "<list>", "<option>"],
            "answer": "<select>"
        },
        {
            "question": "Which tag defines an option inside a select list?",
            "options": ["<option>", "<choice>", "<select-option>", "<item>"],
            "answer": "<option>"
        },
        {
            "question": "Which tag creates a multi-line text input?",
            "options": ["<textarea>", "<textbox>", "<input-area>", "<text>"],
            "answer": "<textarea>"
        },
        {
            "question": "Which tag is used to create a button?",
            "options": ["<button>", "<btn>", "<click>", "<input-button>"],
            "answer": "<button>"
        },
        {
            "question": "Which attribute specifies where form data is sent?",
            "options": ["action", "method", "target", "send"],
            "answer": "action"
        },
        {
            "question": "Which attribute specifies the HTTP method of a form?",
            "options": ["method", "action", "type", "request"],
            "answer": "method"
        },
        {
            "question": "Which tag contains metadata about an HTML document?",
            "options": ["<head>", "<meta>", "<header>", "<info>"],
            "answer": "<head>"
        },
        {
            "question": "Which tag defines the visible content of a webpage?",
            "options": ["<body>", "<main>", "<content>", "<page>"],
            "answer": "<body>"
        },
        {
            "question": "Which tag defines the title shown in the browser tab?",
            "options": ["<title>", "<head>", "<heading>", "<tab-title>"],
            "answer": "<title>"
        },
        {
            "question": "Which tag is used to link an external CSS file?",
            "options": ["<link>", "<css>", "<style>", "<stylesheet>"],
            "answer": "<link>"
        },
        {
            "question": "Which tag is used to write internal CSS?",
            "options": ["<style>", "<css>", "<design>", "<stylesheet>"],
            "answer": "<style>"
        },
        {
            "question": "Which tag is used to include JavaScript?",
            "options": ["<script>", "<javascript>", "<js>", "<code>"],
            "answer": "<script>"
        },
        {
            "question": "Which tag is used to define a navigation section?",
            "options": ["<nav>", "<navigation>", "<menu>", "<links>"],
            "answer": "<nav>"
        },
        {
            "question": "Which semantic tag represents the main content?",
            "options": ["<main>", "<content>", "<section>", "<body>"],
            "answer": "<main>"
        },
        {
            "question": "Which tag represents an independent article?",
            "options": ["<article>", "<post>", "<content>", "<section>"],
            "answer": "<article>"
        },
        {
            "question": "Which tag is used to group related content?",
            "options": ["<section>", "<group>", "<div>", "<content>"],
            "answer": "<section>"
        },
        {
            "question": "Which tag is a generic block-level container?",
            "options": ["<div>", "<span>", "<container>", "<block>"],
            "answer": "<div>"
        },
        {
            "question": "Which tag is a generic inline container?",
            "options": ["<span>", "<div>", "<inline>", "<text>"],
            "answer": "<span>"
        }
    ],


    "SQL Database": [
        {
            "question": "SQL stands for ______.",
            "options": [
                "Structured Query Language",
                "Simple Query Language",
                "System Query Language",
                "Structured Question Language"
            ],
            "answer": "Structured Query Language"
        },
        {
            "question": "Which command is used to retrieve data from a database?",
            "options": ["SELECT", "GET", "FETCH", "SHOW"],
            "answer": "SELECT"
        },
        {
            "question": "Which command is used to add new data?",
            "options": ["INSERT", "ADD", "CREATE", "PUT"],
            "answer": "INSERT"
        },
        {
            "question": "Which command is used to modify existing data?",
            "options": ["UPDATE", "MODIFY", "CHANGE", "ALTER"],
            "answer": "UPDATE"
        },
        {
            "question": "Which command is used to remove data from a table?",
            "options": ["DELETE", "REMOVE", "DROP", "CLEAR"],
            "answer": "DELETE"
        },
        {
            "question": "Which keyword is used to filter records?",
            "options": ["WHERE", "FILTER", "IF", "CHECK"],
            "answer": "WHERE"
        },
        {
            "question": "Which key uniquely identifies each record?",
            "options": ["Primary Key", "Foreign Key", "Candidate Key", "Super Key"],
            "answer": "Primary Key"
        },
        {
            "question": "Which command is used to create a table?",
            "options": ["CREATE TABLE", "MAKE TABLE", "NEW TABLE", "ADD TABLE"],
            "answer": "CREATE TABLE"
        },
        {
            "question": "Which SQL command is used to remove a table?",
            "options": ["DROP TABLE", "DELETE TABLE", "REMOVE TABLE", "CLEAR TABLE"],
            "answer": "DROP TABLE"
        },
        {
            "question": "Which clause is used to sort query results?",
            "options": ["ORDER BY", "SORT BY", "GROUP BY", "ARRANGE BY"],
            "answer": "ORDER BY"
        },
                {
            "question": "Which SQL command is used to create a database?",
            "options": ["CREATE DATABASE", "NEW DATABASE", "MAKE DATABASE", "ADD DATABASE"],
            "answer": "CREATE DATABASE"
        },
        {
            "question": "Which SQL command is used to select a database?",
            "options": ["USE", "SELECT DATABASE", "OPEN", "CHOOSE"],
            "answer": "USE"
        },
        {
            "question": "Which SQL command is used to create a new table?",
            "options": ["CREATE TABLE", "NEW TABLE", "MAKE TABLE", "ADD TABLE"],
            "answer": "CREATE TABLE"
        },
        {
            "question": "Which SQL command is used to change the structure of a table?",
            "options": ["ALTER TABLE", "CHANGE TABLE", "UPDATE TABLE", "MODIFY TABLE"],
            "answer": "ALTER TABLE"
        },
        {
            "question": "Which SQL command is used to remove a database?",
            "options": ["DROP DATABASE", "DELETE DATABASE", "REMOVE DATABASE", "CLEAR DATABASE"],
            "answer": "DROP DATABASE"
        },
        {
            "question": "Which SQL command is used to remove all records from a table while keeping the table?",
            "options": ["TRUNCATE", "DELETE TABLE", "DROP", "CLEAR"],
            "answer": "TRUNCATE"
        },
        {
            "question": "Which clause is used to specify a condition?",
            "options": ["WHERE", "WHEN", "IF", "CONDITION"],
            "answer": "WHERE"
        },
        {
            "question": "Which keyword is used to return only unique values?",
            "options": ["DISTINCT", "UNIQUE", "ONLY", "DIFFERENT"],
            "answer": "DISTINCT"
        },
        {
            "question": "Which clause is used to group rows with the same values?",
            "options": ["GROUP BY", "ORDER BY", "SORT BY", "COLLECT BY"],
            "answer": "GROUP BY"
        },
        {
            "question": "Which clause is used to filter grouped records?",
            "options": ["HAVING", "WHERE", "FILTER", "GROUP"],
            "answer": "HAVING"
        },
        {
            "question": "Which keyword is used to sort data in ascending or descending order?",
            "options": ["ORDER BY", "SORT", "ARRANGE", "GROUP BY"],
            "answer": "ORDER BY"
        },
        {
            "question": "Which keyword is used for ascending order?",
            "options": ["ASC", "UP", "ASCENDING", "A-Z"],
            "answer": "ASC"
        },
        {
            "question": "Which keyword is used for descending order?",
            "options": ["DESC", "DOWN", "DESCENDING", "Z-A"],
            "answer": "DESC"
        },
        {
            "question": "Which function counts the number of rows?",
            "options": ["COUNT()", "NUMBER()", "TOTAL()", "ROWS()"],
            "answer": "COUNT()"
        },
        {
            "question": "Which function calculates the average value?",
            "options": ["AVG()", "AVERAGE()", "MEAN()", "MID()"],
            "answer": "AVG()"
        },
        {
            "question": "Which function returns the largest value?",
            "options": ["MAX()", "LARGE()", "HIGH()", "TOP()"],
            "answer": "MAX()"
        },
        {
            "question": "Which function returns the smallest value?",
            "options": ["MIN()", "SMALL()", "LOW()", "BOTTOM()"],
            "answer": "MIN()"
        },
        {
            "question": "Which function calculates the total of numeric values?",
            "options": ["SUM()", "TOTAL()", "ADD()", "COUNT()"],
            "answer": "SUM()"
        },
        {
            "question": "Which key is used to uniquely identify each row?",
            "options": ["Primary Key", "Foreign Key", "Secondary Key", "Unique Row"],
            "answer": "Primary Key"
        },
        {
            "question": "Which key creates a relationship between two tables?",
            "options": ["Foreign Key", "Primary Key", "Main Key", "Reference Key"],
            "answer": "Foreign Key"
        },
        {
            "question": "Which constraint prevents NULL values?",
            "options": ["NOT NULL", "NO NULL", "REQUIRED", "NOT EMPTY"],
            "answer": "NOT NULL"
        },
        {
            "question": "Which constraint ensures all values are different?",
            "options": ["UNIQUE", "DISTINCT", "DIFFERENT", "ONLY"],
            "answer": "UNIQUE"
        },
        {
            "question": "Which constraint provides a default value?",
            "options": ["DEFAULT", "VALUE", "AUTO", "STANDARD"],
            "answer": "DEFAULT"
        },
        {
            "question": "Which constraint is used to maintain referential integrity?",
            "options": ["FOREIGN KEY", "PRIMARY KEY", "UNIQUE", "CHECK"],
            "answer": "FOREIGN KEY"
        },
        {
            "question": "Which constraint checks whether a value satisfies a condition?",
            "options": ["CHECK", "VALIDATE", "WHERE", "TEST"],
            "answer": "CHECK"
        },
        {
            "question": "Which JOIN returns matching rows from both tables?",
            "options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN"],
            "answer": "INNER JOIN"
        },
        {
            "question": "Which JOIN returns all rows from the left table?",
            "options": ["LEFT JOIN", "INNER JOIN", "RIGHT JOIN", "FULL JOIN"],
            "answer": "LEFT JOIN"
        },
        {
            "question": "Which JOIN returns all rows from the right table?",
            "options": ["RIGHT JOIN", "LEFT JOIN", "INNER JOIN", "FULL JOIN"],
            "answer": "RIGHT JOIN"
        },
        {
            "question": "Which JOIN returns rows from both tables including unmatched rows?",
            "options": ["FULL OUTER JOIN", "INNER JOIN", "LEFT JOIN", "RIGHT JOIN"],
            "answer": "FULL OUTER JOIN"
        },
        {
            "question": "Which operator is used to search for a pattern?",
            "options": ["LIKE", "MATCH", "SEARCH", "FIND"],
            "answer": "LIKE"
        },
        {
            "question": "Which wildcard represents any number of characters with LIKE?",
            "options": ["%", "*", "_", "#"],
            "answer": "%"
        },
        {
            "question": "Which wildcard represents exactly one character with LIKE?",
            "options": ["_", "%", "*", "?"],
            "answer": "_"
        },
        {
            "question": "Which operator is used to specify multiple possible values?",
            "options": ["IN", "MULTI", "ANY", "VALUES"],
            "answer": "IN"
        },
        {
            "question": "Which operator checks whether a value is within a range?",
            "options": ["BETWEEN", "RANGE", "WITHIN", "LIMIT"],
            "answer": "BETWEEN"
        },
        {
            "question": "Which operator is used to combine conditions when both must be true?",
            "options": ["AND", "OR", "BOTH", "WITH"],
            "answer": "AND"
        },
        {
            "question": "Which operator is used when at least one condition must be true?",
            "options": ["OR", "AND", "ANY", "EITHER"],
            "answer": "OR"
        },
        {
            "question": "Which operator is used to reverse a condition?",
            "options": ["NOT", "NO", "REVERSE", "EXCEPT"],
            "answer": "NOT"
        },
        {
            "question": "Which SQL command is used to rename a table in many SQL systems?",
            "options": ["RENAME", "CHANGE", "ALTER NAME", "MODIFY"],
            "answer": "RENAME"
        },
        {
            "question": "Which SQL statement is used to combine results of two SELECT queries?",
            "options": ["UNION", "JOIN", "MERGE", "COMBINE"],
            "answer": "UNION"
        },
        {
            "question": "Which command is used to give privileges to a user?",
            "options": ["GRANT", "ALLOW", "PERMIT", "ACCESS"],
            "answer": "GRANT"
        }
    ],


    "Data Structures": [
        {
            "question": "Which data structure follows LIFO?",
            "options": ["Stack", "Queue", "Array", "Linked List"],
            "answer": "Stack"
        },
        {
            "question": "Which data structure follows FIFO?",
            "options": ["Queue", "Stack", "Tree", "Graph"],
            "answer": "Queue"
        },
        {
            "question": "Which data structure stores elements in a continuous memory location?",
            "options": ["Array", "Stack", "Queue", "Graph"],
            "answer": "Array"
        },
        {
            "question": "Which data structure consists of nodes connected by links?",
            "options": ["Linked List", "Array", "Stack", "Queue"],
            "answer": "Linked List"
        },
        {
            "question": "Which data structure is used in recursion?",
            "options": ["Stack", "Queue", "Array", "Graph"],
            "answer": "Stack"
        },
        {
            "question": "Which data structure is used to represent hierarchical data?",
            "options": ["Tree", "Array", "Stack", "Queue"],
            "answer": "Tree"
        },
        {
            "question": "Which data structure is used to represent networks?",
            "options": ["Graph", "Stack", "Array", "Queue"],
            "answer": "Graph"
        },
        {
            "question": "What is the first element of a linked list called?",
            "options": ["Head", "Root", "Top", "Start"],
            "answer": "Head"
        },
        {
            "question": "Which sorting algorithm repeatedly swaps adjacent elements?",
            "options": ["Bubble Sort", "Merge Sort", "Quick Sort", "Selection Sort"],
            "answer": "Bubble Sort"
        },
        {
            "question": "Which data structure uses a key-value pair?",
            "options": ["Hash Table", "Stack", "Queue", "Array"],
            "answer": "Hash Table"
        },
                {
            "question": "What is the time complexity of accessing an element in an array by index?",
            "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
            "answer": "O(1)"
        },
        {
            "question": "Which data structure uses the principle of LIFO?",
            "options": ["Stack", "Queue", "Tree", "Graph"],
            "answer": "Stack"
        },
        {
            "question": "Which operation adds an element to a stack?",
            "options": ["Push", "Pop", "Enqueue", "Insert"],
            "answer": "Push"
        },
        {
            "question": "Which operation removes an element from a stack?",
            "options": ["Pop", "Push", "Delete", "Dequeue"],
            "answer": "Pop"
        },
        {
            "question": "Which operation adds an element to a queue?",
            "options": ["Enqueue", "Push", "Insert", "Add"],
            "answer": "Enqueue"
        },
        {
            "question": "Which operation removes an element from a queue?",
            "options": ["Dequeue", "Pop", "Delete", "Remove"],
            "answer": "Dequeue"
        },
        {
            "question": "Which data structure is commonly used for BFS?",
            "options": ["Queue", "Stack", "Array", "Tree"],
            "answer": "Queue"
        },
        {
            "question": "Which data structure is commonly used for DFS?",
            "options": ["Stack", "Queue", "Array", "Heap"],
            "answer": "Stack"
        },
        {
            "question": "What is the last node of a linked list called?",
            "options": ["Tail", "Head", "Root", "End"],
            "answer": "Tail"
        },
        {
            "question": "Which linked list has nodes containing next and previous pointers?",
            "options": ["Doubly Linked List", "Singly Linked List", "Circular List", "Linear List"],
            "answer": "Doubly Linked List"
        },
        {
            "question": "Which linked list has the last node connected to the first node?",
            "options": ["Circular Linked List", "Singly Linked List", "Doubly Linked List", "Linear List"],
            "answer": "Circular Linked List"
        },
        {
            "question": "Which data structure is dynamic in size?",
            "options": ["Linked List", "Static Array", "Fixed Array", "Constant"],
            "answer": "Linked List"
        },
        {
            "question": "Which data structure represents hierarchical relationships?",
            "options": ["Tree", "Stack", "Queue", "Array"],
            "answer": "Tree"
        },
        {
            "question": "What is the topmost node of a tree called?",
            "options": ["Root", "Head", "Top", "Parent"],
            "answer": "Root"
        },
        {
            "question": "A node that has no children is called:",
            "options": ["Leaf Node", "Root Node", "Parent Node", "Internal Node"],
            "answer": "Leaf Node"
        },
        {
            "question": "A node that has another node below it is called:",
            "options": ["Parent Node", "Child Node", "Leaf Node", "Root"],
            "answer": "Parent Node"
        },
        {
            "question": "A node directly below another node is called:",
            "options": ["Child Node", "Parent Node", "Root", "Leaf"],
            "answer": "Child Node"
        },
        {
            "question": "A tree where each node has at most two children is called:",
            "options": ["Binary Tree", "AVL Tree", "B-Tree", "Heap"],
            "answer": "Binary Tree"
        },
        {
            "question": "In a binary tree, the maximum number of children of a node is:",
            "options": ["2", "1", "3", "4"],
            "answer": "2"
        },
        {
            "question": "Which traversal visits Root, Left, Right?",
            "options": ["Preorder", "Inorder", "Postorder", "Level Order"],
            "answer": "Preorder"
        },
        {
            "question": "Which traversal visits Left, Root, Right?",
            "options": ["Inorder", "Preorder", "Postorder", "Level Order"],
            "answer": "Inorder"
        },
        {
            "question": "Which traversal visits Left, Right, Root?",
            "options": ["Postorder", "Preorder", "Inorder", "Level Order"],
            "answer": "Postorder"
        },
        {
            "question": "Which tree is useful for maintaining sorted data?",
            "options": ["Binary Search Tree", "Binary Tree", "Heap", "Graph"],
            "answer": "Binary Search Tree"
        },
        {
            "question": "In a Binary Search Tree, smaller values are stored on which side?",
            "options": ["Left", "Right", "Root", "Top"],
            "answer": "Left"
        },
        {
            "question": "In a Binary Search Tree, larger values are stored on which side?",
            "options": ["Right", "Left", "Root", "Bottom"],
            "answer": "Right"
        },
        {
            "question": "Which data structure is used to implement priority queues?",
            "options": ["Heap", "Stack", "Linked List", "Array"],
            "answer": "Heap"
        },
        {
            "question": "Which heap has the largest element at the root?",
            "options": ["Max Heap", "Min Heap", "Binary Tree", "BST"],
            "answer": "Max Heap"
        },
        {
            "question": "Which heap has the smallest element at the root?",
            "options": ["Min Heap", "Max Heap", "BST", "Binary Tree"],
            "answer": "Min Heap"
        },
        {
            "question": "Which data structure is used to represent connections between vertices?",
            "options": ["Graph", "Tree", "Stack", "Queue"],
            "answer": "Graph"
        },
        {
            "question": "In a graph, what are the points called?",
            "options": ["Vertices", "Edges", "Nodes only", "Links"],
            "answer": "Vertices"
        },
        {
            "question": "In a graph, what connects two vertices?",
            "options": ["Edge", "Node", "Root", "Branch"],
            "answer": "Edge"
        },
        {
            "question": "Which graph has edges with direction?",
            "options": ["Directed Graph", "Undirected Graph", "Simple Graph", "Tree"],
            "answer": "Directed Graph"
        },
        {
            "question": "Which graph has edges without direction?",
            "options": ["Undirected Graph", "Directed Graph", "Binary Graph", "Tree"],
            "answer": "Undirected Graph"
        },
        {
            "question": "Which data structure provides key-value mapping?",
            "options": ["Hash Table", "Stack", "Queue", "Array"],
            "answer": "Hash Table"
        },
        {
            "question": "Which technique is used to resolve hash collisions?",
            "options": ["Chaining", "Sorting", "Traversal", "Recursion"],
            "answer": "Chaining"
        },
        {
            "question": "Which sorting algorithm repeatedly compares adjacent elements?",
            "options": ["Bubble Sort", "Selection Sort", "Merge Sort", "Quick Sort"],
            "answer": "Bubble Sort"
        },
        {
            "question": "Which sorting algorithm selects the smallest element repeatedly?",
            "options": ["Selection Sort", "Bubble Sort", "Merge Sort", "Quick Sort"],
            "answer": "Selection Sort"
        },
        {
            "question": "Which sorting algorithm uses divide and conquer?",
            "options": ["Merge Sort", "Bubble Sort", "Selection Sort", "Linear Search"],
            "answer": "Merge Sort"
        },
        {
            "question": "Which sorting algorithm is based on a pivot element?",
            "options": ["Quick Sort", "Bubble Sort", "Selection Sort", "Insertion Sort"],
            "answer": "Quick Sort"
        },
        {
            "question": "Which searching algorithm checks elements one by one?",
            "options": ["Linear Search", "Binary Search", "Hash Search", "Tree Search"],
            "answer": "Linear Search"
        }
    ],


    "Computer Networks": [
        {
            "question": "What does LAN stand for?",
            "options": [
                "Local Area Network",
                "Large Area Network",
                "Long Area Network",
                "Local Access Network"
            ],
            "answer": "Local Area Network"
        },
        {
            "question": "What does WAN stand for?",
            "options": [
                "Wide Area Network",
                "Web Area Network",
                "Wireless Area Network",
                "World Access Network"
            ],
            "answer": "Wide Area Network"
        },
        {
            "question": "Which device connects different networks?",
            "options": ["Router", "Keyboard", "Monitor", "Printer"],
            "answer": "Router"
        },
        {
            "question": "Which protocol is used to browse websites?",
            "options": ["HTTP", "FTP", "SMTP", "TCP"],
            "answer": "HTTP"
        },
        {
            "question": "What does IP stand for?",
            "options": [
                "Internet Protocol",
                "Internet Program",
                "Internal Protocol",
                "Information Protocol"
            ],
            "answer": "Internet Protocol"
        },
        {
            "question": "Which device is used to connect devices in a LAN?",
            "options": ["Switch", "Scanner", "Printer", "Speaker"],
            "answer": "Switch"
        },
        {
            "question": "Which protocol is used to send emails?",
            "options": ["SMTP", "HTTP", "FTP", "DNS"],
            "answer": "SMTP"
        },
        {
            "question": "Which protocol is used to transfer files?",
            "options": ["FTP", "HTTP", "SMTP", "DNS"],
            "answer": "FTP"
        },
        {
            "question": "What does DNS stand for?",
            "options": [
                "Domain Name System",
                "Data Name System",
                "Domain Network Service",
                "Digital Name Service"
            ],
            "answer": "Domain Name System"
        },
        {
            "question": "Which device converts digital and analog signals?",
            "options": ["Modem", "Router", "Switch", "Hub"],
            "answer": "Modem"
        },
                {
            "question": "What is a computer network?",
            "options": [
                "A group of connected computers",
                "A single computer",
                "A programming language",
                "A database"
            ],
            "answer": "A group of connected computers"
        },
        {
            "question": "Which device forwards data packets between networks?",
            "options": ["Router", "Switch", "Hub", "Repeater"],
            "answer": "Router"
        },
        {
            "question": "Which device connects multiple devices in a LAN?",
            "options": ["Switch", "Router", "Modem", "Repeater"],
            "answer": "Switch"
        },
        {
            "question": "Which device broadcasts data to all connected devices?",
            "options": ["Hub", "Router", "Switch", "Bridge"],
            "answer": "Hub"
        },
        {
            "question": "What does MAN stand for?",
            "options": [
                "Metropolitan Area Network",
                "Main Area Network",
                "Medium Area Network",
                "Multiple Area Network"
            ],
            "answer": "Metropolitan Area Network"
        },
        {
            "question": "What does PAN stand for?",
            "options": [
                "Personal Area Network",
                "Private Area Network",
                "Public Area Network",
                "Personal Access Network"
            ],
            "answer": "Personal Area Network"
        },
        {
            "question": "Which network covers the largest geographical area?",
            "options": ["WAN", "LAN", "PAN", "MAN"],
            "answer": "WAN"
        },
        {
            "question": "Which network is usually used within a small building?",
            "options": ["LAN", "WAN", "MAN", "PAN"],
            "answer": "LAN"
        },
        {
            "question": "Which protocol is used to translate domain names into IP addresses?",
            "options": ["DNS", "HTTP", "FTP", "SMTP"],
            "answer": "DNS"
        },
        {
            "question": "What does TCP stand for?",
            "options": [
                "Transmission Control Protocol",
                "Transfer Control Protocol",
                "Transmission Communication Protocol",
                "Transport Communication Protocol"
            ],
            "answer": "Transmission Control Protocol"
        },
        {
            "question": "What does UDP stand for?",
            "options": [
                "User Datagram Protocol",
                "Universal Data Protocol",
                "User Data Program",
                "Unified Datagram Protocol"
            ],
            "answer": "User Datagram Protocol"
        },
        {
            "question": "Which protocol is connection-oriented?",
            "options": ["TCP", "UDP", "IP", "DNS"],
            "answer": "TCP"
        },
        {
            "question": "Which protocol is connectionless?",
            "options": ["UDP", "TCP", "HTTP", "FTP"],
            "answer": "UDP"
        },
        {
            "question": "Which protocol is used to send email?",
            "options": ["SMTP", "POP3", "HTTP", "FTP"],
            "answer": "SMTP"
        },
        {
            "question": "Which protocol is commonly used to receive emails?",
            "options": ["POP3", "SMTP", "HTTP", "FTP"],
            "answer": "POP3"
        },
        {
            "question": "Which protocol is used for secure web browsing?",
            "options": ["HTTPS", "HTTP", "FTP", "SMTP"],
            "answer": "HTTPS"
        },
        {
            "question": "What does HTTPS provide?",
            "options": [
                "Secure communication",
                "Faster hardware",
                "File compression",
                "Database storage"
            ],
            "answer": "Secure communication"
        },
        {
            "question": "Which protocol is used for transferring files?",
            "options": ["FTP", "HTTP", "SMTP", "DNS"],
            "answer": "FTP"
        },
        {
            "question": "What is an IP address?",
            "options": [
                "A unique address assigned to a device on a network",
                "A website name",
                "A password",
                "A programming language"
            ],
            "answer": "A unique address assigned to a device on a network"
        },
        {
            "question": "Which version of IP uses 32-bit addresses?",
            "options": ["IPv4", "IPv6", "IPv5", "IPv2"],
            "answer": "IPv4"
        },
        {
            "question": "Which version of IP uses 128-bit addresses?",
            "options": ["IPv6", "IPv4", "IPv5", "IPv2"],
            "answer": "IPv6"
        },
        {
            "question": "How many bits are there in an IPv4 address?",
            "options": ["32", "64", "128", "16"],
            "answer": "32"
        },
        {
            "question": "How many bits are there in an IPv6 address?",
            "options": ["128", "32", "64", "256"],
            "answer": "128"
        },
        {
            "question": "Which layer of the OSI model is responsible for routing?",
            "options": ["Network Layer", "Transport Layer", "Data Link Layer", "Physical Layer"],
            "answer": "Network Layer"
        },
        {
            "question": "How many layers are there in the OSI model?",
            "options": ["7", "5", "6", "8"],
            "answer": "7"
        },
        {
            "question": "Which is the lowest layer of the OSI model?",
            "options": ["Physical Layer", "Network Layer", "Data Link Layer", "Transport Layer"],
            "answer": "Physical Layer"
        },
        {
            "question": "Which is the highest layer of the OSI model?",
            "options": ["Application Layer", "Session Layer", "Transport Layer", "Presentation Layer"],
            "answer": "Application Layer"
        },
        {
            "question": "Which layer is responsible for reliable data delivery?",
            "options": ["Transport Layer", "Network Layer", "Physical Layer", "Application Layer"],
            "answer": "Transport Layer"
        },
        {
            "question": "Which layer is responsible for MAC addressing?",
            "options": ["Data Link Layer", "Network Layer", "Physical Layer", "Transport Layer"],
            "answer": "Data Link Layer"
        },
        {
            "question": "What does MAC stand for?",
            "options": [
                "Media Access Control",
                "Machine Access Control",
                "Media Address Communication",
                "Multiple Access Control"
            ],
            "answer": "Media Access Control"
        },
        {
            "question": "Which device operates mainly at the Data Link Layer?",
            "options": ["Switch", "Router", "Hub", "Repeater"],
            "answer": "Switch"
        },
        {
            "question": "Which device operates mainly at the Network Layer?",
            "options": ["Router", "Switch", "Hub", "Repeater"],
            "answer": "Router"
        },
        {
            "question": "What is network topology?",
            "options": [
                "Arrangement of devices in a network",
                "Network password",
                "Internet speed",
                "Type of software"
            ],
            "answer": "Arrangement of devices in a network"
        },
        {
            "question": "Which topology connects all devices to a central device?",
            "options": ["Star", "Bus", "Ring", "Mesh"],
            "answer": "Star"
        },
        {
            "question": "Which topology uses a single main cable?",
            "options": ["Bus", "Star", "Ring", "Mesh"],
            "answer": "Bus"
        },
        {
            "question": "Which topology connects devices in a circular arrangement?",
            "options": ["Ring", "Star", "Bus", "Mesh"],
            "answer": "Ring"
        },
        {
            "question": "Which topology provides a direct connection between every pair of devices?",
            "options": ["Mesh", "Star", "Bus", "Ring"],
            "answer": "Mesh"
        },
        {
            "question": "What is bandwidth?",
            "options": [
                "Maximum amount of data that can be transmitted",
                "Network password",
                "IP address",
                "Type of cable"
            ],
            "answer": "Maximum amount of data that can be transmitted"
        },
        {
            "question": "What is network latency?",
            "options": [
                "Delay in data transmission",
                "Amount of storage",
                "Network speed",
                "Number of devices"
            ],
            "answer": "Delay in data transmission"
        },
        {
            "question": "Which technology provides wireless network connectivity?",
            "options": ["Wi-Fi", "Ethernet", "USB", "HDMI"],
            "answer": "Wi-Fi"
        }
    ],


    "Operating System": [
        {
            "question": "Which of the following is an operating system?",
            "options": ["Windows", "Python", "HTML", "SQL"],
            "answer": "Windows"
        },
        {
            "question": "What is the main function of an operating system?",
            "options": [
                "Manage computer resources",
                "Create websites",
                "Write programs",
                "Browse the internet"
            ],
            "answer": "Manage computer resources"
        },
        {
            "question": "Which operating system is developed by Microsoft?",
            "options": ["Windows", "Linux", "Android", "macOS"],
            "answer": "Windows"
        },
        {
            "question": "Which operating system is open source?",
            "options": ["Linux", "Windows", "iOS", "macOS"],
            "answer": "Linux"
        },
        {
            "question": "Which part of an OS manages processes?",
            "options": ["Process Manager", "File Manager", "Browser", "Compiler"],
            "answer": "Process Manager"
        },
        {
            "question": "Which part of an OS manages files?",
            "options": ["File Manager", "Process Manager", "CPU", "RAM"],
            "answer": "File Manager"
        },
        {
            "question": "What is the core of an operating system called?",
            "options": ["Kernel", "Shell", "Compiler", "Driver"],
            "answer": "Kernel"
        },
        {
            "question": "Which OS is commonly used on smartphones?",
            "options": ["Android", "Windows", "Linux", "DOS"],
            "answer": "Android"
        },
        {
            "question": "What is multitasking?",
            "options": [
                "Running multiple tasks at the same time",
                "Running one task only",
                "Deleting files",
                "Starting the computer"
            ],
            "answer": "Running multiple tasks at the same time"
        },
        {
            "question": "Which of these is an example of system software?",
            "options": ["Operating System", "MS Word", "Chrome", "Calculator"],
            "answer": "Operating System"
        },
                {
            "question": "What is an operating system?",
            "options": [
                "System software that manages computer resources",
                "A programming language",
                "A web browser",
                "A database"
            ],
            "answer": "System software that manages computer resources"
        },
        {
            "question": "Which of the following is an example of an operating system?",
            "options": ["Linux", "Python", "HTML", "MySQL"],
            "answer": "Linux"
        },
        {
            "question": "Which operating system is developed by Apple?",
            "options": ["macOS", "Windows", "Linux", "Ubuntu"],
            "answer": "macOS"
        },
        {
            "question": "Which operating system is developed by Google for mobile devices?",
            "options": ["Android", "Windows", "Linux", "macOS"],
            "answer": "Android"
        },
        {
            "question": "Which operating system is open-source?",
            "options": ["Linux", "Windows", "macOS", "iOS"],
            "answer": "Linux"
        },
        {
            "question": "What is the core component of an operating system?",
            "options": ["Kernel", "Shell", "Browser", "Compiler"],
            "answer": "Kernel"
        },
        {
            "question": "Which component manages the hardware and software resources?",
            "options": ["Operating System", "Browser", "Compiler", "Text Editor"],
            "answer": "Operating System"
        },
        {
            "question": "What is a process?",
            "options": [
                "A program in execution",
                "A stored file",
                "A hardware device",
                "A folder"
            ],
            "answer": "A program in execution"
        },
        {
            "question": "Which component of an OS manages processes?",
            "options": ["Process Manager", "File Manager", "Device Manager", "Memory Manager"],
            "answer": "Process Manager"
        },
        {
            "question": "Which component manages the main memory?",
            "options": ["Memory Manager", "File Manager", "Process Manager", "Compiler"],
            "answer": "Memory Manager"
        },
        {
            "question": "Which component manages files and directories?",
            "options": ["File Manager", "Process Manager", "Memory Manager", "CPU Manager"],
            "answer": "File Manager"
        },
        {
            "question": "What is multitasking?",
            "options": [
                "Running multiple tasks at the same time",
                "Running only one program",
                "Deleting multiple files",
                "Installing multiple operating systems"
            ],
            "answer": "Running multiple tasks at the same time"
        },
        {
            "question": "What is multiprocessing?",
            "options": [
                "Using multiple processors to execute tasks",
                "Running one program",
                "Managing files",
                "Connecting computers"
            ],
            "answer": "Using multiple processors to execute tasks"
        },
        {
            "question": "What is multithreading?",
            "options": [
                "Executing multiple threads within a process",
                "Running multiple operating systems",
                "Managing memory",
                "Creating multiple files"
            ],
            "answer": "Executing multiple threads within a process"
        },
        {
            "question": "What is a thread?",
            "options": [
                "A lightweight unit of execution",
                "A type of file",
                "A hardware device",
                "A memory location"
            ],
            "answer": "A lightweight unit of execution"
        },
        {
            "question": "Which scheduling algorithm executes processes in the order they arrive?",
            "options": [
                "FCFS",
                "Round Robin",
                "SJF",
                "Priority"
            ],
            "answer": "FCFS"
        },
        {
            "question": "What does FCFS stand for?",
            "options": [
                "First Come First Served",
                "First Computer First System",
                "Fast Come Fast Serve",
                "First Control First Service"
            ],
            "answer": "First Come First Served"
        },
        {
            "question": "Which scheduling algorithm selects the shortest job first?",
            "options": [
                "SJF",
                "FCFS",
                "Round Robin",
                "Priority"
            ],
            "answer": "SJF"
        },
        {
            "question": "Which scheduling algorithm uses a time quantum?",
            "options": [
                "Round Robin",
                "FCFS",
                "SJF",
                "Priority"
            ],
            "answer": "Round Robin"
        },
        {
            "question": "Which scheduling algorithm assigns priority to each process?",
            "options": [
                "Priority Scheduling",
                "FCFS",
                "Round Robin",
                "FIFO"
            ],
            "answer": "Priority Scheduling"
        },
        {
            "question": "What is deadlock?",
            "options": [
                "A situation where processes wait indefinitely for resources",
                "A system shutdown",
                "A memory error",
                "A file deletion"
            ],
            "answer": "A situation where processes wait indefinitely for resources"
        },
        {
            "question": "Which condition is required for deadlock?",
            "options": [
                "Mutual Exclusion",
                "Compilation",
                "Multitasking",
                "Paging"
            ],
            "answer": "Mutual Exclusion"
        },
        {
            "question": "What is virtual memory?",
            "options": [
                "A technique that uses disk space as an extension of RAM",
                "A type of CPU",
                "A type of software",
                "A network connection"
            ],
            "answer": "A technique that uses disk space as an extension of RAM"
        },
        {
            "question": "What is paging?",
            "options": [
                "A memory management technique",
                "A file management technique",
                "A networking technique",
                "A security technique"
            ],
            "answer": "A memory management technique"
        },
        {
            "question": "What is a page fault?",
            "options": [
                "When a required page is not present in main memory",
                "When a file is deleted",
                "When RAM is damaged",
                "When CPU stops"
            ],
            "answer": "When a required page is not present in main memory"
        },
        {
            "question": "What is RAM?",
            "options": [
                "Random Access Memory",
                "Read Access Memory",
                "Random Application Memory",
                "Read Application Memory"
            ],
            "answer": "Random Access Memory"
        },
        {
            "question": "Which memory is volatile?",
            "options": ["RAM", "ROM", "Hard Disk", "SSD"],
            "answer": "RAM"
        },
        {
            "question": "Which memory is non-volatile?",
            "options": ["ROM", "RAM", "Cache", "Register"],
            "answer": "ROM"
        },
        {
            "question": "What is booting?",
            "options": [
                "Starting a computer and loading the operating system",
                "Deleting the operating system",
                "Installing software",
                "Connecting to the internet"
            ],
            "answer": "Starting a computer and loading the operating system"
        },
        {
            "question": "What is a device driver?",
            "options": [
                "Software that allows the OS to communicate with hardware",
                "A hardware component",
                "A programming language",
                "A database"
            ],
            "answer": "Software that allows the OS to communicate with hardware"
        },
        {
            "question": "Which interface allows users to interact with an OS using commands?",
            "options": [
                "Command Line Interface",
                "Graphical Interface",
                "Touch Interface",
                "Audio Interface"
            ],
            "answer": "Command Line Interface"
        },
        {
            "question": "What does GUI stand for?",
            "options": [
                "Graphical User Interface",
                "General User Interface",
                "Graphical Utility Interface",
                "General Utility Input"
            ],
            "answer": "Graphical User Interface"
        },
        {
            "question": "Which interface uses graphical elements such as icons and windows?",
            "options": ["GUI", "CLI", "API", "BIOS"],
            "answer": "GUI"
        },
        {
            "question": "What is a file system?",
            "options": [
                "A method used by an OS to organize and manage files",
                "A programming language",
                "A network protocol",
                "A type of processor"
            ],
            "answer": "A method used by an OS to organize and manage files"
        },
        {
            "question": "Which operating system is commonly used on servers?",
            "options": ["Linux", "Windows Paint", "MS Word", "Calculator"],
            "answer": "Linux"
        },
        {
            "question": "Which operating system is commonly used on desktop computers?",
            "options": ["Windows", "Android", "iOS", "Embedded OS"],
            "answer": "Windows"
        },
        {
            "question": "What is a real-time operating system?",
            "options": [
                "An OS that responds to events within a specified time",
                "An OS used only for games",
                "An OS without memory",
                "An OS used only for browsing"
            ],
            "answer": "An OS that responds to events within a specified time"
        },
        {
            "question": "Which type of OS is designed for mobile devices?",
            "options": [
                "Mobile Operating System",
                "Batch Operating System",
                "Network Operating System",
                "Mainframe OS"
            ],
            "answer": "Mobile Operating System"
        },
        {
            "question": "Which operating system is commonly used in Apple iPhones?",
            "options": ["iOS", "Android", "Windows", "Linux"],
            "answer": "iOS"
        },
        {
            "question": "What is the main purpose of an operating system?",
            "options": [
                "To manage hardware and software resources",
                "To create only documents",
                "To browse websites",
                "To design images"
            ],
            "answer": "To manage hardware and software resources"
        }
    ]

}
NOTES = {

    # ================= PYTHON =================
    "Python": {
        "title": "Python Short Notes",
        "topics": [
            {
                "heading": "What is Python?",
                "points": [
                    "Python is a high-level programming language.",
                    "It is simple and easy to learn.",
                    "Python is used in web development, AI and data science."
                ]
            },
            {
                "heading": "Variables",
                "points": [
                    "Variables are used to store data.",
                    "Python does not require declaring the variable type."
                ],
                "example": 'name = "Pallavi"\nage = 20'
            },
            {
                "heading": "Data Types",
                "points": [
                    "int → Whole numbers",
                    "float → Decimal numbers",
                    "str → Text",
                    "bool → True or False",
                    "list → Collection of values"
                ]
            },
            {
                "heading": "Functions",
                "points": [
                    "Functions are used to perform a specific task.",
                    "The def keyword is used to define a function."
                ],
                "example": 'def greet():\n    print("Hello")'
            },
            {
                "heading": "Loops",
                "points": [
                    "Loops are used to repeat a block of code.",
                    "Common loops are for and while."
                ]
            },
            {
                "heading": "Conditional Statements",
                "points": [
                    "Conditional statements are used to make decisions.",
                    "Python uses if, elif and else statements."
                ],
                "example": 'if age >= 18:\n    print("Adult")\nelse:\n    print("Minor")'
            },
            {
                "heading": "Lists",
                "points": [
                    "A list stores multiple values.",
                    "Lists are ordered and changeable.",
                    "List indexing starts from 0."
                ],
                "example": 'marks = [80, 75, 90, 85]'
            },
            {
                "heading": "Tuples",
                "points": [
                    "A tuple stores multiple values.",
                    "Tuples are ordered.",
                    "Tuples cannot be changed after creation."
                ],
                "example": 'numbers = (10, 20, 30)'
            },
            {
                "heading": "Dictionaries",
                "points": [
                    "A dictionary stores data in key-value pairs.",
                    "Dictionaries are written using curly brackets.",
                    "Keys are used to access values."
                ],
                "example": 'student = {"name": "Pallavi", "age": 20}'
            },
            {
                "heading": "Exception Handling",
                "points": [
                    "Exception handling manages runtime errors.",
                    "Python uses try and except blocks.",
                    "It prevents the program from stopping unexpectedly."
                ],
                "example": 'try:\n    x = 10 / 0\nexcept:\n    print("Error")'
            }
        ]
    },


    # ================= C =================
    "C": {
        "title": "C Programming Short Notes",
        "topics": [
            {
                "heading": "What is C?",
                "points": [
                    "C is a general-purpose programming language.",
                    "It was developed by Dennis Ritchie.",
                    "C is widely used for system programming."
                ]
            },
            {
                "heading": "Basic Structure",
                "points": [
                    "Every C program generally starts execution from main().",
                    "Statements usually end with a semicolon."
                ],
                "example": '#include <stdio.h>\n\nint main() {\n    printf("Hello");\n    return 0;\n}'
            },
            {
                "heading": "Data Types",
                "points": [
                    "int → Integer values",
                    "float → Decimal values",
                    "char → Single character",
                    "double → Double precision decimal"
                ]
            },
            {
                "heading": "Operators",
                "points": [
                    "+ → Addition",
                    "- → Subtraction",
                    "* → Multiplication",
                    "/ → Division",
                    "% → Modulus"
                ]
            },
            {
                "heading": "Conditional Statements",
                "points": [
                    "if is used to check a condition.",
                    "else is executed when the condition is false.",
                    "switch is used for multiple choices."
                ],
                "example": 'if (age >= 18) {\n    printf("Adult");\n} else {\n    printf("Minor");\n}'
            },
            {
                "heading": "Loops",
                "points": [
                    "Loops repeat a block of code.",
                    "Common loops are for, while and do-while."
                ],
                "example": 'for(int i = 1; i <= 5; i++) {\n    printf("%d", i);\n}'
            },
            {
                "heading": "Arrays",
                "points": [
                    "An array stores multiple values of the same type.",
                    "Array indexing starts from 0.",
                    "Array size is fixed."
                ],
                "example": 'int marks[5] = {80, 75, 90, 85, 70};'
            },
            {
                "heading": "Pointers",
                "points": [
                    "A pointer stores the address of another variable.",
                    "The * symbol is used to declare a pointer.",
                    "The & operator gives the address of a variable."
                ],
                "example": 'int age = 20;\nint *p = &age;'
            },
            {
                "heading": "Functions",
                "points": [
                    "Functions are used to divide a program into smaller parts.",
                    "They improve code reusability.",
                    "A function can accept arguments and return a value."
                ],
                "example": 'int add(int a, int b) {\n    return a + b;\n}'
            },
            {
                "heading": "Structures",
                "points": [
                    "A structure groups different types of data.",
                    "The struct keyword is used to create a structure."
                ],
                "example": 'struct Student {\n    int roll;\n    char name[20];\n};'
            }
        ]
    },


    # ================= C++ =================
    "C++": {
        "title": "C++ Short Notes",
        "topics": [
            {
                "heading": "What is C++?",
                "points": [
                    "C++ is a general-purpose programming language.",
                    "It supports object-oriented programming.",
                    "C++ was developed by Bjarne Stroustrup."
                ]
            },
            {
                "heading": "Class and Object",
                "points": [
                    "A class is a blueprint for creating objects.",
                    "An object is an instance of a class."
                ],
                "example": 'class Student {\npublic:\n    string name;\n};'
            },
            {
                "heading": "OOP Concepts",
                "points": [
                    "Encapsulation",
                    "Inheritance",
                    "Polymorphism",
                    "Abstraction"
                ]
            },
            {
                "heading": "Input and Output",
                "points": [
                    "cin is used to take input.",
                    "cout is used to display output."
                ],
                "example": 'cin >> name;\ncout << name;'
            },
            {
                "heading": "Constructors",
                "points": [
                    "A constructor is a special member function of a class.",
                    "It is automatically called when an object is created.",
                    "A constructor has the same name as the class."
                ],
                "example": 'class Student {\npublic:\n    Student() {\n        cout << "Object Created";\n    }\n};'
            },
            {
                "heading": "Destructors",
                "points": [
                    "A destructor is used to destroy an object.",
                    "It is automatically called when an object is destroyed.",
                    "A destructor uses the ~ symbol."
                ],
                "example": 'class Student {\npublic:\n    ~Student() {\n        cout << "Object Destroyed";\n    }\n};'
            },
            {
                "heading": "Inheritance",
                "points": [
                    "Inheritance allows a class to acquire properties of another class.",
                    "It supports code reusability.",
                    "The derived class inherits members from the base class."
                ],
                "example": 'class Child : public Parent {\n};'
            },
            {
                "heading": "Polymorphism",
                "points": [
                    "Polymorphism means one name with many forms.",
                    "It allows the same function or operator to behave differently.",
                    "Function overloading is an example of polymorphism."
                ]
            },
            {
                "heading": "Encapsulation",
                "points": [
                    "Encapsulation means wrapping data and functions into a single unit.",
                    "A class is commonly used to achieve encapsulation.",
                    "Access specifiers control access to class members."
                ]
            },
            {
                "heading": "Templates",
                "points": [
                    "Templates allow writing generic and reusable code.",
                    "They can work with different data types.",
                    "Function and class templates are commonly used."
                ],
                "example": 'template <class T>\nT add(T a, T b) {\n    return a + b;\n}'
            }
        ]
    },


    # ================= JAVA =================
    "Java": {
        "title": "Java Short Notes",
        "topics": [
            {
                "heading": "What is Java?",
                "points": [
                    "Java is an object-oriented programming language.",
                    "Java was developed by James Gosling.",
                    "Java programs run on the JVM."
                ]
            },
            {
                "heading": "Class and Object",
                "points": [
                    "A class defines properties and methods.",
                    "Objects are created using the new keyword."
                ]
            },
            {
                "heading": "Inheritance",
                "points": [
                    "Inheritance allows one class to acquire properties of another class.",
                    "The extends keyword is used for class inheritance."
                ]
            },
            {
                "heading": "Main Method",
                "points": [
                    "The main() method is the starting point of a Java application."
                ],
                "example": 'public static void main(String[] args) {\n    System.out.println("Hello");\n}'
            },
            {
                "heading": "Data Types",
                "points": [
                    "Java has primitive and non-primitive data types.",
                    "Common primitive types are int, float, double, char and boolean.",
                    "Reference types include classes, arrays and interfaces."
                ],
                "example": "int age = 20;\ndouble marks = 85.5;\nchar grade = 'A';"
            },
            {
                "heading": "Variables",
                "points": [
                    "Variables are used to store data.",
                    "Every variable has a data type.",
                    "The value of a variable can be changed during program execution."
                ],
                "example": 'int age = 20;\nString name = "Pallavi";'
            },
            {
                "heading": "Methods",
                "points": [
                    "Methods are blocks of code used to perform a specific task.",
                    "A method can accept parameters.",
                    "A method can return a value."
                ],
                "example": 'static int add(int a, int b) {\n    return a + b;\n}'
            },
            {
                "heading": "Exception Handling",
                "points": [
                    "Exception handling is used to handle runtime errors.",
                    "Java uses try, catch and finally.",
                    "It helps prevent abnormal termination."
                ],
                "example": 'try {\n    int x = 10 / 0;\n} catch (Exception e) {\n    System.out.println("Error");\n}'
            },
            {
                "heading": "Interfaces",
                "points": [
                    "An interface defines methods that a class can implement.",
                    "Interfaces support abstraction.",
                    "The implements keyword is used."
                ],
                "example": 'interface Animal {\n    void sound();\n}'
            },
            {
                "heading": "Arrays",
                "points": [
                    "An array stores multiple values of the same data type.",
                    "Array indexing starts from 0.",
                    "The size of an array is fixed after creation."
                ],
                "example": 'int marks[] = {80, 75, 90, 85, 70};'
            }
        ]
    },


    # ================= JAVASCRIPT =================
    "JavaScript": {
        "title": "JavaScript Short Notes",
        "topics": [
            {
                "heading": "What is JavaScript?",
                "points": [
                    "JavaScript is mainly used for web development.",
                    "It makes web pages interactive."
                ]
            },
            {
                "heading": "Variables",
                "points": [
                    "var, let and const are used to declare variables.",
                    "let and const are commonly used in modern JavaScript."
                ],
                "example": 'let name = "Pallavi";\nconst age = 20;'
            },
            {
                "heading": "Functions",
                "points": [
                    "Functions are reusable blocks of code.",
                    "The function keyword can be used to define a function."
                ]
            },
            {
                "heading": "DOM",
                "points": [
                    "DOM stands for Document Object Model.",
                    "JavaScript can use the DOM to change HTML elements."
                ]
            },
            {
                "heading": "Data Types",
                "points": [
                    "JavaScript has primitive and non-primitive data types.",
                    "Common data types include string, number, boolean, undefined and null."
                ],
                "example": 'let name = "Pallavi";\nlet age = 20;\nlet passed = true;'
            },
            {
                "heading": "Conditional Statements",
                "points": [
                    "Conditional statements are used to make decisions.",
                    "JavaScript provides if, else if and else."
                ],
                "example": 'if (age >= 18) {\n    console.log("Adult");\n} else {\n    console.log("Minor");\n}'
            },
            {
                "heading": "Loops",
                "points": [
                    "Loops are used to repeat a block of code.",
                    "Common loops include for, while and do-while."
                ],
                "example": 'for (let i = 1; i <= 5; i++) {\n    console.log(i);\n}'
            },
            {
                "heading": "Arrays",
                "points": [
                    "An array stores multiple values in a single variable.",
                    "Array indexing starts from 0."
                ],
                "example": 'let fruits = ["Apple", "Mango", "Banana"];'
            },
            {
                "heading": "Objects",
                "points": [
                    "Objects store data in key-value pairs.",
                    "Objects are used to represent real-world entities."
                ],
                "example": 'let student = {\n    name: "Pallavi",\n    age: 20\n};'
            },
            {
                "heading": "Events",
                "points": [
                    "Events are actions that happen on a web page.",
                    "Examples include click, mouseover and keypress."
                ],
                "example": 'button.addEventListener("click", function() {\n    alert("Button clicked");\n});'
            }
        ]
    },


    # ================= HTML =================
    "HTML": {
        "title": "HTML Short Notes",
        "topics": [
            {
                "heading": "What is HTML?",
                "points": [
                    "HTML stands for Hyper Text Markup Language.",
                    "It is used to create the structure of web pages."
                ]
            },
            {
                "heading": "Common Tags",
                "points": [
                    "<h1> → Heading",
                    "<p> → Paragraph",
                    "<a> → Hyperlink",
                    "<img> → Image",
                    "<br> → Line break"
                ]
            },
            {
                "heading": "Lists",
                "points": [
                    "<ul> is used for unordered lists.",
                    "<ol> is used for ordered lists.",
                    "<li> is used for list items."
                ]
            },
            {
                "heading": "Tables",
                "points": [
                    "<table> creates a table.",
                    "<tr> creates a table row.",
                    "<td> creates a table cell.",
                    "<th> creates a heading cell."
                ]
            },
            {
                "heading": "Forms",
                "points": [
                    "HTML forms are used to collect information from users.",
                    "The <form> tag is used to create a form.",
                    "Common elements include input, textarea, select and button."
                ],
                "example": '<form>\n    <input type="text" placeholder="Enter Name">\n    <button type="submit">Submit</button>\n</form>'
            },
            {
                "heading": "Attributes",
                "points": [
                    "Attributes provide additional information about HTML elements.",
                    "Attributes are written inside the opening tag.",
                    "Common attributes include id, class, src and href."
                ],
                "example": '<img src="image.jpg" alt="Student Image">'
            },
            {
                "heading": "HTML Links",
                "points": [
                    "The <a> tag is used to create hyperlinks.",
                    "The href attribute specifies the destination URL.",
                    "Links can connect different pages or websites."
                ],
                "example": '<a href="https://example.com">Visit Website</a>'
            },
            {
                "heading": "HTML Semantic Elements",
                "points": [
                    "Semantic elements clearly describe their purpose.",
                    "Examples include header, nav, section, article and footer.",
                    "They make HTML structure easier to understand."
                ],
                "example": '<header>My Website</header>\n<section>Welcome</section>\n<footer>Copyright</footer>'
            },
            {
                "heading": "Audio and Video",
                "points": [
                    "HTML provides audio and video elements for multimedia.",
                    "The <audio> tag is used to add audio.",
                    "The <video> tag is used to add videos."
                ],
                "example": '<audio controls>\n    <source src="song.mp3">\n</audio>'
            },
            {
                "heading": "HTML Comments",
                "points": [
                    "Comments are used to write notes inside HTML code.",
                    "Comments are not displayed on the web page.",
                    "HTML comments start with <!-- and end with -->."
                ],
                "example": '<!-- This is an HTML comment -->'
            }
        ]
    },


    # ================= SQL =================
    "SQL Database": {
        "title": "SQL Database Short Notes",
        "topics": [
            {
                "heading": "What is SQL?",
                "points": [
                    "SQL stands for Structured Query Language.",
                    "SQL is used to manage and access databases."
                ]
            },
            {
                "heading": "Important Commands",
                "points": [
                    "SELECT → Retrieve data",
                    "INSERT → Add data",
                    "UPDATE → Modify data",
                    "DELETE → Remove data"
                ]
            },
            {
                "heading": "Primary Key",
                "points": [
                    "A primary key uniquely identifies each record.",
                    "A table can have one primary key."
                ]
            },
            {
                "heading": "WHERE Clause",
                "points": [
                    "WHERE is used to filter records.",
                    "It helps retrieve specific data."
                ],
                "example": 'SELECT * FROM students\nWHERE score >= 50;'
            },
            {
                "heading": "SQL Constraints",
                "points": [
                    "Constraints are rules applied to table columns.",
                    "Common constraints include PRIMARY KEY, NOT NULL, UNIQUE and DEFAULT.",
                    "Constraints help maintain data accuracy."
                ],
                "example": 'CREATE TABLE students (\n    id INTEGER PRIMARY KEY,\n    name TEXT NOT NULL\n);'
            },
            {
                "heading": "ORDER BY",
                "points": [
                    "ORDER BY is used to sort query results.",
                    "ASC sorts data in ascending order.",
                    "DESC sorts data in descending order."
                ],
                "example": 'SELECT * FROM students\nORDER BY score DESC;'
            },
            {
                "heading": "GROUP BY",
                "points": [
                    "GROUP BY is used to group rows with similar values.",
                    "It is commonly used with aggregate functions.",
                    "Examples include COUNT, SUM and AVG."
                ],
                "example": 'SELECT subject, COUNT(*)\nFROM students\nGROUP BY subject;'
            },
            {
                "heading": "Aggregate Functions",
                "points": [
                    "Aggregate functions perform calculations on multiple rows.",
                    "Common functions are COUNT, SUM, AVG, MAX and MIN."
                ],
                "example": 'SELECT AVG(score)\nFROM students;'
            },
            {
                "heading": "Joins",
                "points": [
                    "Joins combine data from multiple tables.",
                    "Common joins include INNER JOIN, LEFT JOIN and RIGHT JOIN.",
                    "Joins usually use a related column."
                ],
                "example": 'SELECT students.name, marks.score\nFROM students\nINNER JOIN marks\nON students.id = marks.student_id;'
            },
            {
                "heading": "DELETE and DROP",
                "points": [
                    "DELETE removes records from a table.",
                    "DROP TABLE removes the complete table.",
                    "DELETE can use a WHERE condition."
                ],
                "example": 'DELETE FROM students\nWHERE id = 5;'
            }
        ]
    },


    # ================= DATA STRUCTURES =================
    "Data Structures": {
        "title": "Data Structures Short Notes",
        "topics": [
            {
                "heading": "What are Data Structures?",
                "points": [
                    "Data structures are used to organize and store data.",
                    "They help in efficient data processing."
                ]
            },
            {
                "heading": "Stack",
                "points": [
                    "Stack follows LIFO.",
                    "LIFO means Last In First Out.",
                    "Push and Pop are common stack operations."
                ]
            },
            {
                "heading": "Queue",
                "points": [
                    "Queue follows FIFO.",
                    "FIFO means First In First Out.",
                    "Enqueue and Dequeue are common operations."
                ]
            },
            {
                "heading": "Linked List",
                "points": [
                    "A linked list consists of nodes.",
                    "Each node contains data and a link to another node."
                ]
            },
            {
                "heading": "Arrays",
                "points": [
                    "An array stores multiple elements of the same type.",
                    "Array elements are stored in contiguous memory locations.",
                    "Elements are accessed using an index."
                ],
                "example": 'int marks[5] = {80, 75, 90, 85, 70};'
            },
            {
                "heading": "Trees",
                "points": [
                    "A tree is a hierarchical data structure.",
                    "The top node is called the root.",
                    "Each node can have child nodes."
                ]
            },
            {
                "heading": "Graphs",
                "points": [
                    "A graph consists of vertices and edges.",
                    "Graphs represent relationships and networks.",
                    "Graphs can be directed or undirected."
                ]
            },
            {
                "heading": "Searching",
                "points": [
                    "Searching is the process of finding an element.",
                    "Linear Search checks elements one by one.",
                    "Binary Search works on sorted data."
                ]
            },
            {
                "heading": "Sorting",
                "points": [
                    "Sorting arranges data in a particular order.",
                    "Common algorithms include Bubble Sort, Selection Sort and Merge Sort.",
                    "Sorting can be ascending or descending."
                ]
            },
            {
                "heading": "Hashing",
                "points": [
                    "Hashing is used to store and retrieve data efficiently.",
                    "A hash function converts a key into an index.",
                    "Hash tables store data using key-value pairs."
                ]
            }
        ]
    },


    # ================= COMPUTER NETWORKS =================
    "Computer Networks": {
        "title": "Computer Networks Short Notes",
        "topics": [
            {
                "heading": "What is a Computer Network?",
                "points": [
                    "A network connects computers and other devices.",
                    "It allows devices to communicate and share resources."
                ]
            },
            {
                "heading": "LAN and WAN",
                "points": [
                    "LAN → Local Area Network",
                    "WAN → Wide Area Network",
                    "LAN covers a smaller area while WAN covers a larger area."
                ]
            },
            {
                "heading": "IP Address",
                "points": [
                    "IP stands for Internet Protocol.",
                    "An IP address identifies a device on a network."
                ]
            },
            {
                "heading": "Router",
                "points": [
                    "A router connects different networks.",
                    "It forwards data between networks."
                ]
            },
            {
                "heading": "Network Topologies",
                "points": [
                    "Network topology describes how devices are connected.",
                    "Common topologies include Bus, Star, Ring, Mesh and Tree.",
                    "Star topology commonly uses a central switch or hub."
                ]
            },
            {
                "heading": "OSI Model",
                "points": [
                    "OSI stands for Open Systems Interconnection.",
                    "The OSI model has seven layers.",
                    "The layers are Physical, Data Link, Network, Transport, Session, Presentation and Application."
                ]
            },
            {
                "heading": "TCP and UDP",
                "points": [
                    "TCP stands for Transmission Control Protocol.",
                    "UDP stands for User Datagram Protocol.",
                    "TCP is connection-oriented while UDP is connectionless."
                ]
            },
            {
                "heading": "IP Addressing",
                "points": [
                    "IPv4 uses 32-bit addresses.",
                    "IPv6 uses 128-bit addresses.",
                    "An IP address identifies a device on a network."
                ],
                "example": "IPv4 Example:\n192.168.1.10"
            },
            {
                "heading": "Network Security",
                "points": [
                    "Network security protects data and network resources.",
                    "Firewalls help control network traffic.",
                    "Encryption helps protect data."
                ]
            },
            {
                "heading": "DNS",
                "points": [
                    "DNS stands for Domain Name System.",
                    "DNS converts domain names into IP addresses.",
                    "It makes websites easier to access."
                ],
                "example": "google.com → DNS → IP Address"
            }
        ]
    },


    # ================= OPERATING SYSTEM =================
    "Operating System": {
        "title": "Operating System Short Notes",
        "topics": [
            {
                "heading": "What is an Operating System?",
                "points": [
                    "An operating system manages computer hardware and software resources.",
                    "It provides an interface between the user and computer."
                ]
            },
            {
                "heading": "Examples",
                "points": [
                    "Windows",
                    "Linux",
                    "macOS",
                    "Android"
                ]
            },
            {
                "heading": "Kernel",
                "points": [
                    "Kernel is the core part of an operating system.",
                    "It manages important system resources."
                ]
            },
            {
                "heading": "Multitasking",
                "points": [
                    "Multitasking means running multiple tasks at the same time."
                ]
            },
            {
                "heading": "Process Management",
                "points": [
                    "A process is a program that is currently running.",
                    "The operating system manages the creation and execution of processes.",
                    "Process management helps the CPU handle multiple processes."
                ]
            },
            {
                "heading": "Memory Management",
                "points": [
                    "Memory management controls the use of main memory.",
                    "The operating system allocates memory to processes.",
                    "It also frees memory when it is no longer required."
                ]
            },
            {
                "heading": "File Management",
                "points": [
                    "The operating system manages files and directories.",
                    "It allows users to create, delete, rename and organize files.",
                    "File management helps store and access data efficiently."
                ]
            },
            {
                "heading": "Device Management",
                "points": [
                    "The operating system manages hardware devices.",
                    "Device drivers help the OS communicate with hardware.",
                    "Examples include printers, keyboards, mice and storage devices."
                ]
            },
            {
                "heading": "CPU Scheduling",
                "points": [
                    "CPU scheduling decides which process gets CPU time.",
                    "Scheduling improves CPU utilization and system performance.",
                    "Common algorithms include FCFS, SJF and Round Robin."
                ]
            },
            {
                "heading": "System Calls",
                "points": [
                    "System calls allow programs to request services from the operating system.",
                    "They allow applications to interact with system resources.",
                    "Examples include file operations and process management."
                ],
                "example": "Application\n     ↓\nSystem Call\n     ↓\nOperating System\n     ↓\nHardware"
            }
        ]
    }
}
app.secret_key = "student_quiz_hub"

def init_db():
    conn = get_db()

    # Quiz Records Table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS quiz_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        subject TEXT,
        score INTEGER NOT NULL,
        attempts INTEGER NOT NULL,
        status TEXT
    )
    """)

    # Students Table
    conn.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        students_name TEXT NOT NULL,
        marks INTEGER,
        roll TEXT,
        subject TEXT,
        attendance INTEGER
    )
    """)

    conn.commit()
    conn.close()
def get_db():
    conn = sqlite3.connect("student_quiz_hub.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_status(score):
    if score >= 5:
        return "Pass"
    return "Fail"


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")

#------------student_login--------------
@app.route("/student_login", methods=["GET", "POST"])
def student_login():

    if request.method == "POST":

        student_name = request.form["student_name"]
        password = request.form["password"]

        # Login session
        session["student_name"] = student_name

        return redirect(url_for(
            "subjects",
            student_name=student_name,
            password=password
        ))

    return render_template("student_login.html")
# ---------------- ADMIN LOGIN ----------------

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Admin credentials
        if username == "admin" and password == "1234":

            session["admin_logged_in"] = True

            return redirect(url_for("add_students"))

        flash("Invalid admin username or password!", "danger")

    return render_template("admin_login.html")
# ---------------- STUDENTS ----------------
@app.route("/students")
def students():

    search = request.args.get("search", "")

    conn = get_db()

    if search:
        students = conn.execute(
            """
            SELECT * FROM quiz_records
            WHERE name LIKE ?
            ORDER BY id DESC
            """,
            ('%' + search + '%',)
        ).fetchall()

    else:
        students = conn.execute(
            """
            SELECT * FROM quiz_records
            ORDER BY id DESC
            """
        ).fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=students
    )
# ---------------- ADD STUDENT ----------------
@app.route("/add_students", methods=["GET", "POST"])
def add_students():

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    if request.method == "POST":

        name = request.form["student_name"]
        subject = request.form["subject"]
        score = int(request.form["score"])
        attempts = int(request.form["attempts"])

        status = "Pass" if score >= 5 else "Fail"

        conn = get_db()

        conn.execute("""
            INSERT INTO quiz_records
            (name, subject, score, attempts, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            subject,
            score,
            attempts,
            status
        ))

        conn.commit()
        conn.close()

        flash("Student added successfully!", "success")

        return redirect(url_for("students"))

    return render_template("add_students.html")
# ---------------- SUBJECTS ----------------
@app.route("/subjects")
def subjects():

    if "student_name" not in session:
        return redirect(url_for("student_login"))

    student_name = session["student_name"]

    subjects = [
        "C",
        "C++",
        "Java",
        "Python",
        "JavaScript",
        "HTML",
        "SQL Database",
        "Data Structures",
        "Computer Networks",
        "Operating System"
    ]

    return render_template(
        "subjects.html",
        subjects=subjects,
        student_name=student_name
    )
                   
#-----------------Quiz-------------------------    
@app.route("/quiz/<subject>")
def quiz(subject):

    if "student_name" not in session:
        return redirect(url_for("student_login"))

    student_name = session["student_name"]

    questions = QUIZZES.get(subject)

    return render_template(
        "quiz.html",
        subject=subject,
        questions=questions,
        student_name=student_name
    )
#------------result----------------
@app.route("/result", methods=["POST"])
def result():

    # ================= STUDENT DETAILS =================

    student_id = request.form.get("student_id", "")
    student_name = request.form.get("student_name", "")
    subject = request.form.get("subject", "")


    # ================= GET QUESTIONS =================

    questions = QUIZZES.get(subject, [])


    # ================= CALCULATE SCORE =================

    score = 0

    for i, q in enumerate(questions):

        user_answer = request.form.get(f"q{i}")

        if user_answer == q["answer"]:
            score += 1


    # ================= TOTAL QUESTIONS =================

    total_questions = len(questions)


    # ================= PERCENTAGE =================

    if total_questions > 0:

        percentage = round(
            (score / total_questions) * 100,
            2
        )

    else:

        percentage = 0


    # ================= PASS / FAIL =================

    if percentage >= 50:

        status = "Pass"

    else:

        status = "Fail"


    # ================= GRADE =================

    if percentage >= 90:

        grade = "A+"

    elif percentage >= 80:

        grade = "A"

    elif percentage >= 70:

        grade = "B+"

    elif percentage >= 60:

        grade = "B"

    elif percentage >= 50:

        grade = "C"

    else:

        grade = "F"


    # ================= DATABASE =================

    conn = get_db()


    # Check existing student + subject

    existing = conn.execute(
        """
        SELECT * FROM quiz_records
        WHERE name=? AND subject=?
        """,
        (student_name, subject)
    ).fetchone()


    if existing:

        # Increase attempts

        attempts = existing["attempts"] + 1

        conn.execute(
            """
            UPDATE quiz_records

            SET score=?,
                attempts=?,
                status=?

            WHERE name=? AND subject=?
            """,
            (
                score,
                attempts,
                status,
                student_name,
                subject
            )
        )


    else:

        # New student + subject record

        conn.execute(
            """
            INSERT INTO quiz_records
            (name, subject, score, attempts, status)

            VALUES (?, ?, ?, ?, ?)
            """,
            (
                student_name,
                subject,
                score,
                1,
                status
            )
        )


    conn.commit()
    conn.close()


    # ================= RESULT PAGE =================

    return render_template(
        "result.html",

        student_id=student_id,

        student_name=student_name,

        subject=subject,

        score=score,

        total_questions=total_questions,

        percentage=percentage,

        status=status,

        grade=grade
    )
#-----------------leaderboard----------------
@app.route("/leaderboard")
def leaderboard():

    conn = get_db()

    students = conn.execute("""
        SELECT
            name AS student_name,
            subject,
            score,
            attempts,
            status
        FROM quiz_records
        ORDER BY score DESC, attempts ASC
    """).fetchall()

    conn.close()

    return render_template("leaderboard.html", students=students)

# ---------------- NOTES ----------------

@app.route("/notes")
def notes():

    if "student_name" not in session:
        return redirect(url_for("student_login"))

    student_name = session["student_name"]

    return render_template(
        "notes.html",
        notes=NOTES,
        student_name=student_name
    )


@app.route("/notes/<subject>")
def note_detail(subject):

    if "student_name" not in session:
        return redirect(url_for("student_login"))

    student_name = session["student_name"]

    note = NOTES.get(subject)

    if note is None:
        return "Notes not found", 404

    return render_template(
        "note_detail.html",
        subject=subject,
        note=note,
        student_name=student_name
    )
# ---------------- ABOUT ----------------
@app.route("/about")
def about():
    return render_template("about.html")
#-------------logout--------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

#--------------AI-chatbox-------------------
@app.route("/ai_chatbox", methods=["GET", "POST"])
def ai_chatbox():

    answer = None
    user_message = ""

    if request.method == "POST":

        user_message = request.form.get("message", "").strip()

        if user_message:

            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=user_message
                )

                answer = response.text

            except Exception as e:
                answer = "AI Error: " + str(e)

    return render_template(
        "chat.html",
        answer=answer,
        user_message=user_message
    )
# ---------------- EDIT ----------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    
    conn = get_db()

    if request.method == "POST":

        name = request.form["name"]
        score = int(request.form["score"])
        attempts = int(request.form["attempts"])

        status = "Pass" if score >= 50 else "Fail"

        conn.execute(
            """
            UPDATE quiz_records
            SET name=?, score=?, attempts=?, status=?
            WHERE id=?
            """,
            (name, score, attempts, status, id)
        )

        conn.commit()
        conn.close()

        flash("Student updated successfully!", "success")
        return redirect(url_for("students"))

    student = conn.execute(
        "SELECT * FROM quiz_records WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "Edit_student.html",
        student=student
    )
#------------Delete-----------------------
@app.route("/delete_student/<int:id>")
def delete_student(id):

    # Admin login check
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    conn = get_db()

    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    flash("Student deleted successfully!", "success")

    return redirect(url_for("students"))
#-----------clear_old_leaderboard------------
@app.route("/clear_old_leaderboard")
def clear_old_leaderboard():
    conn = get_db()
    conn.execute(
        "DELETE FROM quiz_records WHERE name != ?",
        ("Mohini",)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("leaderboard"))
# ---------------- MAIN ----------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)