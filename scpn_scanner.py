#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import socket
import argparse
import threading
from queue import Queue
from datetime import datetime

# Configuration
VERSION = "3.0"
REPO_URL = "https://github.com/yourusername/scpn-scanner.git"
DEFAULT_PORTS = "21,22,80,443,3306,8080"
THREADS = 50
TIMEOUT = 2
LOG_FILE = "scan_log.txt"

class NetworkScanner:
    def __init__(self):
        self.queue = Queue()
        self.open_ports = []
        self.lock = threading.Lock()

    def validate_target(self, target):
        try:
            socket.gethostbyname(target)
            return True
        except socket.error:
            return False

    def port_scan(self, target, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(TIMEOUT)
                result = s.connect_ex((target, port))
                if result == 0:
                    with self.lock:
                        self.open_ports.append(port)
        except Exception as e:
            self.log_error(f"Port scan error: {str(e)}")

    def start_workers(self, target):
        for _ in range(THREADS):
            t = threading.Thread(target=self.worker, args=(target,))
            t.daemon = True
            t.start()

    def worker(self, target):
        while True:
            port = self.queue.get()
            self.port_scan(target, port)
            self.queue.task_done()

    def quick_scan(self, target):
        if not self.validate_target(target):
            return None
            
        start_time = time.time()
        ports = [int(p) for p in DEFAULT_PORTS.split(",")]
        
        for port in ports:
            self.queue.put(port)
            
        self.queue.join()
        return {
            "target": target,
            "ports": sorted(self.open_ports),
            "duration": time.time() - start_time
        }

    def full_scan(self, target):
        if not self.validate_target(target):
            return None

        try:
            # Nmap TCP SYN Scan (requires root)
            nmap_result = subprocess.run(
                ["sudo", "nmap", "-sS", "-sV", "-O", "-p-", "-T4", target],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=600
            )
            
            # Web directory brute force
            gobuster_result = subprocess.run(
                ["gobuster", "dir", "-u", f"http://{target}", "-w", 
                 "/usr/share/wordlists/dirb/common.txt"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=300
            )
            
            return {
                "nmap": nmap_result.stdout,
                "gobuster": gobuster_result.stdout
            }
            
        except subprocess.TimeoutExpired:
            self.log_error("Full scan timed out")
            return None

    def vulnerability_scan(self, target):
        try:
            vuln_checks = [
                ("nmap_vuln", ["nmap", "--script", "vuln", "-Pn", target]),
                ("nikto", ["nikto", "-h", target]),
                ("ssl_scan", ["testssl.sh", target])
            ]
            
            results = {}
            for name, cmd in vuln_checks:
                result = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=300
                )
                results[name] = result.stdout
                
            return results
            
        except FileNotFoundError as e:
            self.log_error(f"Tool not found: {str(e)}")
            return None

    def log_error(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"[{timestamp}] ERROR: {message}\n")

    def generate_report(self, data, scan_type):
        filename = f"scan_{scan_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w") as f:
            f.write(f"SCPN Scan Report\n")
            f.write(f"Scan Type: {scan_type}\n")
            f.write(f"Date: {datetime.now()}\n\n")
            
            if scan_type == "quick":
                f.write(f"Target: {data['target']}\n")
                f.write(f"Open Ports: {', '.join(map(str, data['ports']))}\n")
                f.write(f"Scan Duration: {data['duration']:.2f} seconds\n")
                
            elif scan_type == "full":
                f.write("Nmap Results:\n")
                f.write(data.get('nmap', 'No data') + "\n\n")
                f.write("Gobuster Results:\n")
                f.write(data.get('gobuster', 'No data') + "\n")
                
            elif scan_type == "vuln":
                for tool, result in data.items():
                    f.write(f"{tool.upper()} Results:\n")
                    f.write(result + "\n\n")
                    
        return filename

    def update_tool(self):
        try:
            result = subprocess.run(
                ["git", "pull", REPO_URL],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("Update successful!")
                print(result.stdout)
            else:
                print("Update failed:")
                print(result.stderr)
                
        except subprocess.TimeoutExpired:
            self.log_error("Update process timed out")
            print("Update timed out - check internet connection")

def main():
    parser = argparse.ArgumentParser(description="SCPN Advanced Network Scanner")
    parser.add_argument("target", help="Target IP/hostname to scan")
    parser.add_argument("-q", "--quick", action="store_true", help="Perform quick port scan")
    parser.add_argument("-f", "--full", action="store_true", help="Perform comprehensive scan")
    parser.add_argument("-v", "--vuln", action="store_true", help="Perform vulnerability assessment")
    parser.add_argument("-u", "--update", action="store_true", help="Update the tool")
    args = parser.parse_args()

    scanner = NetworkScanner()
    
    if args.update:
        scanner.update_tool()
        return

    if not scanner.validate_target(args.target):
        print("Invalid target specified")
        sys.exit(1)

    if args.quick:
        print(f"Starting quick scan on {args.target}...")
        results = scanner.quick_scan(args.target)
        if results:
            report_file = scanner.generate_report(results, "quick")
            print(f"Scan completed. Report saved to {report_file}")
            
    elif args.full:
        print(f"Starting comprehensive scan on {args.target}...")
        if os.geteuid() != 0:
            print("Full scan requires root privileges")
            sys.exit(1)
            
        results = scanner.full_scan(args.target)
        if results:
            report_file = scanner.generate_report(results, "full")
            print(f"Scan completed. Report saved to {report_file}")
            
    elif args.vuln:
        print(f"Starting vulnerability assessment on {args.target}...")
        results = scanner.vulnerability_scan(args.target)
        if results:
            report_file = scanner.generate_report(results, "vuln")
            print(f"Assessment completed. Report saved to {report_file}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScan aborted by user")
        sys.exit(0)
