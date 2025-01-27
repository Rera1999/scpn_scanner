import subprocess
import sys
import os
import requests
from datetime import datetime
from jinja2 import Template

# Terminal colors
class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

# Required tools for advanced scanning
REQUIRED_TOOLS = {
    'nmap': 'Network exploration and security auditing',
    'gobuster': 'Directory/file & DNS busting tool',
    'sslscan': 'SSL/TLS scanner',
    'whois': 'Domain information lookup',
    'dig': 'DNS analysis tool',
    'nikto': 'Web server vulnerability scanner',
    'sqlmap': 'SQL injection automation tool',
    'dnsenum': 'DNS enumeration tool',
    'whatweb': 'Web application fingerprinting'
}

def print_banner():
    print(f"""{colors.CYAN}
    ███████╗ █████╗ ██████╗ ██╗   ██╗███████╗██████╗ 
    ██╔════╝██╔══██╗██╔══██╗██║   ██║██╔════╝██╔══██╗
    █████╗  ███████║██████╔╝██║   ██║█████╗  ██████╔╝
    ██╔══╝  ██╔══██║██╔═══╝ ██║   ██║██╔══╝  ██╔═══╝ 
    ██║     ██║  ██║██║     ╚██████╔╝███████╗██║     
    ╚═╝     ╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝╚═╝     
    {colors.RESET}""")
    print(f"{colors.YELLOW}Advanced Network and Web Scanner v4.0{colors.RESET}\n")

def check_tools():
    missing = []
    for tool, desc in REQUIRED_TOOLS.items():
        if not shutil.which(tool):
            missing.append(tool)
    return missing

def run_command(cmd, timeout=300):
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return f"{colors.RED}[!] Command timed out: {' '.join(cmd)}{colors.RESET}"
    except Exception as e:
        return f"{colors.RED}[!] Error: {str(e)}{colors.RESET}"

# Advanced IP or Server Scanning
def analyze_ip(ip):
    print(f"{colors.CYAN}[*] Starting IP analysis: {ip}{colors.RESET}")
    results = {
        'nmap': run_command(["nmap", "-sV", "-A", "-T4", ip]),
        'sslscan': run_command(["sslscan", ip]),
        'whois': run_command(["whois", ip])
    }
    generate_report(ip, "IP Analysis", results)

# Web Application Scanning
def analyze_website(url):
    print(f"{colors.CYAN}[*] Starting web application scan on {url}{colors.RESET}")
    results = {
        'gobuster': run_command(["gobuster", "dir", "-u", url, "-w", "/usr/share/wordlists/dirb/common.txt"]),
        'nikto': run_command(["nikto", "-h", url]),
        'sqlmap': run_command(["sqlmap", "-u", url, "--batch", "--level=3"]),
        'whatweb': run_command(["whatweb", url])
    }
    generate_report(url, "Web Application Analysis", results)

# DNS Analysis
def analyze_dns(domain):
    print(f"{colors.CYAN}[*] Starting DNS analysis for {domain}{colors.RESET}")
    results = {
        'dig': run_command(["dig", domain]),
        'dnsenum': run_command(["dnsenum", domain]),
        'whois': run_command(["whois", domain])
    }
    generate_report(domain, "DNS Analysis", results)

# Report Generation
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
            <pre>{{ data }}</pre>
        </div>
        {% endfor %}
    </body>
    </html>
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = Template(template).render(scan_type=scan_type, target=target, results=results, timestamp=timestamp)
    filename = f"scan_report_{target.replace('.', '_')}.html"
    with open(filename, 'w') as f:
        f.write(report)
    print(f"{colors.GREEN}[+] Report generated: {filename}{colors.RESET}")

# Main Menu
def main():
    print_banner()
    missing_tools = check_tools()
    if missing_tools:
        print(f"{colors.RED}[!] Missing tools: {', '.join(missing_tools)}{colors.RESET}")
        choice = input("Install missing tools? (y/n): ").lower()
        if choice == 'y':
            os.system("sudo apt-get install -y " + " ".join(missing_tools))

    while True:
        print("\n" + "="*50)
        print(f"{colors.YELLOW}Main Menu{colors.RESET}")
        print("1. IP/Server Analysis")
        print("2. Web Application Analysis")
        print("3. DNS Analysis")
        print("4. Exit")

        choice = input("\n[?] Select option: ")

        if choice == "1":
            ip = input("[?] Enter target IP: ")
            analyze_ip(ip)
        elif choice == "2":
            url = input("[?] Enter target URL: ")
            analyze_website(url)
        elif choice == "3":
            domain = input("[?] Enter target domain: ")
            analyze_dns(domain)
        elif choice == "4":
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
