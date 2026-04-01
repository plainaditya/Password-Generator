import random
import string

def generate_password(length, use_letters, use_digits, use_symbols):
    characters = ""

    if use_letters:
        characters += string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        return None

    password = "".join(random.choice(characters) for _ in range(length))
    return password


def password_strength(password):
    score = 0

    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    if len(password) >= 12:
        score += 1

    if score <= 2:
        return "Weak ❌"
    elif score <= 4:
        return "Medium ⚠️"
    else:
        return "Strong 🔥"


print("🔐 Advanced Password Generator")

while True:
    try:
        length = int(input("Enter password length: "))
        if length <= 0:
            print("Length must be greater than 0")
            continue
    except:
        print("Invalid input. Enter a number.")
        continue

    use_letters = input("Include letters? (yes/no): ").lower() == "yes"
    use_digits = input("Include numbers? (yes/no): ").lower() == "yes"
    use_symbols = input("Include symbols? (yes/no): ").lower() == "yes"

    password = generate_password(length, use_letters, use_digits, use_symbols)

    if password is None:
        print("❌ You must select at least one character type")
        continue

    print("\nGenerated Password:", password)
    print("Password Strength:", password_strength(password))

    again = input("\nGenerate another? (yes/no): ").lower()
    if again != "yes":
        print("Goodbye 👋")
        break
