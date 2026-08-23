print("CHAT online.")

name = input("What is your name? ")

print(f"Welcome, {name}.")

command = input("What would you like to do? ").strip().lower()

if command == "study":
    print("Entering study mode.")

elif command == "code":
    print("Entering developer mode.")

elif command == "game":
    print("Entering game development mode.")

else:
    print("I don't recognize that command yet.")