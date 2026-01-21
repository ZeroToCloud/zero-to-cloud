╔══════════════════════════════════════╗
║           ZERO2CLOUD // LOCK-IN      ║
║          LINUX CHEAT SHEET           ║
╚══════════════════════════════════════╝

=========================================
NAVIGATION
=========================================
pwd
ls
ls -lah
cd ..
cd ~
cd /path/to/folder

=========================================
FILES & FOLDERS
=========================================
touch file.txt
mkdir folder
mkdir -p a/b/c
cp file1 file2
cp -r folder1 folder2
mv oldname newname
rm file
rm -r folder

=========================================
VIEW / EDIT
=========================================
cat file
less file     # quit with q
nano file

=========================================
FIND / SEARCH
=========================================
grep word file
grep -R word .
find . -name "*.md"

=========================================
PERMISSIONS
=========================================
ls -l
chmod +x script.sh

=========================================
SYSTEM
=========================================
whoami
uname -a
df -h
free -h
top

=========================================
APT (UBUNTU)
=========================================
sudo apt update
sudo apt upgrade
sudo apt install pkg
