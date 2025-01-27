import subprocess
import os
import sys
import shutil
import random
from datetime import datetime

# HTML template for results
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SCPN Scanner Results</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            color: #333;
            margin: 0;
            padding: 20px;
        }}
        h1 {{
            color: #4CAF50;
        }}
        .result {{
            margin: 20px 0;
            padding: 15px;
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .timestamp {{
            font-size: 0.9em;
            color: #666;
        }}
    </style>
</head>
<body>
    <h1>SCPN Scanner Results</h1>
    {content}
</body>
</html>
"""

# Generate HTML output
def write_to_html(title, content):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    html_content = f"""
    <div class="result">
        <h2>{title}</h2>
        <p class="timestamp">Timestamp: {timestamp}</p>
        <pre>{content}</pre>
    </div>
    """
    # Append to the HTML file
    with open("scpn_results.html", "a") as f:
        f.write(html_content)

# Required tools
REQUIRED_TOOLS = {
    'nmap': 'Network exploration and security auditing',
    'gobuster': 'Directory/file enumeration tool',
    'msfconsole': 'Metasploit framework console',
}

# Check required tools
def check_tools():
    missing_tools = [tool for tool in REQUIRED_TOOLS.keys() if not shutil.which(tool)]
    if missing_tools:
        print(f"[!] Missing tools: {', '.join(missing_tools)}")
        sys.exit(1)

# Run command and return output
def run_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

# Quick Scan
def quick_scan(target):
    print(f"[+] Performing quick scan on {target}...")
    output = run_command(['nmap', '-T4', '-F', target])
    write_to_html(f"Quick Scan Results for {target}", output)
    print("[+] Quick scan results saved to scpn_results.html")

# Full Scan
def full_scan(target):
    print(f"[+] Performing full scan on {target}...")
    nmap_output = run_command(['nmap', '-sV', '-A', target])
    gobuster_output = run_command(['gobuster', 'dir', '-u', target, '-w', '/usr/share/wordlists/dirb/common.txt'])
    content = f"### Nmap Output ###\n{nmap_output}\n\n### Gobuster Output ###\n{gobuster_output}"
    write_to_html(f"Full Scan Results for {target}", content)
    print("[+] Full scan results saved to scpn_results.html")

# Vulnerability Scan
def vulnerability_scan(target):
    print(f"[+] Performing vulnerability scan on {target}...")
    vuln_scan = f"msfconsole -q -x 'db_nmap -sV {target}; vulns; exit'"
    output = run_command(['bash', '-c', vuln_scan])
    write_to_html(f"Vulnerability Scan Results for {target}", output)
    print("[+] Vulnerability scan results saved to scpn_results.html")

# Help Menu
def show_help():
    help_content = """
    SCPN Scanner Options:
    1. Quick Scan - Fast port scanning.
    2. Full Scan - Comprehensive scan with services and directories.
    3. Vulnerability Scan - Scan for known vulnerabilities.
    4. Update - Update the tool.
    5. Help - Show this menu.
    6. Exit - Exit the program.
    """
    print(help_content)
    write_to_html("Help Menu", help_content)

# Main menu
def main():
    check_tools()
    print("[*] SCPN Scanner - Advanced Network and Web Scanner")
    while True:
        print("""
        [1] Quick Scan
        [2] Full Scan
        [3] Vulnerability Scan
        [4] Update
        [5] Help
        [6] Exit
        """)
        choice = input("[?] Choose an option: ").strip()
        if choice == "1":
            target = input("[?] Enter target (IP/URL): ").strip()
            quick_scan(target)
        elif choice == "2":
            target = input("[?] Enter target (IP/URL): ").strip()
            full_scan(target)
        elif choice == "3":
            target = input("[?] Enter target (IP/URL): ").strip()
            vulnerability_scan(target)
        elif choice == "4":
            print("[+] Updating SCPN Scanner...")
            os.system("git pull")
        elif choice == "5":
            show_help()
        elif choice == "6":
            print("[+] Exiting SCPN Scanner. Goodbye!")
            break
        else:
            print("[!] Invalid option, please try again.")

if __name__ == "__main__":
    main()
