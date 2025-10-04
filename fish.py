# Program to check if a caught zander meets the size limit

# Ask for the length of the zander
length = int(input("Enter the length of the zander in centimeters: "))

# Size limit
size_limit = 42

# Check if it meets the requirement
if length < size_limit:
    difference = size_limit - length
    print(f"The zander is too small, please release it back into the lake.")
    print(f"It is {difference} cm below the size limit.")
else:
      print("Good catch! The zander meets the size limit.")
