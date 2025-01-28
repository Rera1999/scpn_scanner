# Import necessary libraries
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from jinja2 import Template
import subprocess
import requests
import time
import random
import os
import re
from concurrent.futures import ThreadPoolExecutor

# Console for rich text output
console = Console()

# Predefined logos for display
LOGOS = [
    """
     ██████  ██████   ██████  ███    ██
    ██       ██   ██ ██    ██ ████   ██
    ██   ███ ██████  ██    ██ ██ ██  ██
    ██    ██ ██      ██    ██ ██  ██ ██
     ██████  ██       ██████  ██   ████
    """
]

# Function to validate user input
def validate_input(target):
    if re.match(r'^(https?://)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', target):  # Validates URLs
        return True
    elif re.match(r'^\d{1,3}(\.\d{1,3}){3}$', target):  # Validates IPs
        return True
    return False

# Function to display a random logo
def display_logo():
    logo = random.choice(LOGOS)
    console.print(f"[bold cyan]{logo}[/]")
    console.print("[bold yellow]=======================================[/]")
    console.print("[bold green]  SCPN Vulnerability Scanner[/]")
    console.print("[bold yellow]=======================================[/]\n")

# Auto-detection of target type
def detect_target(target):
    console.print("[*] Detecting target type...")
    if target.startswith("http"):
        console.print("[bold green][+] Detected as Website/Application[/]")
        return "web"
    else:
        console.print("[bold green][+] Detected as Router/Server[/]")
        return "network"

# Nmap Scan
def scan_nmap(target):
    console.print("[*] Running Nmap Scan...")
    try:
        with Progress() as progress:
            task = progress.add_task("[cyan]Scanning...", total=100)
            for _ in range(10):
                time.sleep(0.5)
                progress.update(task, advance=10)
        result = subprocess.run(["nmap", "-sV", "-p-", target], stdout=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"[!] Error running Nmap: {e}"

# SQLMap Scan
def scan_sqlmap(url):
    console.print("[*] Running SQLMap...")
    try:
        result = subprocess.run(["sqlmap", "-u", url, "--batch", "--dbs"], stdout=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"[!] Error running SQLMap: {e}"

# XSS Scan
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

# Main Function
def main():
    display_logo()
    console.print("[1] Full Scan (Auto-Detect)")
    console.print("[2] Website/Application Scan")
    console.print("[3] Router/Server Scan")
    choice = console.input("\n[bold cyan]Enter your choice:[/] ")

    target = console.input("[bold yellow]Enter the target (IP or URL): [/]").strip()
    
    # Validate target input
    if not validate_input(target):
        console.print("[bold red][!] Invalid target format! Please enter a valid IP or URL.[/]")
        return

    if choice not in ["1", "2", "3"]:
        console.print("[bold red][!] Invalid Choice! Exiting...[/]")
        return

    # Detect target type
    if choice == "1":
        target_type = detect_target(target)
    elif choice == "2":
        target_type = "web"
    elif choice == "3":
        target_type = "network"

    # Execute scans concurrently
    with ThreadPoolExecutor() as executor:
        nmap_future = executor.submit(scan_nmap, target)
        sqlmap_future = executor.submit(scan_sqlmap, target) if target_type == "web" else None
        xss_future = executor.submit(scan_xss, target) if target_type == "web" else None

        # Get results
        nmap_result = nmap_future.result()
        sqlmap_result = sqlmap_future.result() if sqlmap_future else ""
        xss_result = xss_future.result() if xss_future else ""

    # Display results
    console.print("\n[bold green]Scan Results:[/]")
    console.print(f"[bold cyan]Nmap Results:[/]\n{nmap_result}")
    if target_type == "web":
        console.print(f"[bold cyan]SQLMap Results:[/]\n{sqlmap_result}")
        console.print(f"[bold cyan]XSS Results:[/]\n{xss_result}")

if __name__ == "__main__":
    main()
