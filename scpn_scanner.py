import subprocess
import sys
import os
import random
import requests
import time
import json
from datetime import datetime
from jinja2 import Template
import colorama
from colorama import Fore, Style

# تهيئة ألوان التيرمينال
colorama.init(autoreset=True)

class TerminalScanner:
    def __init__(self):
        self.report_data = {
            'vulnerabilities': [],
            'target': '',
            'start_time': datetime.now(),
            'services': []
        }
        
    def display_header(self):
        header = r"""
         _____  _____ _____  _   _ 
        /  ___|/  ___|  ___|| \ | |
        \ `--. \ `--.| |__  |  \| |
         `--. \ `--. \  __| | . ` |
        /\__/ //\__/ / |___ | |\  |
        \____/ \____/\____/ \_| \_/
        """
        print(Fore.CYAN + header)
        print(Fore.YELLOW + "="*55)
        print(Fore.GREEN + "Advanced Vulnerability Scanner v2.0")
        print(Fore.YELLOW + "="*55 + Style.RESET_ALL + "\n")

    def check_tool(self, tool):
        try:
            subprocess.run([tool, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(Fore.GREEN + f"[+] {tool.ljust(10)} installed")
            return True
        except FileNotFoundError:
            print(Fore.RED + f"[!] {tool.ljust(10)} not found!")
            return False

    def scan_nmap(self, target):
        print(Fore.BLUE + "[*] Starting Nmap scan..." + Style.RESET_ALL)
        try:
            result = subprocess.run(
                ["nmap", "-sV", "-T4", "-Pn", target],
                capture_output=True,
                text=True,
                timeout=600
            )
            return result.stdout
        except Exception as e:
            return f"Scan failed: {str(e)}"

    def scan_sqlmap(self, url):
        print(Fore.BLUE + "[*] Starting SQLMap scan..." + Style.RESET_ALL)
        try:
            result = subprocess.run(
                ["sqlmap", "-u", url, "--batch", "--level=3", "--risk=3"],
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.stdout
        except Exception as e:
            return f"Scan failed: {str(e)}"

    def scan_xss(self, url):
        print(Fore.BLUE + "[*] Testing for XSS vulnerabilities..." + Style.RESET_ALL)
        payloads = [
            "<script>alert('XSS1')</script>",
            "<img src=x onerror=alert('XSS2')>",
            "%3Cscript%3Ealert('XSS3')%3C/script%3E"
        ]
        
        vulnerabilities = []
        for payload in payloads:
            try:
                response = requests.get(f"{url}?input={payload}", timeout=10)
                if payload in response.text:
                    vulnerabilities.append(f"XSS detected with payload: {payload}")
            except Exception as e:
                return f"Error: {str(e)}"
        
        return vulnerabilities if vulnerabilities else "No XSS vulnerabilities found"

    def cve_lookup(self, service, version):
        print(Fore.BLUE + "[*] Checking CVE database..." + Style.RESET_ALL)
        try:
            url = f"https://services.nvd.nist.gov/rest/json/cves/1.0?keyword={service} {version}"
            response = requests.get(url, timeout=15)
            cves = response.json().get('result', {}).get('CVE_Items', [])
            
            results = []
            for cve in cves[:5]:  # عرض أول 5 نتائج فقط
                cve_id = cve['cve']['CVE_data_meta']['ID']
                desc = cve['cve']['description']['description_data'][0]['value']
                severity = cve['impact'].get('baseMetricV2', {}).get('severity', 'UNKNOWN')
                results.append(f"{cve_id} ({severity}): {desc}")
            
            return results if results else "No CVEs found"
        except Exception as e:
            return f"CVE lookup failed: {str(e)}"

    def generate_report(self, results):
        print(Fore.BLUE + "[*] Generating HTML report..." + Style.RESET_ALL)
        template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Scan Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 2em; }
                h1 { color: #2c3e50; }
                .vuln { border: 1px solid #ddd; padding: 1em; margin: 1em 0; }
                .critical { background-color: #ffebee; border-color: #ff5252; }
                .high { background-color: #fff3e0; border-color: #ff9100; }
                .medium { background-color: #fffde7; border-color: #ffd600; }
                pre { background-color: #f5f5f5; padding: 1em; overflow-x: auto; }
            </style>
        </head>
        <body>
            <h1>Security Scan Report</h1>
            <p>Generated at: {{ timestamp }}</p>
            <p>Target: {{ target }}</p>
            
            {% for scan in results %}
            <div class="vuln {% if 'critical' in scan.result|lower %}critical{% elif 'high' in scan.result|lower %}high{% elif 'medium' in scan.result|lower %}medium{% endif %}">
                <h3>{{ scan.name }}</h3>
                {% if scan.result is iterable and scan.result is not string %}
                    <ul>
                    {% for item in scan.result %}
                        <li>{{ item }}</li>
                    {% endfor %}
                    </ul>
                {% else %}
                    <pre>{{ scan.result }}</pre>
                {% endif %}
            </div>
            {% endfor %}
        </body>
        </html>
        """
        
        report = Template(template_str).render(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            target=self.report_data['target'],
            results=results
        )
        
        filename = f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
        with open(filename, 'w') as f:
            f.write(report)
        
        print(Fore.GREEN + f"[+] Report saved as {filename}" + Style.RESET_ALL)

    def main_menu(self):
        self.display_header()
        
        # التحقق من الأدوات المطلوبة
        required_tools = ['nmap', 'sqlmap', 'curl']
        for tool in required_tools:
            if not self.check_tool(tool):
                print(Fore.RED + "\n[!] Required tools missing. Exiting...")
                sys.exit(1)
        
        # إدخال الهدف
        target = input(Fore.YELLOW + "\n[?] Enter target IP/URL: " + Style.RESET_ALL)
        self.report_data['target'] = target
        
        # اختيار نوع الفحص
        print(Fore.CYAN + "\nScan Types:")
        print("1. Full Network Scan (Nmap)")
        print("2. Web Application Scan (SQLMap + XSS)")
        print("3. CVE Lookup")
        print("4. Comprehensive Scan (All tests)")
        choice = input(Fore.YELLOW + "\n[?] Select scan type (1-4): " + Style.RESET_ALL)
        
        results = []
        
        if choice in ['1', '4']:
            nmap_result = self.scan_nmap(target)
            results.append({'name': 'Nmap Scan', 'result': nmap_result})
        
        if choice in ['2', '4']:
            sqlmap_result = self.scan_sqlmap(target)
            xss_result = self.scan_xss(target)
            results.extend([
                {'name': 'SQL Injection Scan', 'result': sqlmap_result},
                {'name': 'XSS Scan', 'result': xss_result}
            ])
        
        if choice in ['3', '4']:
            service = input(Fore.YELLOW + "[?] Enter service name (e.g., Apache): " + Style.RESET_ALL)
            version = input(Fore.YELLOW + "[?] Enter service version (e.g., 2.4.49): " + Style.RESET_ALL)
            cve_result = self.cve_lookup(service, version)
            results.append({'name': 'CVE Check', 'result': cve_result})
        
        self.generate_report(results)
        print(Fore.GREEN + "\n[+] Scan completed successfully!")

if __name__ == "__main__":
    scanner = TerminalScanner()
    scanner.main_menu()
