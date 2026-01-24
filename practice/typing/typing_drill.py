#!/usr/bin/env python3
import random
import time

QUESTIONS = [
    # Linux basics
    {
        "q": "What command shows your current directory?",
        "a": ["pwd"]
    },
    {
        "q": "List files (including hidden) in long format:",
        "a": ["ls -lah", "ls -alh", "ls -la"]
    },
    {
        "q": "What command prints the first 20 lines of a file?",
        "a": ["head -n 20 <file>", "head -n 20 file", "head -n 20"]
    },
    {
        "q": "What command prints the last 20 lines of a file?",
        "a": ["tail -n 20 <file>", "tail -n 20 file", "tail -n 20"]
    },

    # Git
    {
        "q": "Stage all changes (new + modified) in git:",
        "a": ["git add ."]
    },
    {
        "q": "Commit with a message:",
        "a": ['git commit -m "message"', "git commit -m"]
    },
    {
        "q": "Show current branch + status:",
        "a": ["git status"]
    },
    {
        "q": "Push to remote (current branch):",
        "a": ["git push", "git push -u origin main"]
    },

    # Docker
    {
        "q": "List running containers:",
        "a": ["docker ps"]
    },
    {
        "q": "List all containers (including stopped):",
        "a": ["docker ps -a"]
    },
    {
        "q": "List images:",
        "a": ["docker images"]
    },
    {
        "q": "Run an image interactively with a shell (example alpine):",
        "a": ["docker run -it alpine sh", "docker run -it alpine /bin/sh"]
    },
    {
        "q": "Build a docker image with tag mandelbrot:1 from current folder:",
        "a": ["docker build -t mandelbrot:1 ."]
    },

    # YAML
    {
        "q": "In YAML, what does indentation control?",
        "a": ["structure", "nesting", "hierarchy"]
    },
    {
        "q": "In YAML, lists are written with what character?",
        "a": ["-"]
    },
]

def normalize(s: str) -> str:
    return " ".join(s.strip().lower().split())

def ask_question(item, num, total):
    print("\n" + "=" * 60)
    print(f"QUESTION {num}/{total}")
    print(item["q"])
    print("-" * 60)
    user = input("Your answer: ").strip()

    if user.lower() in ["q", "quit", "exit"]:
        return None  # signal quit

    user_norm = normalize(user)
    valid = [normalize(x) for x in item["a"]]

    # accept partial-match for concept answers (like "structure")
    correct = (user_norm in valid) or any(user_norm in v for v in valid)

    if correct:
        print("✅ Correct!")
        return True
    else:
        print("❌ Not quite.")
        print("✅ Acceptable answers:")
        for v in item["a"]:
            print(f"   - {v}")
        return False

def main():
    print("\n🔥 ZERO2CLOUD DRILL MODE 🔥")
    print("Type 'q' to quit anytime.")
    time.sleep(0.4)

    score = 0
    asked = 0

    while True:
        item = random.choice(QUESTIONS)
        asked += 1

        result = ask_question(item, asked, asked)
        if result is None:
            break
        if result is True:
            score += 1

        print(f"\nScore: {score}/{asked} ({round(score/asked*100)}%)")

    print("\n✅ Drill ended.")
    print(f"Final Score: {score}/{asked} ({round(score/asked*100) if asked else 0}%)")
    print("Keep stacking wins, Paul. 🧱🔥")

if __name__ == "__main__":
    main()
