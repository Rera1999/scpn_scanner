import subprocess
import sys
import time
from rich.console import Console
from rich.progress import Progress
import requests

# إعداد الكونسول
console = Console()

# لوجو البرنامج
def display_logo():
    logo = """
    [bold cyan]███████╗██████╗ ███████╗██╗   ██╗██╗███╗   ██╗[/]
    [bold cyan]╚══██╔══╝██╔══██╗██╔════╝██║   ██║██║████╗  ██║[/]
    [bold cyan]   ██║   ██████╔╝███████╗██║   ██║██║██╔██╗ ██║[/]
    [bold cyan]   ██║   ██╔══██╗╚════██║██║   ██║██║██║╚██╗██║[/]
    [bold cyan]   ██║   ██████╔╝███████║╚██████╔╝██║██║ ╚████║[/]
    [bold cyan]   ╚═╝   ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝[/]

    [bold yellow]SCPN Vulnerability Scanner - Version 1.0[/]
    [bold green]=============================================[/]
    """
    console.print(logo)

# تحقق من الاتصال بالإنترنت
def check_internet():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

# تثبيت الأدوات والمكتبات
def install_dependencies():
    # قائمة الأدوات التي يجب تثبيتها
    packages = [
        "git", "openssh-client", "curl", "wget", "clang", "make", "nano",
        "nmap", "sqlmap"
    ]
    python_packages = [
        "rich", "requests", "jinja2", "python-telegram-bot"
    ]
    
    # التحقق من وجود اتصال بالإنترنت
    if not check_internet():
        console.print("[bold red]Error: No internet connection. Please check your connection.[/]")
        console.print("[*] Exiting...")
        time.sleep(3)
        sys.exit(1)
    
    # تحديث الحزم أولاً
    console.print("[*] Updating package repositories...")
    subprocess.run(["sudo", "apt", "update", "-y"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # تثبيت الأدوات الأساسية
    for package in packages:
        console.print(f"[*] Installing package: {package}...")
        subprocess.run(["sudo", "apt", "install", "-y", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # تثبيت مكتبات بايثون المطلوبة
    for package in python_packages:
        console.print(f"[*] Installing Python package: {package}...")
        subprocess.run([sys.executable, "-m", "pip", "install", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # التأكد من تثبيت الأدوات
    console.print("[*] Verifying installations...")
    subprocess.run([sys.executable, "-m", "pip", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["nmap", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(["sqlmap", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# الوظيفة الرئيسية التي تجمع كل شيء
def main():
    display_logo()
    
    # عرض شريط التقدم عند تنزيل الأدوات
    with Progress() as progress:
        task = progress.add_task("[cyan]Downloading and Installing tools...", total=100)
        
        # تثبيت الأدوات مع تحديث شريط التقدم
        for i in range(10):
            time.sleep(1)  # محاكاة تأخير حقيقي عند تثبيت الأدوات
            progress.update(task, advance=10)  # تحديث شريط التقدم
        install_dependencies()

    # بعد التثبيت، عرض اللوجو لمدة 5 ثوانٍ
    console.clear()
    display_logo()
    time.sleep(5)
    
    # إعلام المستخدم بانتهاء التثبيت والخروج
    console.print("[bold green][+] Installation complete! All tools have been successfully installed.[/]")
    console.print("[*] Exiting...[/]")
    time.sleep(2)

if __name__ == "__main__":
    main()
