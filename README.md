

# SCPN Vulnerability Scanner

## 🛠️ Introduction
**SCPN Vulnerability Scanner** is a comprehensive tool designed to detect vulnerabilities in websites, web applications, and router devices. It utilizes powerful tools and techniques such as **Nmap**, **SQLMap**, **XSS** testing, and even **Artificial Intelligence** to enhance vulnerability detection.

---

## 🌟 Key Features

### 1. **Multi-target Scanning**
   - Supports scanning websites, web applications, and router devices.
   - Automatically detects the target type (website, application, router/server) based on the provided URL/IP.

### 2. **Integrated Scanning Tools**
   - **Nmap**: A powerful tool for network scanning and port analysis.
   - **SQLMap**: A tool for detecting and exploiting SQL injection vulnerabilities in databases.
   - **XSS**: A tool to test websites for **Cross-Site Scripting (XSS)** vulnerabilities.

### 3. **Beautiful HTML Report**
   - After scanning, the tool generates a visually appealing **HTML** report summarizing the findings.
   - The report includes results from **Nmap**, **SQLMap**, and **XSS** tests.

### 4. **Graphical Terminal Interface**
   - Uses the **Rich** library to enhance the user interface with progress bars, beautiful text formatting, and clear outputs during the scanning process.
   - User-friendly terminal experience.

### 5. **Auto-detection**
   - Automatically detects whether the input is a website, application, or router.
   - Selects appropriate scanning methods based on the target type.

### 6. **AI-Enhanced Scanning**
   - Incorporates Artificial Intelligence algorithms that analyze scan results to enhance vulnerability detection.
   - AI helps identify potential vulnerabilities by analyzing patterns and anomalies in the scan data.

### 7. **Hidden Remote Access (Optional)**
   - **Telegram Bot** integration for remote interaction with the scanner.
   - Enables command execution remotely on the scanner tool through Telegram, ideal for ethical penetration testing purposes.

### 8. **Easy Installation Script**
   - Provides a Python-based installation script that automates the setup of all required tools and libraries.
   - Supports installation in **Termux** or other environments.

---

## 📦 Prerequisites

Before using **SCPN Vulnerability Scanner**, make sure you have the following installed:

- **Python 3.x** (with `pip` for package management)
- **Termux** (if using on Android)
- **Nmap** (for network scanning)
- **SQLMap** (for SQL injection testing)

---

## ⚙️ Installation

To install all necessary dependencies and tools, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/scpn-scanner.git
   cd scpn-scanner

2. Make the installation script executable:

chmod +x setup.py


3. Run the installation script:

python3 setup.py



This script will automatically install Nmap, SQLMap, and all the required Python libraries.


---

🚀 Usage

1. After installation, run the SCPN Vulnerability Scanner:

python3 scpn_scanner.py


2. You will be prompted to enter a target (IP or URL). The tool will auto-detect the type of target (website, application, or router) based on your input.


3. The scanning process will start, and you will see progress bars and stylish output in the terminal.


4. After the scan finishes, the tool will generate a detailed HTML report with the results.




---

📊 Example Output

Here’s an example of how the HTML report will look:

<html>
<head>
    <title>SCPN Vulnerability Report</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333; }
        h1 { color: #444; }
        .section { margin-bottom: 20px; }
        .section h2 { color: #555; }
        .result { background-color: #fff; padding: 10px; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <h1>SCPN Vulnerability Report</h1>
    <div class="section">
        <h2>Nmap Scan Results</h2>
        <div class="result">[Nmap output here]</div>
    </div>
    <div class="section">
        <h2>SQLMap Results</h2>
        <div class="result">[SQLMap output here]</div>
    </div>
    <div class="section">
        <h2>XSS Results</h2>
        <div class="result">[XSS output here]</div>
    </div>
</body>
</html>


---

📝 Notes

This tool is designed for ethical penetration testing and vulnerability assessment only.

Always obtain proper authorization before scanning any website or network.

Use responsibly and ensure compliance with all relevant laws and regulations.



---

📢 Contact

If you have any questions, suggestions, or improvements, feel free to contact us:

Email: rera1999.rera@gmail.com

Telegram: @vvsks
