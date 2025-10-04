# Program to check hemoglobin level

# Ask for inputs
sex = input("Enter your biological sex (male/female): ").lower()
hemoglobin = int(input("Enter your hemoglobin value (g/l): "))

# Check ranges
if sex == "female":
    if hemoglobin < 117:
        print("Your hemoglobin value is low.")
    elif hemoglobin <= 155:
        print("Your hemoglobin value is normal.")
    else:
        print("Your hemoglobin value is high.")
elif sex == "male":
    if hemoglobin < 134:
        print("Your hemoglobin value is low.")
    elif hemoglobin <= 167:
        print("Your hemoglobin value is normal.")
    else:
        print("Your hemoglobin value is high.")
else:
    print("Invalid input for sex. Please enter 'male' or 'female'.")
