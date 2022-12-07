from functions import black_scholes_put, option_1, option_2

print("Hello! Welcome to Patrick Haney's MATH 425 Final Project. \nIn this program you will have two options: \n"
      " 1. Run program based on rubric \n 2. Enter your own information for your own calculations")

user_number = "0"
while user_number != "1" or "2":
    user_number = input("Enter 1 or 2 based on the above options: ")
    if user_number == "1":
        option_1()
        quit()
    elif user_number == "2":
        option_2()
        quit()
    else:
        print("Invalid input")
        continue
