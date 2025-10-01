# 🕵️ Web Path Scanner

A Python tool to discover hidden web paths by brute-forcing directories and endpoints on target websites or IP addresses. Stores results in JSON format for further analysis.

## ✨ Features
- **Dual Input Modes**
  - Scan by IP address (`192.168.1.1`)
  - Scan by full URL (`https://example.com`)
- **Smart Validation**
  - IPv4 format verification
  - URL syntax checking
- **Structured Output**
  - JSON reports with timestamps
  - HTTP status codes and response content
- **Flexible Input**
  - Works with piped wordlists (`cat wordlist.txt | python scanner.py`)
  - Optional custom output filename

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/Sahilumar94/web-path-scanner.git
cd web-path-scanner
pip install -r requirements.txt
