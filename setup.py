import subprocess
import sys
import time
import os
from rich.console import Console
from rich.progress import Progress
from rich import print

# إعداد الكونسول
console = Console()

# لوجو البرنامج
def display_logo():
    logo = """
    [bold cyan]███ █████ ███  ███ ███ ███[/]
    [bold cyan]   SCPN Vulnerability Scanner[/]
    [bold yellow]=======================================[/]
    """
    console.print(logo)

# تثبيت الأدوات والمكتبات
def install_dependencies():
    # قائمة الأدوات التي يجب تثبيتها
    packages = [
        "python3", "git", "openssh", "curl", "wget", "clang", "make", "nano",
        "nmap", "sqlmap"
    ]
    python_packages = [
        "rich", "requests", "jinja2", "python-telegram-bot"
    ]
    
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

# تشغيل الأداة بعد التثبيت
def run_scanner():
    console.print("[*] Running SCPN Vulnerability Scanner...")
    subprocess.run(["python3", "scpn_scanner.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# الوظيفة الرئيسية التي تجمع كل شيء
def main():
    display_logo()
    
    # عرض شريط التقدم عند تنزيل الأدوات
    with Progress() as progress:
        task = progress.add_task("[cyan]Downloading and Installing tools...", total=100)
        
        for _ in range(10):
            time.sleep(0.5)
            progress.update(task, advance=10)
        
        # تثبيت الأدوات
        install_dependencies()

    # بعد التثبيت، عرض اللوجو لمدة 5 ثوانٍ
    console.clear()
    display_logo()
    time.sleep(5)
    
    # تشغيل أداة الفحص بعد التثبيت
    run_scanner()

if __name__ == "__main__":
    main()
