# Advanced Password Generator (Python)

This is a Python-based password generator that creates secure and customizable passwords based on user input.  
It also evaluates the strength of the generated password to help users understand how secure it is.

---

## 🚀 Features

### 🔐 1. Custom Password Length
The user can define the desired length of the password.  
- Ensures flexibility based on different use cases  
- Input validation prevents invalid values  

---

### 🔤 2. Character Type Selection
The user can choose which types of characters to include:
- Letters (uppercase + lowercase)
- Numbers (0–9)
- Symbols (special characters like !, @, #, etc.)

👉 This allows generating:
- Simple passwords  
- Complex and highly secure passwords  

---

### 🧠 3. Password Generation Logic
- Uses Python’s `random` module  
- Combines selected character sets  
- Randomly picks characters to form the password  

This ensures:
- High randomness  
- Better security  

---

### 📊 4. Password Strength Checker
After generating a password, the program evaluates its strength based on:
- Presence of lowercase letters  
- Presence of uppercase letters  
- Presence of numbers  
- Presence of symbols  
- Length of the password  

Strength Levels:
- Weak ❌  
- Medium ⚠️  
- Strong 🔥  

---

### ⚠️ 5. Input Validation & Error Handling
- Prevents crashes from invalid inputs  
- Ensures only valid numbers are accepted for length  
- Ensures at least one character type is selected  

---

### 🔁 6. Multiple Password Generation
- The program runs in a loop  
- Users can generate multiple passwords without restarting  

---

## 🛠️ Technologies Used
- Python
- Built-in modules:
  - `random`
  - `string`

---

## ▶️ How to Run

1. Install Python (if not already installed)
2. Download or clone this repository
3. Run the program:

```bash
python password.py
