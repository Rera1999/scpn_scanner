import subprocess
import sys
import time
import os
import random
import requests
from rich.console import Console
from rich.progress import Progress
from jinja2 import Template
import shutil
import platform
import socket

# إعداد الكونسول
console = Console()

# قائمة الشعارات (اللوجو)
LOGOS = [
    """
    ██████  ██████   ██████  ███    ██
    ██       ██   ██ ██    ██ ████   ██
    ██   ███ ██████  ██    ██ ██ ██  ██
    ██    ██ ██      ██    ██ ██  ██ ██
     ██████  ██       ██████  ██   ████
    """,
    """
     _____   _____   _____   _   _
    /  ___| /  _  \ | ____| | | | |
    | |     | | | | | |__   | |_| |
    | |  _  | | | | |  __|  |  _  |
    | |_| | | |_| | | |___  | | | |
    \_____/ \_____/ |_____| |_| |_|
    """,
    """
     ██████  ███████  ██████  ██  ███    ██
    ██       ██      ██       ██  ████   ██
    ██   ███ █████   ██   ███ ██  ██ ██  ██
    ██    ██ ██      ██    ██ ██  ██  ██ ██
     ██████  ███████  ██████  ██  ██   ████
    """
]

# عرض لوجو عشوائي
def display_logo():
    logo = random.choice(LOGOS)
    console.print(f"[bold cyan]{logo}[/]")
    console.print("[bold yellow]======================================= [/]")
    console.print("[bold green]  SCPN Vulnerability Scanner[/]")
    console.print("[bold yellow]======================================= [/]")
    
# التحقق من نوع الهدف
def detect_target(target):
    console.print("[*] Detecting target type...")
    if target.startswith("http"):
        console.print("[bold green][+] Detected as Website/Application[/]")
        return "web"
    else:
        console.print("[bold green][+] Detected as Router/Server[/]")
        return "network"

# فحص Nmap
def scan_nmap(target):
    console.print("[*] Running Nmap Scan...")
    with Progress() as progress:
        task = progress.add_task("[cyan]Scanning...", total=100)
        for _ in range(10):
            time.sleep(0.5)
            progress.update(task, advance=10)
    result = subprocess.run(["nmap", "-sV", "-p-", target], stdout=subprocess.PIPE, text=True)
    return result.stdout

# فحص SQLMap
def scan_sqlmap(url):
    console.print("[*] Running SQLMap...")
    result = subprocess.run(["sqlmap", "-u", url, "--batch", "--dbs"], stdout=subprocess.PIPE, text=True)
    return result.stdout

# فحص XSS
def scan_xss(url):
    console.print("[*] Testing for XSS...")
    payload = "<script>alert('XSS')</script>"
    try:
        response = requests.get(url, params={"input": payload}, timeout=10)
        if payload in response.text:
            return f"[!] XSS Vulnerability Found in {url}"
        else:
            return "[*] No XSS Vulnerability Found."
    except requests.exceptions.RequestException as e:
        return f"[!] Error testing XSS: {e}"

# فحص سريع
def quick_scan(target):
    console.print("[*] Running Quick Scan...")
    result = subprocess.run(["nmap", "-p", "80,443", target], stdout=subprocess.PIPE, text=True)
    return result.stdout

# توليد التقرير HTML
def generate_report(steps, nmap_result, sqlmap_result, xss_result, quick_result):
    console.print("[*] Generating HTML Report...")
    template = """
    <html>
    <head>
        <title>SCPN Vulnerability Report</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333; }
            h1 { color: #444; }
            .section { margin-bottom: 20px; }
            .section h2 { color: #555; }
            .result { background-color: #fff; padding: 10px; border: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <h1>SCPN Vulnerability Report</h1>
        {% for step in steps %}
        <div class="section">
            <h2>{{ step.name }}</h2>
            <div class="result">{{ step.result }}</div>
            <button onclick="toggleDetails('step{{ loop.index }}')">View Details</button>
            <div id="step{{ loop.index }}" style="display:none; margin-top:10px;">
                {{ step.details }}
            </div>
        </div>
        {% endfor %}
        <div class="section">
            <h2>Quick Scan Results</h2>
            <div class="result">{{ quick }}</div>
        </div>
        <div class="section">
            <h2>Nmap Scan Results</h2>
            <div class="result">{{ nmap }}</div>
        </div>
        <div class="section">
            <h2>SQLMap Results</h2>
            <div class="result">{{ sqlmap }}</div>
        </div>
        <div class="section">
            <h2>XSS Results</h2>
            <div class="result">{{ xss }}</div>
        </div>
    </body>
    </html>
    """
    report = Template(template).render(steps=steps, nmap=nmap_result, sqlmap=sqlmap_result, xss=xss_result, quick=quick_result)
    with open("report.html", "w") as file:
        file.write(report)
    console.print("[bold green][+] Report saved as report.html[/]")

# التحقق من وجود أدوات
def check_tools():
    tools = ['nmap', 'sqlmap', 'curl', 'git', 'python3']
    for tool in tools:
        result = subprocess.run(["which", tool], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            console.print(f"[bold red][!] {tool} not found! Please install it.[/]")
        else:
            console.print(f"[bold green][+] {tool} is installed.[/]")

# التحقق من حالة الإنترنت
def check_internet():
    try:
        subprocess.check_call(['ping', '-c', '1', '8.8.8.8'])
        console.print("[bold green][+] Internet connection is working.[/]")
    except subprocess.CalledProcessError:
        console.print("[bold red][!] Internet connection is not available.[/]")

# إضافة التحديثات
def check_updates():
    console.print("[*] Checking for updates...")
    result = subprocess.run(["git", "pull"], stdout=subprocess.PIPE, text=True)
    console.print(result.stdout)

# إعداد الأدوات
def setup_tools():
    console.print("[*] Installing missing tools...")
    try:
        subprocess.check_call(["apt-get", "install", "-y", "nmap", "sqlmap", "curl", "git", "python3-pip"])
        subprocess.check_call(["pip3", "install", "requests", "jinja2", "rich"])
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red][!] Error installing tools: {e}[/]")
    
# التحقق من حالة النظام
def check_system():
    console.print("[*] Checking system info...")
    system_info = platform.uname()
    console.print(f"System: {system_info.system}")
    console.print(f"Node Name: {system_info.node}")
    console.print(f"Release: {system_info.release}")
    console.print(f"Version: {system_info.version}")
    console.print(f"Machine: {system_info.machine}")
    console.print(f"Processor: {system_info.processor}")

# الدالة الرئيسية
def main():
    check_tools()
    check_internet()
    check_system()
    display_logo()
    console.print("[1] Full Scan (Auto-Detect)")
    console.print("[2] Website/Application Scan")
    console.print("[3] Router/Server Scan")
    console.print("[4] Quick Scan")
    console.print("[5] Check for Updates")
    console.print("[6] Install Tools")
    choice = console.input("\n[bold cyan]Enter your choice:[/] ")

    target = console.input("[bold yellow]Enter the target (IP or URL): [/]").strip()
    steps = []
    quick_result = ""

    if choice == "1":
        target_type = detect_target(target)
    elif choice == "2":
        target_type = "web"
    elif choice == "3":
        target_type = "network"
    elif choice == "4":
        quick_result = quick_scan(target)
        steps.append({"name": "Quick Scan", "result": "Completed", "details": quick_result})
        generate_report(steps, "", "", "", quick_result)
        return
    elif choice == "5":
        check_updates()
        return
    elif choice == "6":
        setup_tools()
        return
    else:
        console.print("[bold red][!] Invalid Choice! Exiting...[/]")
        return

    # Nmap Scan
    nmap_result = scan_nmap(target)
    steps.append({"name": "Nmap Scan", "result": "Completed", "details": nmap_result})

    # Conditional Scans for Web Targets
    sqlmap_result, xss_result = "", ""
    if target_type == "web":
        sqlmap_result = scan_sqlmap(target)
        steps.append({"name": "SQLMap Scan", "result": "Completed", "details": sqlmap_result})
        xss_result = scan_xss(target)
        steps.append({"name": "XSS Scan", "result": "Completed", "details": xss_result})

    generate_report(steps, nmap_result, sqlmap_result, xss_result, "")

if __name__ == "__main__":
    main()
