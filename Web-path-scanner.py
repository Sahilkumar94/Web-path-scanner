import requests
import sys
import re
import json
from datetime import datetime

def is_valid_ip(ip):
    """Check if the input is a valid IPv4 address."""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False

def is_valid_url(url):
    """Check if the input looks like a valid HTTP/HTTPS URL."""
    return re.match(r'^https?://[^\s/$.?#].[^\s]*$', url, re.IGNORECASE) is not None

def get_target_input():
    """Let user choose between IP or URL input."""
    print("\n=== Target Scanner ===")
    print("1. IP Address (e.g., 192.168.1.1)")
    print("2. Full URL (e.g., http://example.com)")
    
    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice == '1':
            ip = input("Enter target IP: ").strip()
            if is_valid_ip(ip):
                return f"http://{ip}"
            print("❌ Invalid IP. Please try again.")
        elif choice == '2':
            url = input("Enter target URL (include http:// or https://): ").strip()
            if is_valid_url(url):
                return url.rstrip('/')
            print("❌ Invalid URL. Please include http:// or https://")
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")

def scan_target(base_url, output_file):
    """Scan the target and save results to a file."""
    results = {
        'target': base_url,
        'timestamp': datetime.now().isoformat(),
        'findings': []
    }
    
    print(f"\n🔍 Scanning: {base_url}\n")
    
    for word in sys.stdin:
        word = word.strip()
        if not word:
            continue
        
        url = f"{base_url}/{word}"
        try:
            res = requests.get(url, timeout=5)
            if res.status_code != 404:
                entry = {
                    'url': url,
                    'status': res.status_code,
                    'content': None
                }
                
                try:
                    entry['content'] = res.json()
                    print(f"[{res.status_code}] {url} (JSON)")
                except ValueError:
                    entry['content'] = res.text[:500]  # Store first 500 chars
                    print(f"[{res.status_code}] {url} (Text)")
                
                results['findings'].append(entry)
                print("-" * 50)
                
        except Exception as e:
            print(f"⚠️ Error with {word}: {str(e)}")
            continue
    
    # Save results to file
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Results saved to: {output_file}")

if __name__ == "__main__":
    target = get_target_input()
    output_file = input("\nEnter output filename (e.g., results.json): ").strip() or "scan_results.json"
    scan_target(target, output_file)