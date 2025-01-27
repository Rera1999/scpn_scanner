
import subprocess
import sys
import time
import os
import random
import requests
from rich.console import Console
from rich.progress import Progress
from jinja2 import Template
import platform
import socket
import threading
from datetime import datetime

console = Console()

LOGOS = [
    """
    ██████  ██████   ██████  ███    ██
    ██       ██   ██ ██    ██ ████   ██
    ██   ███ ██████  ██    ██ ██ ██  ██
    ██    ██ ██      ██    ██ ██  ██ ██
     ██████  ██       ██████  ██   ████
    """
]

def display_logo():
    logo = random.choice(LOGOS)
    console.print(f"[bold cyan]{logo}[/]")
    console.print("[bold yellow]======================================= [/]")
    console.print("[bold green]  SCPN Vulnerability Scanner[/]")
    console.print("[bold yellow]======================================= [/]")

def quick_scan(target):
    console.print("[*] Running Quick Scan...")
    result = subprocess.run(["nmap", "-p", "80,443", target], stdout=subprocess.PIPE, text=True)
    return result.stdout

def full_scan(target):
    console.print("[*] Running Full Scan...")
    result = subprocess.run(["nmap", "-sV", "-p-", target], stdout=subprocess.PIPE, text=True)
    return result.stdout

def ssl_scan(target):
    console.print("[*] Running SSL Analysis...")
    result = subprocess.run(["sslscan", target], stdout=subprocess.PIPE, text=True)
    return result.stdout

def dns_analysis(domain):
    console.print("[*] Running DNS Analysis...")
    result = subprocess.run(["dig", domain], stdout=subprocess.PIPE, text=True)
    return result.stdout

def network_scan():
    console.print("[*] Scanning Network...")
    devices = subprocess.run(["arp-scan", "-l"], stdout=subprocess.PIPE, text=True)
    return devices.stdout

def generate_report(scans):
    console.print("[*] Generating Report...")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    template = """
    <html>
    <head>
        <title>SCPN Vulnerability Report</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #101010; color: #f0f0f0; }
            h1 { color: #e6e600; text-align: center; }
            .section { margin-bottom: 20px; padding: 15px; border-radius: 8px; }
            .result { padding: 10px; border: 1px solid #333; border-radius: 5px; background-color: #222; }
        </style>
    </head>
    <body>
        <h1>SCPN Vulnerability Report</h1>
        <p>Generated on {{ date }}</p>
        {% for scan in scans %}
        <div class="section">
            <h2>{{ scan["name"] }}</h2>
            <pre class="result">{{ scan["output"] }}</pre>
        </div>
        {% endfor %}
    </body>
    </html>
    """
    rendered = Template(template).render(scans=scans, date=date)
    with open("report.html", "w") as f:
        f.write(rendered)
    console.print("[bold green][+] Report saved as report.html[/]")

def main():
    display_logo()
    console.print("[1] Quick Scan")
    console.print("[2] Full Scan")
    console.print("[3] SSL Analysis")
    console.print("[4] DNS Analysis")
    console.print("[5] Network Scan")
    choice = console.input("[bold cyan]Enter your choice: [/]").strip()

    scans = []
    if choice == "1":
        target = console.input("[bold yellow]Enter the target (IP or domain): [/]").strip()
        result = quick_scan(target)
        scans.append({"name": "Quick Scan", "output": result})
    elif choice == "2":
        target = console.input("[bold yellow]Enter the target (IP or domain): [/]").strip()
        result = full_scan(target)
        scans.append({"name": "Full Scan", "output": result})
    elif choice == "3":
        target = console.input("[bold yellow]Enter the target (domain): [/]").strip()
        result = ssl_scan(target)
        scans.append({"name": "SSL Analysis", "output": result})
    elif choice == "4":
        target = console.input("[bold yellow]Enter the target (domain): [/]").strip()
        result = dns_analysis(target)
        scans.append({"name": "DNS Analysis", "output": result})
    elif choice == "5":
        result = network_scan()
        scans.append({"name": "Network Scan", "output": result})
    else:
        console.print("[bold red]Invalid choice. Exiting...[/]")
        return

    generate_report(scans)

if __name__ == "__main__":
    main()
