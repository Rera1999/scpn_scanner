from rich.console import Console
from rich.table import Table
from rich.progress import Progress
import html
import time
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.console = Console(record=True)
        self.styles = {
            'header': 'bold cyan',
            'success': 'bold green',
            'error': 'bold red',
            'warning': 'bold yellow',
            'tool_header': 'white on blue'
        }
    
    def _generate_summary_table(self, results: dict) -> Table:
        table = Table(
            title="Scan Summary",
            box=box.ROUNDED,
            header_style="bold magenta",
            expand=True
        )
        
        table.add_column("Tool", justify="left")
        table.add_column("Status", justify="center")
        table.add_column("Execution Time", justify="right")
        
        for tool, data in results.items():
            status_icon = "✅" if data['status'] == 'completed' else "❌"
            table.add_row(
                tool.upper(),
                f"{status_icon} {data['status'].title()}",
                datetime.now().strftime("%H:%M:%S")
            )
            
        return table
    
    def _parse_tool_results(self, result: dict) -> str:
        if result['status'] != 'completed':
            return f"[{self.styles['error']}]Error: {result['result']}[/]"
            
        if result['tool'] == 'nmap':
            return self._parse_nmap(result['result'])
        elif result['tool'] == 'nikto':
            return self._parse_nikto(result['result'])
        # Add parsers for other tools here
        
        return result['result']
    
    def _parse_nmap(self, output: str) -> str:
        parsed = []
        for line in output.split('\n'):
            if 'open' in line and not line.startswith('#'):
                parts = line.split()
                if len(parts) >= 4:
                    parsed.append(f"Port {parts[0]}: {parts[2]} ({' '.join(parts[3:])})")
        return "\n".join(parsed) if parsed else "No open ports found"
    
    def _parse_nikto(self, output: str) -> str:
        important_findings = [line for line in output.split('\n') if '+ ' in line]
        return "\n".join(important_findings) if important_findings else "No critical findings"
    
    def generate_html_report(self, scan_data: dict) -> str:
        self.console.print(f"\n[bold cyan]SCPN Security Scan Report[/bold cyan]")
        self.console.print(f"[bold]Target:[/] {scan_data['target']}")
        self.console.print(f"[bold]Scan Date:[/] {scan_data['timestamp']}")
        
        # Summary Section
        self.console.print(self._generate_summary_table(scan_data['results']))
        
        # Detailed Results
        for tool, result in scan_data['results'].items():
            self.console.print(f"\n[bold green]{'='*40}[/]")
            self.console.print(f"[{self.styles['tool_header']}]{tool.upper()} RESULTS[/]")
            self.console.print(f"[bold green]{'='*40}[/]\n")
            self.console.print(self._parse_tool_results(result))
        
        # HTML Export
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>SCPN Report - {html.escape(scan_data['target'])}</title>
            <style>
                {self._get_css_styles()}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>SCPN Security Scan Report</h1>
                <div class="scan-info">
                    <p><strong>Target:</strong> {html.escape(scan_data['target'])}</p>
                    <p><strong>Scan Date:</strong> {scan_data['timestamp']}</p>
                </div>
                {self.console.export_html(inline_styles=True)}
            </div>
        </body>
        </html>
        """
    
    def _get_css_styles(self) -> str:
        return """
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        .scan-info { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        pre { 
            background: #1e1e1e; 
            color: #d4d4d4; 
            padding: 15px; 
            border-radius: 5px; 
            overflow-x: auto;
            font-family: 'Consolas', monospace;
        }
        .success { color: #2ecc71; }
        .error { color: #e74c3c; }
        .warning { color: #f1c40f; }
        """