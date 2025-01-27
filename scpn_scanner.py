import subprocess
import sys
import time
import os
import random
import requests
import shutil
import platform
from datetime import datetime
from jinja2 import Template

# Terminal colors
class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

# Required tools for Kali Linux
REQUIRED_TOOLS = {
    'nmap': 'Network exploration and security auditing',
    'gobuster': 'Directory/file & DNS busting tool',
    'sslscan': 'SSL/TLS scanner',
    'nbtscan': 'NetBIOS name scanner',
    'nikto': 'Web server vulnerability scanner',
    'sqlmap': 'SQL injection automation tool',
    'hydra': 'Brute-force attack tool',
    'arp-scan': 'ARP packet scanner'
}

def print_banner():
    banners = [
        f"""{colors.CYAN}
         _____  _____ _____  _   _ 
        /  ___|/  ___|  ___|| \ | |
        \ `--. \ `--.| |__  |  \| |
         `--. \ `--. \  __| | . ` |
        /\__/ //\__/ / |___ | |\  |
        \____/ \____/\____/ \_| \_/
        {colors.RESET}""",
        f"""{colors.GREEN}
        ███████╗ ██████╗██████╗ ███╗   ██╗
        ╚══██╔══╝██╔════╝██╔══██╗████╗  ██║
           ██║   ██║     ██████╔╝██╔██╗ ██║
           ██║   ██║     ██╔═══╝ ██║╚██╗██║
           ██║   ╚██████╗██║     ██║ ╚████║
           ╚═╝    ╚═════╝╚═╝     ╚═╝  ╚═══╝
        {colors.RESET}"""
    ]
    print(random.choice(banners))
    print(f"{colors.YELLOW}Advanced Network Scanner v3.0{colors.RESET}")
    print(f"{colors.CYAN}Kali Linux Integrated Security Tools{colors.RESET}\n")

def check_tools():
    missing = []
    for tool, desc in REQUIRED_TOOLS.items():
        if not shutil.which(tool):
            missing.append(tool)
    return missing

def show_help(scan_type):
    help_texts = {
        "quick": "Rapid scan of common ports and services",
        "full": "Comprehensive scan with vulnerability assessment",
        "web": "Full web application security analysis",
        "network": "Network device discovery and analysis",
        "install": "Install missing security tools",
        "update": "Update scanner from GitHub repository"
    }
    print(f"\n{colors.YELLOW}[*] {help_texts.get(scan_type, 'General scan')}{colors.RESET}")

def run_command(cmd, timeout=300):
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Scan timed out"
    except Exception as e:
        return str(e)

# Scanning functions
def quick_scan(target):
    show_help("quick")
    print(f"{colors.CYAN}[*] Starting quick scan on {target}{colors.RESET}")
    results = {
        'nmap': run_command(["nmap", "-T4", "-F", target]),
        'ssl': run_command(["sslscan", target])
    }
    generate_report(target, "Quick Scan", results)

def full_scan(target):
    show_help("full")
    print(f"{colors.CYAN}[*] Starting comprehensive scan on {target}{colors.RESET}")
    results = {
        'nmap': run_command(["nmap", "-sV", "-A", "-T4", "-p-", target]),
        'ssl': run_command(["sslscan", target]),
        'dir': run_command(["gobuster", "dir", "-u", target, "-w", "/usr/share/wordlists/dirb/common.txt"]),
        'vuln': run_command(["nikto", "-h", target])
    }
    generate_report(target, "Full Scan", results)

def web_scan(url):
    show_help("web")
    print(f"{colors.CYAN}[*] Starting web application scan on {url}{colors.RESET}")
    results = {
        'sql': run_command(["sqlmap", "-u", url, "--batch", "--level=3"]),
        'xss': xss_test(url),
        'dir': run_command(["gobuster", "dir", "-u", url, "-w", "/usr/share/wordlists/dirb/common.txt"])
    }
    generate_report(url, "Web Application Scan", results)

def network_scan(network):
    show_help("network")
    print(f"{colors.CYAN}[*] Scanning network: {network}{colors.RESET}")
    devices = run_command(["arp-scan", "--localnet"]).split('\n')
    results = {
        'devices': devices,
        'nbtscan': run_command(["nbtscan", "-r", network]),
        'ports': run_command(["nmap", "-sn", network])
    }
    generate_report(network, "Network Scan", results)

def xss_test(url):
    payloads = ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>"]
    vulnerable = []
    for payload in payloads:
        try:
            res = requests.get(f"{url}?q={payload}", timeout=5)
            if payload in res.text:
                vulnerable.append(payload)
        except:
            pass
    return "XSS vulnerabilities found" if vulnerable else "No XSS detected"

# Report generation
def generate_report(target, scan_type, results):
    template = """
    <html>
    <head>
        <title>Security Scan Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 2em; background: #1a1a1a; color: #fff; }
            h1, h2 { color: #4CAF50; }
            .card { background: #2d2d2d; padding: 1em; margin: 1em 0; border-radius: 5px; }
            pre { background: #000; padding: 1em; overflow-x: auto; }
            button { background: #4CAF50; color: white; border: none; padding: 10px; cursor: pointer; }
            .collapsible { display: none; }
        </style>
    </head>
    <body>
        <h1>Security Scan Report</h1>
        <h2>Scan Type: {{ scan_type }}</h2>
        <h3>Target: {{ target }}</h3>
        <p>Generated: {{ timestamp }}</p>

        {% for section, data in results.items() %}
        <div class="card">
            <h2>{{ section|upper }}</h2>
            <button onclick="toggle('{{ section }}')">Show/Hide Details</button>
            <div id="{{ section }}" class="collapsible">
                <pre>{{ data }}</pre>
            </div>
        </div>
        {% endfor %}

        <script>
            function toggle(id) {
                const elem = document.getElementById(id);
                elem.style.display = elem.style.display === 'none' ? 'block' : 'none';
            }
        </script>
    </body>
    </html>
    """
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = Template(template).render(
        scan_type=scan_type,
        target=target,
        results=results,
        timestamp=timestamp
    )
    
    filename = f"scan_report_{timestamp.replace(':', '')}.html"
    with open(filename, 'w') as f:
        f.write(report)
    
    print(f"{colors.GREEN}[+] Report generated: {filename}{colors.RESET}")

def main():
    print_banner()
    
    # Check dependencies
    missing_tools = check_tools()
    if missing_tools:
        print(f"{colors.RED}[!] Missing tools: {', '.join(missing_tools)}{colors.RESET}")
        choice = input("Install missing tools? (y/n): ").lower()
        if choice == 'y':
            os.system("sudo apt-get install -y " + " ".join(missing_tools))
    
    while True:
        print("\n" + "="*50)
        print(f"{colors.YELLOW}Main Menu{colors.RESET}")
        print("1. Quick Scan")
        print("2. Comprehensive Scan")
        print("3. Web Application Scan")
        print("4. Network Device Scan")
        print("5. Install/Update Tools")
        print("6. Update Scanner")
        print("7. Exit")
        
        choice = input("\n[?] Select option: ")
        
        if choice == "1":
            target = input("[?] Enter target IP/URL: ")
            quick_scan(target)
        elif choice == "2":
            target = input("[?] Enter target IP/URL: ")
            full_scan(target)
        elif choice == "3":
            url = input("[?] Enter website URL: ")
            web_scan(url)
        elif choice == "4":
            network = input("[?] Enter network (e.g., 192.168.1.0/24): ")
            network_scan(network)
        elif choice == "5":
            os.system("sudo apt-get install -y " + " ".join(REQUIRED_TOOLS.keys()))
        elif choice == "6":
            os.system("git pull https://github.com/your-repo/scanner.git")
        elif choice == "7":
            print(f"{colors.GREEN}[+] Exiting...{colors.RESET}")
            break
        else:
            print(f"{colors.RED}[!] Invalid choice{colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{colors.RED}[!] Scan interrupted{colors.RESET}")
        sys.exit(1)
