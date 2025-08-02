import requests
import json
import os
import csv
import time
import textwrap

# ========== CONFIG ==========
BASE_DIR = "IntelASK_AI"
CHAT_DIR = os.path.join(BASE_DIR, "chats")
CSV_FILE = os.path.join(BASE_DIR, "conversation.csv")

API_URL = "http://38.54.116.137:8000/api/v1/ai/chat"
HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "http://38.54.116.137:8000",
    "Referer": "http://38.54.116.137:8000/",
    "User-Agent": "IntelASK-Agent/1.0"
}
CONVERSATION_ID = "b5b53347-c4e5-4394-85bf-374d09bcd542"

# ========== INIT STRUCTURE ==========
os.makedirs(CHAT_DIR, exist_ok=True)

# ========== ASCII BANNER ==========
def ascii_banner():
    print("\033[95m")
    print(r"""
 ██▓███   ███▄    █ ▄▄▄█████▓▓█████ ██▓     ▄▄▄▄    ▄▄▄       ██ ▄█▀
▓██░  ██▒ ██ ▀█   █ ▓  ██▒ ▓▒▓█   ▀▓██▒    ▓█████▄ ▒████▄     ██▄█▒ 
▓██░ ██▓▒▓██  ▀█ ██▒▒ ▓██░ ▒░▒███  ▒██░    ▒██▒ ▄██▒██  ▀█▄  ▓███▄░ 
▒██▄█▓▒ ▒▓██▒  ▐▌██▒░ ▓██▓ ░ ▒▓█  ▄▒██░    ▒██░█▀  ░██▄▄▄▄██ ▓██ █▄ 
▒██▒ ░  ░▒██░   ▓██░  ▒██▒ ░ ░▒████░██████▒░▓█  ▀█▓ ▓█   ▓██▒▒██▒ █▄
▒▓▒░ ░  ░░ ▒░   ▒ ▒   ▒ ░░   ░░ ▒░ ░ ▒░▓  ░░▒▓███▀▒ ▒▒   ▓▒█░▒ ▒▒ ▓▒
░▒ ░     ░ ░░   ░ ▒░    ░     ░ ░  ░ ░ ▒  ░▒░▒   ░   ▒   ▒▒ ░░ ░▒ ▒░
░░          ░   ░ ░   ░         ░    ░ ░    ░    ░   ░   ▒   ░ ░░ ░ 
                  ░             ░  ░   ░  ░ ░            ░  ░░  ░   

      \033[96mAI OSINT Terminal — IntelASK AI Interface\033[0m
\033[90mNOTE: We do not own the emulated API in Python programming language,
we found this AI available and have decided to share it.\033[0m
""")
    print("═══════════════════════════════════════════════════════════════════════════\n")

# ========== SUGGESTIONS ==========
def show_suggestions():
    print("\033[94m💡 Suggested Prompts:\033[0m")
    suggestions = [
        '🧠 iocs "lockbit" ?',
        '🌐 top dark net forums?',
        '🚨 top CVE 2025?'
    ]
    for s in suggestions:
        print(f"   {s}")
    print()

# ========== STYLE: CYBERPUNK WRAPPED ==========
def print_cyberpunk(text, width=80):
    border = "═" * width
    print(f"\033[95m╔{border}╗")
    for paragraph in text.split("\n"):
        wrapped_lines = textwrap.wrap(paragraph, width=width)
        if not wrapped_lines:
            print(f"║ {' ' * width} ║")
        for line in wrapped_lines:
            print(f"║ \033[92m{line.ljust(width)}\033[95m ║")
    print(f"╚{border}╝\033[0m\n")

# ========== SAVE CHAT ==========
def save_txt(question, answer, index):
    filename = os.path.join(CHAT_DIR, f"question_{index}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"📝 Question:\n{question}\n\n📡 Answer:\n{answer}")

def save_csv(question, answer):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Question", "Answer"])
        writer.writerow([question, answer])

# ========== ASK ==========
def ask_question(index):
    question = input("\n\033[96m🧾 Enter your question: \033[0m")
    payload = {
        "message": question,
        "context": {"source": "dashboard"},
        "conversation_id": CONVERSATION_ID
    }
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, verify=False)
        data = response.json()
        answer = data.get("response", "❌ No valid response received.")
        print_cyberpunk(answer)

        save_txt(question, answer, index)
        save_csv(question, answer)
        return True
    except Exception as e:
        print_cyberpunk(f"⚠️ Connection error:\n{str(e)}")
        return False

# ========== HISTORY ==========
def show_history():
    if not os.path.isfile(CSV_FILE):
        print("\033[91m⚠️ No history found.\033[0m")
        return
    print("\n\033[93m📜 Previous Interactions:\033[0m\n")
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for idx, row in enumerate(reader, 1):
            print_cyberpunk(f"💬 Question {idx}:\n{row[0]}\n\n📡 Answer:\n{row[1]}")

# ========== MENU ==========
def menu():
    index = 1
    if os.path.isfile(CSV_FILE):
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            index = sum(1 for _ in f)

    while True:
        print("\n\033[92m📟 INTELASK MENU\033[0m")
        print("1. 🔍 Ask a question")
        print("2. 📖 View history")
        print("3. ❌ Exit")
        choice = input("\nChoose an option (1-3): ").strip()

        if choice == "1":
            if ask_question(index):
                index += 1
        elif choice == "2":
            show_history()
        elif choice == "3":
            print("\n\033[92m👋 Shutting down IntelASK AI... See you next time.\033[0m\n")
            break
        else:
            print("\033[91m❌ Invalid option. Try again.\033[0m")

# ========== RUN ==========
if __name__ == "__main__":
    ascii_banner()
    show_suggestions()
    menu()
