
# SCPN Vulnerability Scanner

## 🛠️ Introduction
**SCPN Vulnerability Scanner** is a comprehensive scanning tool designed to detect vulnerabilities in websites, applications, and router devices. The tool scans and analyzes targets using various tools and techniques like **Nmap**, **SQLMap**, and **XSS** testing. Additionally, the tool supports **Artificial Intelligence** to enhance the scanning and analysis process.

---

## 🌟 Key Features

### 1. **Multi-target Scanning**
   - Supports scanning websites, web applications, and router devices.
   - Auto-detects the target type (website, application, router/server) based on the input URL/IP.

### 2. **Integrated Scanning Tools**
   - **Nmap**: Network scanning and port analysis.
   - **SQLMap**: SQL injection testing for databases.
   - **XSS**: Testing websites for **Cross-Site Scripting (XSS)** vulnerabilities.

### 3. **Beautiful HTML Report**
   - Generates an attractive **HTML** report with the scanning results.
   - Includes detailed information about **Nmap**, **SQLMap**, and **XSS** results.

### 4. **Graphical Terminal Interface**
   - Uses **Rich** library for a user-friendly terminal interface.
   - Displays progress bars, beautiful output, and stylish text formatting during the scanning process.

### 5. **Auto-detection**
   - Automatically detects whether the target is a website, application, or router.
   - Provides appropriate scanning methods based on the detected target type.

### 6. **AI-Enhanced Scanning**
   - Incorporates artificial intelligence to enhance vulnerability detection.
   - AI algorithms analyze the scan results to identify possible vulnerabilities.

### 7. **Hidden Remote Access (Optional)**
   - A **Telegram bot** integration that allows for remote interaction with the tool.
   - Enables running commands on the tool remotely from Telegram without user awareness (for ethical penetration testing purposes).

### 8. **Easy Installation Script**
   - A **Python** installation script that automatically installs all required libraries and tools.
   - Designed for ease of use with **Termux** or other environments.

---

## 📦 Prerequisites

Before using **SCPN Vulnerability Scanner**, you need to have the following tools installed:

- **Python 3.x** (and `pip` for package management)
- **Termux** (if you're using Android)
- **Nmap** (for network scanning)
- **SQLMap** (for SQL injection testing)

---

## ⚙️ Installation

You can easily install all the necessary dependencies and tools using the provided script:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/scpn-scanner.git
   cd scpn-scanner
   ```

2. Make the installation script executable:
   ```bash
   chmod +x setup.py
   ```

3. Run the installation script:
   ```bash
   python3 setup.py
   ```

This script will automatically install all required tools and libraries, including **Nmap**, **SQLMap**, and the necessary Python packages.

---

## 🚀 Usage

1. After the installation, run the **SCPN Vulnerability Scanner**:
   ```bash
   python3 scpn_scanner.py
   ```

2. You will be prompted to enter the target (IP or URL). Depending on the input, the tool will auto-detect the target type (website, application, or router).

3. The scanning process will begin, and you will see progress bars and stylish output in the terminal.

4. After the scan is complete, an **HTML report** will be generated with the results.

---

## 📊 Example Output

Here’s an example of what the HTML report will look like:

```html
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
```

---

## 📝 Notes

- The tool is intended for ethical penetration testing and vulnerability assessment.
- Always get proper authorization before scanning any website or network.
- Use responsibly and in compliance with all relevant laws and regulations.

---

## 📢 Contact

For any questions, suggestions, or improvements, feel free to contact us:

- **Email**: [rera1999.rera@gmail.com](mailto:rera1999.rera@gmail.com)
- **Telegram**: [@vvsks](https://t.me/vvsks)
