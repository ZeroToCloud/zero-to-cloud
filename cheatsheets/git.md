╔══════════════════════════════════════╗
║           ZERO2CLOUD // LOCK-IN      ║
║            GIT CHEAT SHEET           ║
╚══════════════════════════════════════╝

=========================================
CHECK STATUS
=========================================
git status
git log --oneline --max-count=10

=========================================
FIRST TIME SETUP
=========================================
git config --global user.name "Paul Harris"
git config --global user.email "Zero_to_Cloud@proton.me"

=========================================
BASIC WORKFLOW
=========================================
git add .
git commit -m "message here"
git push

=========================================
ADD FILES
=========================================
git add file.txt
git add folder/

=========================================
UNDO / FIX
=========================================
git restore file.txt
git restore --staged file.txt

=========================================
BRANCHES
=========================================
git branch
git checkout -b new-branch
git checkout main

