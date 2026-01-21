╔══════════════════════════════════════╗
║           ZERO2CLOUD // LOCK-IN      ║
║           YAML CHEAT SHEET           ║
╚══════════════════════════════════════╝

=========================================
WHAT IS YAML?
=========================================
YAML = a human-readable config format
Used in: Docker Compose, Kubernetes, CI/CD, app config files

RULES:
- Indent with SPACES (never tabs)
- Use consistent indentation (2 spaces is common)

=========================================
KEY: VALUE
=========================================
name: Paul
active: true
count: 5

=========================================
LISTS
=========================================
items:
  - one
  - two
  - three

=========================================
NESTED OBJECTS
=========================================
server:
  host: localhost
  port: 8080

=========================================
LIST OF OBJECTS
=========================================
users:
  - name: Paul
    role: admin
  - name: Sam
    role: user

=========================================
COMMENTS
=========================================
# this is a comment
