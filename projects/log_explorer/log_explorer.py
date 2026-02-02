#!/usr/bin/env python3
from pathlib import Path
import sys

PORT_NOTES = {
    "22":  "SSH (remote login)",
    "53":  "DNS (resolver)",
    "80":  "HTTP (web)",
    "443": "HTTPS (web)",
    "631": "IPP/CUPS printing",
    "3389":"RDP (remote desktop)",
    "5432":"PostgreSQL",
    "6379":"Redis",
    "27017":"MongoDB",
}


def extract_ports(lines):
    ports = []
    for line in lines:
        if "LISTEN" in line:
            parts = line.split()
            if len(parts) >= 5:
                ports.append(parts[4])
    return sorted(set(ports))

def extract_interfaces(lines):
    interfaces = []
    for line in lines:
        if line and line[0].isdigit() and ":" in line:
            try:
                iface = line.split(":")[1].strip().split()[0]
                if iface:
                    interfaces.append(iface)
            except Exception:
                pass
    return sorted(set(interfaces))

def print_list(title, items):
    print(title)
    if not items:
        print(" (none)")
        return
    for x in items:
        print(f" - {x}")

def annotate_ports(port_items):
    """
    port_items: list of strings like '0.0.0.0:631' or '127.0.0.53%lo:53'
    Returns list with notes appended when known.
    """
    out = []
    for item in port_items:
        port = item.split(":")[-1]
        note = PORT_NOTES.get(port)
        if note:
            out.append(f"{item}  <- {note}")
        else:
            out.append(item)
    return out


def get_latest_two_logs():
    log_dir = Path.home() / "zero_to_cloud/syscheck/netcheck"
    logs = sorted(
        log_dir.glob("netcheck_*.txt"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    return logs[:2]

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  ./log_explorer.py netcheck_log.txt")
        print("  ./log_explorer.py old_log.txt new_log.txt")
        print("  ./log_explorer.py latest")
        sys.exit(1)

    # latest mode
    if sys.argv[1] == "latest":
        latest_logs = get_latest_two_logs()
        if len(latest_logs) < 2:
            print("Not enough netcheck logs found in ~/zero_to_cloud/syscheck/netcheck/")
            sys.exit(1)
        old_path, new_path = latest_logs[1], latest_logs[0]

    # two file compare mode
    elif len(sys.argv) >= 3:
        old_path = Path(sys.argv[1])
        new_path = Path(sys.argv[2])

    # one file mode
    else:
        log_path = Path(sys.argv[1])
        if not log_path.exists():
            print(f"Error: file not found -> {log_path}")
            sys.exit(1)

        lines = log_path.read_text(errors="ignore").splitlines()
        ports = extract_ports(lines)
        interfaces = extract_interfaces(lines)

        print("\n=== ZERO2CLOUD LOG EXPLORER ===")
        print(f"File: {log_path}\n")
        print_list("Interfaces:", interfaces)
        print()
        print_list("Listening Ports:", ports)
        print("\nSummary:")
        print(f" Interfaces: {len(interfaces)}")
        print(f" Listening ports: {len(ports)}")
        return

    # compare section
    old_lines = old_path.read_text(errors="ignore").splitlines()
    new_lines = new_path.read_text(errors="ignore").splitlines()

    old_ports = set(extract_ports(old_lines))
    new_ports = set(extract_ports(new_lines))
    old_ifaces = set(extract_interfaces(old_lines))
    new_ifaces = set(extract_interfaces(new_lines))

    added_ports = sorted(new_ports - old_ports)
    removed_ports = sorted(old_ports - new_ports)
    added_ifaces = sorted(new_ifaces - old_ifaces)
    removed_ifaces = sorted(old_ifaces - new_ifaces)

    print("\n=== ZERO2CLOUD LOG EXPLORER (COMPARE) ===")
    print(f"Old: {old_path.name}")
    print(f"New: {new_path.name}\n")

    print_list("Ports ADDED:", annotate_ports(added_ports))
    print()
    print_list("Ports REMOVED:", annotate_ports(removed_ports))
    print()
    print_list("Interfaces ADDED:", added_ifaces)
    print()
    print_list("Interfaces REMOVED:", removed_ifaces)

    print("\nSummary:")
    print(f" Old ports: {len(old_ports)}  ->  New ports: {len(new_ports)}")
    print(f" Old ifaces: {len(old_ifaces)} ->  New ifaces: {len(new_ifaces)}")

if __name__ == "__main__":
    main()
