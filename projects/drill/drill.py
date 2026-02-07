#!/usr/bin/env python3
import random
import time

BANK = [

    {"q":"Show last 20 journal logs","a":["journalctl -n 20"],"hint":"journalctl last lines"},
    {"q":"Show logs for ssh service","a":["journalctl -u ssh"],"hint":"service logs"},
    {"q":"Check service status ssh","a":["systemctl status ssh"],"hint":"systemctl status"},


    {"q":"Change group of file.txt to staff","a":["chgrp staff file.txt"],"hint":"change group"},
    {"q":"Give owner execute permission","a":["chmod u+x file"],"hint":"user execute"},
    {"q":"Remove write permission for others","a":["chmod o-w file"],"hint":"others minus write"},


    {"q":"Create tar archive of logs folder","a":["tar -cf logs.tar logs"],"hint":"tar create file"},
    {"q":"Extract logs.tar","a":["tar -xf logs.tar"],"hint":"tar extract"},
    {"q":"Create gzipped archive logs.tar.gz","a":["tar -czf logs.tar.gz logs"],"hint":"gzip tar"},
    {"q":"Extract logs.tar.gz","a":["tar -xzf logs.tar.gz"],"hint":"extract gzip"},


    {"q":"Ping google.com once","a":["ping -c 1 google.com"],"hint":"count 1 ping"},
    {"q":"Show network interfaces","a":["ip link"],"hint":"interface list"},
    {"q":"Show DNS servers","a":["cat /etc/resolv.conf"],"hint":"resolver config"},


    {"q":"Show system uptime","a":["uptime"],"hint":"system running time"},
    {"q":"Show current user","a":["whoami"],"hint":"who am i"},
    {"q":"Show logged in users","a":["who"],"hint":"logged users"},
    {"q":"Show process tree","a":["ps auxf"],"hint":"process tree format"},
    {"q":"Kill process by name firefox","a":["pkill firefox"],"hint":"kill by name"},


    {"q":"Find files bigger than 100MB starting here","a":["find . -type f -size +100M"],"hint":"find by size"},
    {"q":"Find directories named logs","a":["find . -type d -name logs"],"hint":"type d"},
    {"q":"Search recursively for TODO in current folder","a":["grep -r TODO ."],"hint":"recursive grep"},
    {"q":"Count lines in file.txt","a":["wc -l file.txt"],"hint":"word count lines"},
    {"q":"Sort lines in file.txt","a":["sort file.txt"],"hint":"sort command"},


    {"q":"List files (including hidden) in long format","a":["ls -lah"],"hint":"Think: ls + long + all + human"},
    {"q":"Show current working directory","a":["pwd"],"hint":"print working directory"},
    {"q":"Create a folder named test","a":["mkdir test"],"hint":"make directory"},
    {"q":"Create an empty file named notes.txt","a":["touch notes.txt"],"hint":"touch creates empty files"},
    {"q":"Show the last 20 lines of file.log","a":["tail -n 20 file.log"],"hint":"tail + -n"},
    {"q":"Search for 'error' in app.log (case-insensitive)","a":["grep -i error app.log"],"hint":"grep -i ignores case"},
    {"q":"Make script.sh executable","a":["chmod +x script.sh"],"hint":"chmod +x adds execute permission"},

    {"q":"Show disk usage of all mounted filesystems","a":["df -h"],"hint":"df + human readable"},
    {"q":"Show disk usage of current folder","a":["du -sh ."],"hint":"du summary human; . = current folder"},
    {"q":"Find files named test.txt starting here","a":["find . -name test.txt"],"hint":"find + -name"},
    {"q":"Find all .log files","a":["find . -name '*.log'"],"hint":"quotes around *.log"},
    {"q":"Show running processes","a":["ps aux"],"hint":"classic full process list"},
    {"q":"Show processes in real time","a":["top"],"hint":"live process viewer"},
    {"q":"Kill process with PID 1234","a":["kill 1234"],"hint":"kill + PID"},
    {"q":"Show listening ports","a":["ss -tulpen"],"hint":"ss listening ports"},
    {"q":"Show IP addresses","a":["ip a"],"hint":"ip addr"},
    {"q":"Show route table","a":["ip route"],"hint":"routing table"},
    {"q":"Change owner to user pharr for file.txt","a":["chown pharr file.txt"],"hint":"change owner"},
    {"q":"Change permissions to rwxr-xr-x","a":["chmod 755 file"],"hint":"755 = rwx r-x r-x"},
]

def normalize(s: str) -> str:
    return " ".join(s.strip().split())

def ask_one(item: dict, strict: bool = False) -> tuple[str, float, bool]:
    print("\n" + "=" * 48)
    print(item["q"])
    print("(Enter = hint, q = quit)")
    t0 = time.time()

    user = input("Command: ").strip()

    if user == "":
        hint = item.get("hint", "No hint available.")
        print(f"💡 Hint: {hint}")
        user = input("Command: ").strip()

    if user.lower() == "q":
        dt = time.time() - t0
        return ("quit", dt, False)

    dt = time.time() - t0

    user_n = normalize(user)
    answers_n = [normalize(a) for a in item["a"]]
    got_point = user_n in answers_n

    if got_point:
        print("✅ Correct!")
        return ("ok", dt, True)

    print("❌ Not quite.")
    if strict:
        print("Strict mode: exact match required.")
    print("✅ Accepted:")
    for a in item["a"]:
        print(f" - {a}")

    return ("ok", dt, False)

def main():
    print("ZERO2CLOUD DRILL (SIMPLE)")
    print("Hint: press Enter on empty input to get a clue (you can still answer). \n")

    strict = input("Strict mode? [y/N]: ").strip().lower() == "y"

    correct = 0
    wrong = 0
    missed = {}
    total_time = 0.0

    while True:
        item = random.choice(BANK)
        status, dt, got_point = ask_one(item, strict=strict)

        if status == "quit":
            break

        total_time += dt

        if got_point:
            correct += 1
        else:
            wrong += 1
            key = f"{item['q']}  ->  {item['a'][0]}"
            missed[key] = missed.get(key, 0) + 1

        print(f"\nScore: {correct}/{correct+wrong} | Wrong: {wrong} | Time: {total_time:.1f}s")

    print("\n" + "=" * 48)
    print("SESSION SUMMARY")
    print(f"Correct: {correct}")
    print(f"Wrong:   {wrong}")
    print(f"Time:    {total_time:.1f}s")

    if missed:
        print("\nMost missed:")
        for k, v in sorted(missed.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f" - ({v}x) {k}")

if __name__ == "__main__":
    main()
