# ZERO2CLOUD – COMMAND SUMMARY

Your daily quick-reference.

---

## Navigation
pwd              # show current folder
ls               # list files
ls -lah          # detailed list (incl. hidden)
cd folder        # change folder
cd ..            # go up one level
cd ~             # go home

---

## Files & Folders
mkdir dir        # create folder
touch file.txt   # create file
cp src dst       # copy
mv src dst       # move/rename
rm file          # delete file
rm -r dir        # delete folder

---

## Viewing Files
cat file         # show whole file
less file        # scroll view
head file        # first lines
tail file        # last lines
tail -f file     # live updates

---

## Search
grep text file
grep -i text file      # ignore case
grep -r text folder    # recursive search

Nano search:
CTRL + W  → search
ALT + W   → next match

---

## Permissions
chmod +x script.sh     # make executable
./script.sh            # run script

---

## Networking / Ports
ip a
ss -tulpen
ping google.com

---

## Git Basics
git status
git add .
git commit -m "message"
git push
git pull
git log --oneline

---

## Docker Basics
docker ps
docker images
docker build -t name .
docker run image
docker stop container

---

## Zero2Cloud Daily Flow
cd ~/zero_to_cloud
git status
run netcheck
review changes
commit progress
