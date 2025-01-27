import subprocess
import sys
import os
import random
import requests
import shutil
import platform
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from fpdf import FPDF
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
    'arp-scan': 'ARP packet scanner',
    'testssl.sh': 'Advanced SSL/TLS analysis'
}

# Banner display
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

# Check missing tools
def check_tools():
    missing = []
    for tool, desc in REQUIRED_TOOLS.items():
        if not shutil.which(tool):
            missing.append(tool)
    return missing

# Install missing tools
def auto_install_tools():
    missing_tools = check_tools()
    if missing_tools:
        print(f"{colors.YELLOW}[*] Installing missing tools: {', '.join(missing_tools)}{colors.RESET}")
        for tool in missing_tools:
            os.system(f"sudo apt install {tool} -y")
    else:
        print(f"{colors.GREEN}[+] All required tools are installed.{colors.RESET}")

# Run command safely
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
        return "Command timed out"
    except Exception as e:
        return str(e)

# SSL/TLS analysis
def ssl_analysis(target):
    print(f"{colors.CYAN}[*] Running SSL/TLS analysis on {target}{colors.RESET}")
    results = {
        'sslscan': run_command(["sslscan", target]),
        'testssl.sh': run_command(["testssl.sh", target]),
        'cipher_check': run_command(["nmap", "--script", "ssl-enum-ciphers", "-p", "443", target])
    }
    return results

# Generate PDF report
def generate_pdf_report(data, scan_type):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Security Audit Report - {scan_type}", ln=1, align='C')
    pdf.cell(200, 10, txt=f"Date: {datetime.now()}", ln=1)

    for section, content in data.items():
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(200, 10, txt=section, ln=1, fill=True)
        pdf.multi_cell(0, 10, txt=content)

    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf.output(filename)
    print(f"{colors.GREEN}[+] PDF Report generated: {filename}{colors.RESET}")

# Main menu display
def show_menu():
    print(f"\n{colors.YELLOW}Main Menu:{colors.RESET}")
    print("1. 🚀 Quick Network Scan")
    print("2. 🔍 Full Vulnerability Audit")
    print("3. 🌐 Web Application Analysis")
    print("4. 📡 Network Device Discovery")
    print("5. 🛠️ Manage Tools")
    print("6. ℹ️ Help & Documentation")
    print("7. 🚪 Exit")

# Main function
def main():
    print_banner()

    # Check dependencies
    auto_install_tools()

    while True:
        show_menu()
        choice = input("\n[?] Select option: ")

        if choice == "1":
            target = input("[?] Enter target IP/URL: ")
            results = ssl_analysis(target)
            generate_pdf_report(results, "Quick Scan")
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
