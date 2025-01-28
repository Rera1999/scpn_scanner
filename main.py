from rich.prompt import Prompt
from rich.progress import Progress, BarColumn, TextColumn
from scanner.scanner import full_scan, validate_target, load_config
from scanner.report_generator import ReportGenerator
import subprocess
import time
import random
import os
import logging

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("scpn_scanner.log"),
        logging.StreamHandler()
    ]
)

console = Console()

def display_logo():
    logo = """
     ██████  ██████   ██████  ███    ██
    ██       ██   ██ ██    ██ ████   ██
    ██   ███ ██████  ██    ██ ██ ██  ██
    ██    ██ ██      ██    ██ ██  ██ ██
     ██████  ██       ██████  ██   ████
    """
    console.print(f"[bold cyan]{logo}[/]")
    console.print("[bold yellow]=======================================[/]")
    console.print("[bold green]  Advanced Network Security Scanner[/]")
    console.print("[bold yellow]=======================================[/]\n")

def update_tools():
    tools = load_config()['tools'].keys()
    console.print(f"[*] Updating {len(tools)} security tools...")
    try:
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y"] + list(tools), check=True)
        console.print("[bold green][+] Tools updated successfully![/]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red][!] Failed to update tools: {e}[/]")

def main_menu():
    display_logo()
    console.print("[1] Full Security Scan")
    console.print("[2] Update Security Tools")
    console.print("[3] Generate Sample Report")
    console.print("[4] Exit")
    return Prompt.ask("\n[bold cyan]Select an option[/]", choices=["1", "2", "3", "4"])

def run_full_scan():
    target = Prompt.ask("[bold yellow]Enter target (IP/URL)[/]")
    if not validate_target(target):
        console.print("[bold red][!] Invalid target format![/]")
        return
    
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        transient=True
    ) as progress:
        task = progress.add_task("[cyan]Running Full Security Scan...", total=1)
        
        try:
            scan_data = full_scan(target)
            report = ReportGenerator().generate_html_report(scan_data)
            
            filename = f"scan_report_{time.strftime('%Y%m%d_%H%M%S')}.html"
            with open(filename, "w") as f:
                f.write(report)
            
            progress.update(task, completed=1)
            console.print(f"\n[bold green]Scan completed! Report saved to {filename}[/]")
            console.print(f"[bold]Open report with: [cyan]xdg-open {filename}[/]")
            
        except Exception as e:
            console.print(f"[bold red]Scan failed: {str(e)}[/]")
            logging.error(f"Scan failed: {str(e)}")

if __name__ == "__main__":
    while True:
        choice = main_menu()
        
        if choice == "1":
            run_full_scan()
        elif choice == "2":
            update_tools()
        elif choice == "3":
            ReportGenerator().generate_html_report({
                'target': 'example.com',
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                'results': {}
            })
        elif choice == "4":
            console.print("[bold yellow]Exiting... Goodbye![/]")
            break
        
        input("\nPress Enter to continue...")
        os.system('clear' if os.name == 'posix' else 'cls')