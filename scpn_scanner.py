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

    with Progress() as progress:

        task = progress.add_task("[cyan]Scanning...", total=100)

        for _ in range(10):

            time.sleep(0.5)

            progress.update(task, advance=10)

    result = subprocess.run(["nmap", "-sV", "-p-", target], stdout=subprocess.PIPE, text=True)

    return result.stdout



# SQLMap Scan

def scan_sqlmap(url):

    console.print("[*] Running SQLMap...")

    result = subprocess.run(["sqlmap", "-u", url, "--batch", "--dbs"], stdout=subprocess.PIPE, text=True)

    return result.stdout



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



# Generate HTML Report

def generate_report(steps, nmap_result, sqlmap_result, xss_result):

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

            button { margin-top: 10px; padding: 10px; background-color: #007bff; color: white; border: none; cursor: pointer; }

        </style>

        <script>

            function toggleDetails(stepId) {

                var x = document.getElementById(stepId);

                if (x.style.display === "none") {

                    x.style.display = "block";

                } else {

                    x.style.display = "none";

                }

            }

        </script>

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

    report = Template(template).render(steps=steps, nmap=nmap_result, sqlmap=sqlmap_result, xss=xss_result)

    with open("report.html", "w") as file:

        file.write(report)

    console.print("[bold green][+] Report saved as report.html[/]")



# Main Function

def main():

    display_logo()

    console.print("[1] Full Scan (Auto-Detect)")

    console.print("[2] Website/Application Scan")

    console.print("[3] Router/Server Scan")

    choice = console.input("\n[bold cyan]Enter your choice:[/] ")



    target = console.input("[bold yellow]Enter the target (IP or URL): [/]").strip()

    steps = []

    if choice == "1":

        target_type = detect_target(target)

    elif choice == "2":

        target_type = "web"

    elif choice == "3":

        target_type = "network"

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



    generate_report(steps, nmap_result, sqlmap_result, xss_result)



if __name__ == "__main__":

    main()
