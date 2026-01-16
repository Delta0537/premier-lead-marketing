#!/usr/bin/env python3
"""
Docker API Environment Debugger
Diagnoses connection issues between Python scripts and Docker-hosted services (n8n, GHL)
"""

import os
import sys
import socket
import urllib.request
import urllib.error
import json
from datetime import datetime

def print_header(title):
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def print_status(name, status, details=""):
    icon = "✓" if status else "✗"
    color_status = "PASS" if status else "FAIL"
    print(f"  [{icon}] {name}: {color_status}")
    if details:
        print(f"      → {details}")

def check_env_variables():
    """Check if required environment variables are set"""
    print_header("ENVIRONMENT VARIABLES CHECK")

    env_vars = {
        # n8n variables
        'N8N_API_KEY': os.environ.get('N8N_API_KEY'),
        'N8N_API_URL': os.environ.get('N8N_API_URL'),
        'N8N_HOST': os.environ.get('N8N_HOST'),
        'N8N_BASE_URL': os.environ.get('N8N_BASE_URL'),
        # GHL variables
        'GHL_API_KEY': os.environ.get('GHL_API_KEY'),
        'GHL_LOCATION_ID': os.environ.get('GHL_LOCATION_ID'),
        'GHL_BASE_URL': os.environ.get('GHL_BASE_URL'),
        # Docker-specific
        'DOCKER_HOST': os.environ.get('DOCKER_HOST'),
    }

    found_any = False
    for var, value in env_vars.items():
        if value:
            found_any = True
            masked = value[:10] + "..." if len(value) > 10 else value
            print_status(var, True, f"Set (value: {masked})")
        else:
            print_status(var, False, "Not set")

    if not found_any:
        print("\n  ⚠️  WARNING: No API environment variables detected!")
        print("     Make sure you have set them in your system environment")
        print("     or in a .env file that your script loads.")

    return env_vars

def check_port_connectivity(host, port, service_name):
    """Check if a port is reachable"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            print_status(f"{service_name} ({host}:{port})", True, "Port is open")
            return True
        else:
            print_status(f"{service_name} ({host}:{port})", False, f"Port closed (error code: {result})")
            return False
    except socket.gaierror as e:
        print_status(f"{service_name} ({host}:{port})", False, f"DNS resolution failed: {e}")
        return False
    except socket.timeout:
        print_status(f"{service_name} ({host}:{port})", False, "Connection timed out")
        return False
    except Exception as e:
        print_status(f"{service_name} ({host}:{port})", False, f"Error: {e}")
        return False

def check_network_connectivity():
    """Check network connectivity to various hosts"""
    print_header("NETWORK CONNECTIVITY CHECK")

    hosts_to_check = [
        ("localhost", 5678, "n8n (localhost)"),
        ("127.0.0.1", 5678, "n8n (127.0.0.1)"),
        ("host.docker.internal", 5678, "n8n (Docker internal)"),
    ]

    results = {}
    for host, port, name in hosts_to_check:
        results[name] = check_port_connectivity(host, port, name)

    return results

def test_n8n_api(base_url, api_key):
    """Test n8n API connection"""
    print_header("N8N API TEST")

    if not base_url:
        base_url = "http://localhost:5678"

    # Remove trailing slash
    base_url = base_url.rstrip('/')

    endpoints = [
        (f"{base_url}/api/v1/workflows", "List Workflows"),
        (f"{base_url}/healthz", "Health Check"),
        (f"{base_url}/api/v1/credentials", "List Credentials"),
    ]

    headers = {}
    if api_key:
        headers['X-N8N-API-KEY'] = api_key

    for url, name in endpoints:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                status = response.status
                print_status(name, True, f"HTTP {status} - {url}")
        except urllib.error.HTTPError as e:
            if e.code == 401:
                print_status(name, False, f"HTTP 401 Unauthorized - API key may be invalid")
            elif e.code == 403:
                print_status(name, False, f"HTTP 403 Forbidden - Check API permissions")
            else:
                print_status(name, False, f"HTTP {e.code} - {url}")
        except urllib.error.URLError as e:
            print_status(name, False, f"Connection failed: {e.reason}")
        except Exception as e:
            print_status(name, False, f"Error: {e}")

def test_ghl_api(api_key, location_id):
    """Test GHL (GoHighLevel) API connection"""
    print_header("GHL (GOHIGHLEVEL) API TEST")

    if not api_key:
        print("  ⚠️  GHL_API_KEY not set - skipping GHL tests")
        return

    base_url = "https://services.leadconnectorhq.com"

    # Test location endpoint if location_id is provided
    if location_id:
        url = f"{base_url}/locations/{location_id}"
    else:
        url = f"{base_url}/locations/"

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Version': '2021-07-28',
        'Content-Type': 'application/json'
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.status
            print_status("GHL API Connection", True, f"HTTP {status}")
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print_status("GHL API Connection", False, "HTTP 401 - API key is invalid or expired")
            print("      → You may need to regenerate your GHL API key")
        elif e.code == 403:
            print_status("GHL API Connection", False, "HTTP 403 - Check API permissions/scopes")
        else:
            print_status("GHL API Connection", False, f"HTTP {e.code}")
    except urllib.error.URLError as e:
        print_status("GHL API Connection", False, f"Connection failed: {e.reason}")
    except Exception as e:
        print_status("GHL API Connection", False, f"Error: {e}")

def check_docker_status():
    """Check if Docker is running and accessible"""
    print_header("DOCKER STATUS CHECK")

    try:
        import subprocess
        result = subprocess.run(['docker', 'info'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print_status("Docker Engine", True, "Running")

            # Check for n8n container
            result = subprocess.run(['docker', 'ps', '--filter', 'name=n8n', '--format', '{{.Names}}: {{.Status}}'],
                                  capture_output=True, text=True, timeout=10)
            if result.stdout.strip():
                print_status("n8n Container", True, result.stdout.strip())
            else:
                print_status("n8n Container", False, "No n8n container found running")
        else:
            print_status("Docker Engine", False, result.stderr.strip())
    except FileNotFoundError:
        print_status("Docker CLI", False, "Docker command not found in PATH")
    except subprocess.TimeoutExpired:
        print_status("Docker Engine", False, "Command timed out - Docker may be unresponsive")
    except Exception as e:
        print_status("Docker Engine", False, f"Error: {e}")

def print_recommendations(env_vars, network_results):
    """Print recommendations based on diagnostic results"""
    print_header("RECOMMENDATIONS")

    issues_found = []

    # Check for missing env vars
    if not env_vars.get('N8N_API_KEY'):
        issues_found.append("""
  1. N8N_API_KEY not set:
     - Set it in your system environment variables
     - Windows: setx N8N_API_KEY "your-api-key-here"
     - Or add to .env file: N8N_API_KEY=your-api-key-here
     - Make sure your Python script loads the .env file with python-dotenv""")

    if not env_vars.get('GHL_API_KEY'):
        issues_found.append("""
  2. GHL_API_KEY not set:
     - Set it in your system environment variables
     - Windows: setx GHL_API_KEY "your-api-key-here"
     - Or add to .env file: GHL_API_KEY=your-api-key-here""")

    # Check network connectivity
    localhost_ok = network_results.get("n8n (localhost)", False)
    docker_internal_ok = network_results.get("n8n (Docker internal)", False)

    if not localhost_ok and not docker_internal_ok:
        issues_found.append("""
  3. n8n service not reachable:
     - Make sure n8n is running (check Docker Desktop or start manually)
     - If running in Docker: docker start n8n
     - If running standalone: n8n start
     - Check if port 5678 is blocked by firewall""")

    if localhost_ok and not docker_internal_ok:
        issues_found.append("""
  4. Docker internal networking issue:
     - 'host.docker.internal' not resolving correctly
     - Try using 'localhost' or '127.0.0.1' instead
     - In Docker Desktop settings, ensure 'host.docker.internal' is enabled
     - For WSL2: may need additional network configuration""")

    if not issues_found:
        print("  ✓ No critical issues detected!")
        print("    If still experiencing problems:")
        print("    - Close and reopen your terminal to reload environment variables")
        print("    - Restart Docker Desktop")
        print("    - Regenerate API keys and update configuration")
    else:
        print("  Issues found and recommendations:")
        for issue in issues_found:
            print(issue)

def create_env_template():
    """Create a .env template file"""
    print_header("CREATING .ENV TEMPLATE")

    template = """# n8n Configuration
N8N_API_KEY=your-n8n-api-key-here
N8N_API_URL=http://localhost:5678
# For Docker: N8N_API_URL=http://host.docker.internal:5678

# GHL (GoHighLevel) Configuration
GHL_API_KEY=your-ghl-api-key-here
GHL_LOCATION_ID=your-location-id-here
GHL_BASE_URL=https://services.leadconnectorhq.com

# Optional Docker configuration
# DOCKER_HOST=tcp://localhost:2375
"""

    env_path = ".env.template"
    try:
        with open(env_path, 'w') as f:
            f.write(template)
        print(f"  ✓ Created {env_path}")
        print(f"    Copy to .env and fill in your actual values")
    except Exception as e:
        print(f"  ✗ Failed to create template: {e}")

def main():
    print("\n" + "=" * 60)
    print(" DOCKER API ENVIRONMENT DEBUGGER")
    print(f" Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Run diagnostics
    env_vars = check_env_variables()
    network_results = check_network_connectivity()
    check_docker_status()

    # Test APIs
    n8n_url = env_vars.get('N8N_API_URL') or env_vars.get('N8N_BASE_URL') or "http://localhost:5678"
    n8n_key = env_vars.get('N8N_API_KEY')
    test_n8n_api(n8n_url, n8n_key)

    ghl_key = env_vars.get('GHL_API_KEY')
    ghl_location = env_vars.get('GHL_LOCATION_ID')
    test_ghl_api(ghl_key, ghl_location)

    # Print recommendations
    print_recommendations(env_vars, network_results)

    # Create template
    create_env_template()

    print("\n" + "=" * 60)
    print(" NEXT STEPS")
    print("=" * 60)
    print("""
  1. Set environment variables properly:
     Windows (PowerShell as Admin):
       [System.Environment]::SetEnvironmentVariable('N8N_API_KEY', 'your-key', 'User')
       [System.Environment]::SetEnvironmentVariable('GHL_API_KEY', 'your-key', 'User')

  2. Or create a .env file in your project directory with:
       N8N_API_KEY=eyJhb...your-key
       N8N_API_URL=http://localhost:5678
       GHL_API_KEY=your-ghl-key

  3. Make sure your Python script loads .env:
       from dotenv import load_dotenv
       load_dotenv()

  4. For Docker MCP Toolkit:
     - The API key in Docker Desktop is separate from system env vars
     - Enter the key directly in Docker Desktop > n8n > Configuration > Secrets

  5. Close and reopen your terminal after setting env vars

  6. Restart Docker Desktop if networking issues persist
""")

if __name__ == "__main__":
    main()
