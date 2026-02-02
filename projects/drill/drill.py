#!/usr/bin/env python3
import random
import time

BANK = [

    {
        "q": "Show disk usage of all mounted filesystems",
        "a": ["df -h"],
        "hint": "df + human readable"
    },
    {
        "q": "Show disk usage of current folder",
        "a": ["du -sh ."],
        "hint": "du summary human"
    },
    {
        "q": "Find files named test.txt starting here",
        "a": ["find . -name test.txt"],
        "hint": "find current dir by name"
    },
    {
        "q": "Find all .log files",
        "a": ["find . -name '*.log'"],
        "hint": "find by extension"
    },
    {
        "q": "Show running processes",
        "a": ["ps aux"],
        "hint": "classic full process list"
    },
    {
        "q": "Show processes in real time",
        "a": ["top"],
        "hint": "live process viewer"
    },
    {
        "q": "Kill process with PID 1234",
        "a": ["kill 1234"],
        "hint": "kill + PID"
    },
    {
        "q": "Show listening ports",
        "a": ["ss -tulpen"],
        "hint": "ss with tcp/udp/listen flags"
    },
    {
        "q": "Show IP addresses",
        "a": ["ip a"],
        "hint": "modern replacement for ifconfig"
    },
    {
        "q": "Show route table",
        "a": ["ip route"],
        "hint": "ip routing info"
    },
    {
        "q": "Change owner to user pharr for file.txt",
        "a": ["chown pharr file.txt"],
        "hint": "change owner"
    },
    {
        "q": "Change permissions to rwxr-xr-x",
        "a": ["chmod 755 file"],
        "hint": "numeric permissions"
    },


    {
        "q": "List files (including hidden) in long format",
        "a": ["ls -lah"],
        "hint": "Think: ls + long + all + human"
    },
    {
        "q": "Show current working directory",
        "a": ["pwd"],
        "hint": "3-letter command for 'print working directory'"
    },
    {
        "q": "Create a folder named test",
        "a": ["mkdir test"],
        "hint": "Make directory"
    },
    {
        "q": "Create an empty file named notes.txt",
        "a": ["touch notes.txt"],
        "hint": "Touch creates empty files"
    },
    {
        "q": "Show the last 20 lines of file.log",
        "a": ["tail -n 20 file.log"],
        "hint": "tail + -n for number of lines"
    },
    {
        "q": "Search for 'error' in app.log (case-insensitive)",
        "a": ["grep -i error app.log"],
        "hint": "grep with -i ignores case"
    },
    {
        "q": "Make script.sh executable",
        "a": ["chmod +x script.sh"],
        "hint": "chmod +x adds execute permission"
    },
]

def normalize(s: str) -> str:
    # normalize whitespace so "tail   -n 20 file.log" still counts
    return " ".join(s.strip().split())

def ask_one(item: dict, strict: bool = False) -> tuple[str, float, bool]:
    """
    Returns (status, seconds, got_point)
    status: "ok" | "hint" | "quit"
    """
    print("\n" + "=" * 48)
    print(item["q"])
    print("(Enter = hint, q = quit)")
    t0 = time.time()
    user = input("Command: ").strip()
    dt = time.time() - t0

    if user.lower() == "q":
        return ("quit", dt, False)

    if user == "":
        # Hint mode (no penalty, just gives clue)
        hint = item.get("hint", "No hint available.")
        print(f"💡 Hint: {hint}")
        return ("hint", dt, False)

    user_n = normalize(user)
    answers_n = [normalize(a) for a in item["a"]]

    got_point = user_n in answers_n

    if got_point:
        print("✅ Correct!")
        return ("ok", dt, True)

    # Wrong: show correct answer(s)
    print("❌ Not quite.")
    if strict:
        print("Strict mode: exact match required.")
    print("✅ Accepted:")
    for a in item["a"]:
        print(f" - {a}")
    return ("ok", dt, False)

def main():
    print("ZERO2CLOUD DRILL (SIMPLE)")
    print("Hint: press Enter on empty input to get a clue.\n")

    strict = input("Strict mode? [y/N]: ").strip().lower() == "y"

    correct = 0
    wrong = 0
    hints = 0
    missed = {}  # key -> count
    total_time = 0.0

    while True:
        item = random.choice(BANK)
        status, dt, got_point = ask_one(item, strict=strict)

        if status == "quit":
            break
        if status == "hint":
            hints += 1
            continue

        total_time += dt

        if got_point:
            correct += 1
        else:
            wrong += 1
            key = f"{item['q']}  ->  {item['a'][0]}"
            missed[key] = missed.get(key, 0) + 1

        print(f"\nScore: {correct}/{correct+wrong} | Wrong: {wrong} | Hints: {hints} | Time: {total_time:.1f}s")

    print("\n" + "=" * 48)
    print("SESSION SUMMARY")
    print(f"Correct: {correct}")
    print(f"Wrong:   {wrong}")
    print(f"Hints:   {hints}")
    print(f"Time:    {total_time:.1f}s")

    if missed:
        print("\nMost missed:")
        for k, v in sorted(missed.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f" - ({v}x) {k}")

if __name__ == "__main__":
    main()
