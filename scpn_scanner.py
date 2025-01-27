import subprocess
import os
import sys
import shutil
import time
import random
from datetime import datetime

# الألوان لإضفاء لمسة جمالية على المخرجات
class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

# الأدوات المطلوبة
REQUIRED_TOOLS = {
    'nmap': 'Network exploration and security auditing',
    'gobuster': 'Directory/file enumeration tool',
    'msfconsole': 'Metasploit framework console',
    'sslscan': 'SSL/TLS scanner'
}

# عرض اللوجو
def print_banner():
    banners = [
        f"""{colors.CYAN}
          ███████╗ ██████╗██████╗ ███╗   ██╗
          ╚══██╔══╝██╔════╝██╔══██╗████╗  ██║
             ██║   ██║     ██████╔╝██╔██╗ ██║
             ██║   ██║     ██╔═══╝ ██║╚██╗██║
             ██║   ╚██████╗██║     ██║ ╚████║
             ╚═╝    ╚═════╝╚═╝     ╚═╝  ╚═══╝
          Advanced Network and Web Scanner
          {colors.YELLOW}v1.0 - SCPN Scanner{colors.RESET}
        """
    ]
    print(random.choice(banners))

# التحقق من وجود الأدوات المطلوبة
def check_tools():
    missing_tools = [tool for tool in REQUIRED_TOOLS.keys() if not shutil.which(tool)]
    if missing_tools:
        print(f"{colors.RED}[!] الأدوات الناقصة: {', '.join(missing_tools)}{colors.RESET}")
        print(f"{colors.YELLOW}[*] قم بتثبيتها عبر: sudo apt-get install {' '.join(missing_tools)}{colors.RESET}")
        sys.exit(1)

# تنفيذ الأوامر
def run_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

# فحص سريع
def quick_scan(target):
    print(f"{colors.GREEN}[+] فحص سريع للبورتات على الهدف: {target}{colors.RESET}")
    output = run_command(['nmap', '-T4', '-F', target])
    print(output)

# فحص كامل
def full_scan(target):
    print(f"{colors.GREEN}[+] فحص شامل للهدف: {target}{colors.RESET}")
    nmap_output = run_command(['nmap', '-sV', '-A', target])
    gobuster_output = run_command(['gobuster', 'dir', '-u', target, '-w', '/usr/share/wordlists/dirb/common.txt'])
    print(f"{colors.CYAN}[+] نتائج nmap:{colors.RESET}\n{nmap_output}")
    print(f"{colors.CYAN}[+] نتائج gobuster:{colors.RESET}\n{gobuster_output}")

# فحص الثغرات باستخدام Metasploit
def vulnerability_scan(target):
    print(f"{colors.GREEN}[+] فحص الثغرات على الهدف: {target}{colors.RESET}")
    vuln_scan = f"msfconsole -q -x 'db_nmap -sV {target}; vulns; exit'"
    os.system(vuln_scan)

# تحديث الأداة
def update_tool():
    print(f"{colors.YELLOW}[+] جارٍ تحديث الأداة...{colors.RESET}")
    os.system("git pull")
    print(f"{colors.GREEN}[+] تم التحديث بنجاح!{colors.RESET}")

# المساعدة
def show_help():
    print(f"""
    {colors.CYAN}[?] دليل استخدام SCPN Scanner:{colors.RESET}
    1. Quick Scan: فحص سريع للبورتات.
    2. Full Scan: فحص شامل للبورتات والخدمات والملفات.
    3. Vulnerability Scan: فحص الثغرات باستخدام Metasploit.
    4. Update: تحديث الأداة.
    5. Help: عرض هذا الدليل.
    """)

# القائمة الرئيسية
def main():
    print_banner()
    check_tools()
    
    while True:
        print(f"""
        {colors.YELLOW}[*] القائمة الرئيسية:{colors.RESET}
        1. Quick Scan
        2. Full Scan
        3. Vulnerability Scan
        4. Update
        5. Help
        6. Exit
        """)
        
        choice = input(f"{colors.CYAN}[?] اختر الخيار: {colors.RESET}")
        
        if choice == "1":
            target = input(f"{colors.YELLOW}[?] أدخل الهدف (IP/URL): {colors.RESET}")
            quick_scan(target)
        elif choice == "2":
            target = input(f"{colors.YELLOW}[?] أدخل الهدف (IP/URL): {colors.RESET}")
            full_scan(target)
        elif choice == "3":
            target = input(f"{colors.YELLOW}[?] أدخل الهدف (IP/URL): {colors.RESET}")
            vulnerability_scan(target)
        elif choice == "4":
            update_tool()
        elif choice == "5":
            show_help()
        elif choice == "6":
            print(f"{colors.GREEN}[+] إلى اللقاء!{colors.RESET}")
            break
        else:
            print(f"{colors.RED}[!] خيار غير صالح!{colors.RESET}")

if __name__ == "__main__":
    main()
