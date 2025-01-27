import subprocess
import sys
import time
from rich.console import Console
from rich.progress import Progress
import requests
import platform

# إعداد الكونسول
console = Console()

# لوجو البرنامج المحدث
def display_logo():
    logo = """
    [bold cyan]███████╗ ██████╗██████╗ ███╗   ██╗[/]
    [bold cyan]╚══██╔══╝██╔════╝██╔══██╗████╗  ██║[/]
    [bold cyan]   ██║   ██║     ██████╔╝██╔██╗ ██║[/]
    [bold cyan]   ██║   ██║     ██╔═══╝ ██║╚██╗██║[/]
    [bold cyan]   ██║   ╚██████╗██║     ██║ ╚████║[/]
    [bold cyan]   ╚═╝    ╚═════╝╚═╝     ╚═╝  ╚═══╝[/]

    [bold yellow]SCPN Advanced Security Platform - Version 2.0[/]
    [bold green]=================================================[/]
    [bold magenta]AI-Powered | Cloud-Ready | Zero-Trust Integrated[/]
    """
    console.print(logo)

# تحقق من الاتصال بالإنترنت مع إعادة المحاولة
def check_internet(retries=3):
    for i in range(retries):
        try:
            requests.get("https://api.cloudservices.example.com/ping", timeout=5)
            return True
        except (requests.ConnectionError, requests.Timeout):
            console.print(f"[yellow]Retrying internet connection... ({i+1}/{retries})[/]")
            time.sleep(2)
    return False

# تثبيت التبعيات المحدثة
def install_dependencies():
    # تحديد نظام التشغيل
    os_type = platform.system().lower()
    is_linux = os_type == "linux"
    is_wsl = "microsoft" in platform.uname().release.lower()

    # قائمة التبعيات الجديدة
    system_packages = [
        "git", "openssh-client", "curl", "wget", "clang", "make",
        "nmap", "sqlmap", "tor", "proxychains", "awscli", "azure-cli",
        "docker.io", "jq", "libssl-dev", "libffi-dev"
    ]

    python_packages = [
        "rich", "requests", "jinja2", "plotly", "scikit-learn",
        "tensorflow", "python-telegram-bot", "boto3", "azure-identity",
        "pycryptodome", "pytorch", "selenium", "beautifulsoup4",
        "pandas", "numpy", "streamlit", "fastapi", "uvicorn"
    ]

    # التحقق من الاتصال بالإنترنت
    if not check_internet():
        console.print("[bold red]✖ Critical Error: Internet connection required for installation[/]")
        sys.exit(1)

    # تثبيت التبعيات النظامية
    with Progress() as progress:
        # تحديث النظام
        update_task = progress.add_task("[cyan]Updating system packages...", total=1)
        if is_linux:
            subprocess.run(["sudo", "apt", "update", "-y"], check=True)
            subprocess.run(["sudo", "apt", "upgrade", "-y"], check=True)
        progress.update(update_task, advance=1)

        # تثبيت الحزم الأساسية
        install_task = progress.add_task("[cyan]Installing system packages...", total=len(system_packages))
        for pkg in system_packages:
            try:
                if is_linux:
                    subprocess.run(["sudo", "apt", "install", "-y", pkg], check=True)
                progress.update(install_task, advance=1)
            except subprocess.CalledProcessError:
                console.print(f"[red]Failed to install {pkg}[/]")
                sys.exit(1)

    # تثبيت تبعيات بايثون
    with Progress() as progress:
        py_task = progress.add_task("[magenta]Installing Python packages...", total=len(python_packages))
        for pkg in python_packages:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "--user", pkg], check=True)
                progress.update(py_task, advance=1)
            except subprocess.CalledProcessError:
                console.print(f"[red]Failed to install {pkg}[/]")
                sys.exit(1)

    # التكوينات الإضافية
    console.print("[bold cyan]\nRunning post-install configurations...[/]")
    config_steps = [
        ("Initializing Tor service", ["sudo", "systemctl", "enable", "tor"]),
        ("Configuring AWS CLI", ["aws", "configure"]),
        ("Setting up Docker", ["sudo", "usermod", "-aG", "docker", "$USER"]),
        ("Updating vulnerability database", ["git", "clone", "https://github.com/CVEProject/cve-data.git", "cve_db"])
    ]

    for desc, cmd in config_steps:
        try:
            console.print(f"[*] {desc}...")
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            console.print(f"[yellow]Warning: {desc} failed[/]")

# التحقق من التثبيت
def verify_installation():
    console.print("\n[bold green]Verifying installation...[/]")
    checks = {
        "AI Engine": ["python3", "-c", "import sklearn; print(sklearn.__version__)"],
        "Cloud Tools": ["aws", "--version"],
        "Security Tools": ["nmap", "--version"],
        "Tor Network": ["tor", "--version"]
    }

    for name, cmd in checks.items():
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            console.print(f"[green]✓ {name}:[/] {result.stdout.split()[0]}")
        except FileNotFoundError:
            console.print(f"[red]✖ {name} not installed properly[/]")

# الوظيفة الرئيسية
def main():
    display_logo()
    
    console.print("[bold cyan]Starting Advanced Installation Process...[/]\n")
    time.sleep(2)
    
    install_dependencies()
    verify_installation()

    # رسالة الإكمال
    console.print("\n[bold green on black]✅ Installation Completed Successfully![/]")
    console.print("\n[bold]Next Steps:[/]")
    console.print("1. Run [cyan]source ~/.bashrc[/] to refresh environment")
    console.print("2. Configure cloud credentials using [cyan]aws configure[/]")
    console.print("3. Start the AI engine with [cyan]python3 scpn_ai.py[/]\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Installation aborted by user![/]")
        sys.exit(130)
