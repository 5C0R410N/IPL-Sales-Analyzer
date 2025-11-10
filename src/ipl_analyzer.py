#!/usr/bin/env python3
"""
IPL Sales Analyzer - Final Version with Tabula Integration
"""

import os
import sys
import subprocess
import shutil
import hashlib
import time
from datetime import datetime
from pathlib import Path
import re
from collections import Counter

# Color codes for terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Import modules
try:
    import tabula_parser
    TABULA_AVAILABLE = True
except ImportError as e:
    print(f"{Colors.RED}❌ Tabula parser not available: {e}{Colors.RESET}")
    sys.exit(1)

try:
    import calculator_pure_python as calculator
    import core_pure_python as core
except ImportError as e:
    print(f"{Colors.RED}❌ Module import error: {e}{Colors.RESET}")
    sys.exit(1)

# Configuration
USER_DATA_FILE = "user_data.txt"
TARGET_SHARE_FILE = "target_share.txt"
HASH_REGISTRY_FILE = "pdf_hash_registry.txt"
SCRIPT_DIR = Path(__file__).parent

# Professional Display Functions
def clear_line():
    """Clear current line in terminal"""
    sys.stdout.write('\r\033[K')
    sys.stdout.flush()

def print_centered(text, color=Colors.WHITE):
    """Print text centered in terminal"""
    try:
        width = shutil.get_terminal_size().columns
        centered_text = text.center(width)
        print(f"{color}{centered_text}{Colors.RESET}")
    except:
        print(f"{color}{text}{Colors.RESET}")

def show_progress(description, duration=8, color=Colors.CYAN):
    """Show progress bar that clears after completion"""
    frames = [
        '▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯',
        '▮▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯',
        '▮▮▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯',
        '▮▮▮▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯',
        '▮▮▮▮▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯',
        '▮▮▮▮▮▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯',
        '▮▮▮▮▮▮▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯',
        '▮▮▮▮▮▮▮▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯',
        '▮▮▮▮▮▮▮▮▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯',
        '▮▮▮▮▮▮▮▮▮▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯',
        '▮▮▮▮▮▮▮▮▮▮▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯',
        '▮▮▮▮▮▮▮▮▮▮▮▯▯▯▯▯▯▯▯▯▯▯▯▯▯▯',
        '▮▮▮▮▮▮▮▮▮▮▮▮▯▯▯▯▯▯▯▯▯▯▯▯▯▯',
        '▮▮▮▮▮▮▮▮▮▮▮▮▮▯▯▯▯▯▯▯▯▯▯▯▯▯',
        '▮▮▮▮▮▮▮▮▮▮▮▮▮▮▯▯▯▯▯▯▯▯▯▯▯▯',
        '▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▯▯▯▯▯▯▯▯▯▯▯',
        '▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▯▯▯▯▯▯▯▯▯▯',
        '▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▯▯▯▯▯▯▯▯▯',
        '▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▯▯▯▯▯▯▯▯',
        '▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▯▯▯▯▯▯▯',
        '▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▯▯▯▯▯▯',
        '▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▯▯▯▯▯',
        '▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▯▯▯▯',
        '▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▯▯▯',
        '▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▯▯',
        '▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▯',
        '▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮'
    ]
    
    start_time = time.time()
    frame_count = len(frames)
    
    while time.time() - start_time < duration:
        elapsed = time.time() - start_time
        progress = min(elapsed / duration, 1.0)
        current_frame = frames[min(int(progress * frame_count), frame_count - 1)]
        percentage = int(progress * 100)
        
        clear_line()
        print(f"{color}🕒 {description}: [{current_frame}] {percentage}%{Colors.RESET}", end='\r')
        time.sleep(0.1)
    
    clear_line()
    print(f"{Colors.GREEN}✅ {description} completed{Colors.RESET}")

# Hash and File Functions
def calculate_single_file_hash(file_path):
    """Calculate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        return None

def load_hash_registry():
    """Load existing PDF hashes from registry file"""
    registry = set()
    registry_file = SCRIPT_DIR / HASH_REGISTRY_FILE
    
    if registry_file.exists():
        try:
            with open(registry_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 2:
                            registry.add(parts[0])
        except:
            pass
    
    return registry

def save_to_hash_registry(file_hash, filename, file_size, source_folder):
    """Save new PDF hash to registry file"""
    try:
        registry_file = SCRIPT_DIR / HASH_REGISTRY_FILE
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registry_entry = f"{file_hash}|{filename}|{file_size:.2f}MB|{source_folder}|{timestamp}\n"
        
        with open(registry_file, 'a', encoding='utf-8') as f:
            f.write(registry_entry)
    except:
        pass

# Enhanced Hash Registry with Date Storage
def load_enhanced_hash_registry():
    """Load hash registry with date range information"""
    registry = {}
    registry_file = SCRIPT_DIR / HASH_REGISTRY_FILE
    
    if registry_file.exists():
        try:
            with open(registry_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 6:
                            file_hash = parts[0]
                            filename = parts[1]
                            file_size = parts[2]
                            source_folder = parts[3]
                            import_date = parts[4]
                            date_range = parts[5]
                            printed_date = parts[6] if len(parts) > 6 else "Not available"
                            
                            registry[file_hash] = {
                                'filename': filename,
                                'size_mb': file_size,
                                'source': source_folder,
                                'import_date': import_date,
                                'date_range': date_range,
                                'printed_date': printed_date
                            }
        except:
            pass
    
    return registry

def save_enhanced_hash_registry(file_hash, filename, file_size, source_folder, date_range, printed_date):
    """Save to hash registry with date information"""
    try:
        registry_file = SCRIPT_DIR / HASH_REGISTRY_FILE
        import_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        registry_entry = f"{file_hash}|{filename}|{file_size:.2f}MB|{source_folder}|{import_date}|{date_range}|{printed_date}\n"
        
        with open(registry_file, 'a', encoding='utf-8') as f:
            f.write(registry_entry)
    except:
        pass

def extract_dates_from_pdf(file_path):
    """Extract dates from PDF using Tabula"""
    try:
        header_data = tabula_parser.extract_header_from_cut_pdf(file_path)
        
        date_range = "Date range not found"
        if header_data.get('period_from') and header_data.get('period_to'):
            date_range = f"{header_data['period_from']} To {header_data['period_to']}"
        
        printed_date = header_data.get('printed_on', 'Not available')
        
        return date_range, printed_date
        
    except Exception as e:
        return "Date range not found", "Not available"

# Enhanced File Listing with Registry Dates - MODIFIED FOR IMPORT DATE SORTING
def find_pdf_files_with_registry_dates():
    """Find PDF files with date information from registry - SORTED BY IMPORT DATE"""
    source_dir = "/storage/emulated/0/SalesSource"
    pdf_files = []
    
    hash_registry = load_enhanced_hash_registry()
    
    if not os.path.exists(source_dir):
        return []
    
    try:
        for file in os.listdir(source_dir):
            if file.lower().endswith('.pdf'):
                full_path = os.path.join(source_dir, file)
                mod_time = os.path.getmtime(full_path)
                mod_time_str = datetime.fromtimestamp(mod_time).strftime("%d-%m-%y (%I:%M %p)")
                file_size = os.path.getsize(full_path) / (1024 * 1024)
                
                file_hash = calculate_single_file_hash(full_path)
                
                date_range = "Date range not in registry"
                printed_date = "Not available"
                import_timestamp = mod_time  # Default to file modification time
                
                if file_hash and file_hash in hash_registry:
                    registry_data = hash_registry[file_hash]
                    date_range = registry_data.get('date_range', 'Date range not in registry')
                    printed_date = registry_data.get('printed_date', 'Not available')
                    # Get import timestamp from registry if available
                    import_date_str = registry_data.get('import_date', '')
                    if import_date_str:
                        try:
                            import_timestamp = datetime.strptime(import_date_str, "%Y-%m-%d %H:%M:%S").timestamp()
                        except:
                            import_timestamp = mod_time
                else:
                    date_range, printed_date = extract_dates_from_pdf(full_path)
                    if file_hash:
                        save_enhanced_hash_registry(file_hash, file, file_size, "SalesSource", date_range, printed_date)
                
                pdf_files.append({
                    'path': full_path,
                    'name': file,
                    'mod_time_str': mod_time_str,
                    'size_mb': file_size,
                    'date_range': date_range,
                    'printed_date': printed_date,
                    'import_timestamp': import_timestamp  # Add this for sorting
                })
    except Exception as e:
        return []
    
    # SORT BY IMPORT TIMESTAMP (most recent first)
    pdf_files.sort(key=lambda x: x['import_timestamp'], reverse=True)
    return pdf_files

def select_pdf_file_with_dates():
    """Enhanced file selection with date information"""
    print(f"\n{Colors.CYAN}📁 Checking SalesSource directory...{Colors.RESET}")
    pdf_files = find_pdf_files_with_registry_dates()
    
    if not pdf_files:
        print(f"{Colors.RED}❌ No PDF files found in SalesSource directory{Colors.RESET}")
        sys.exit(1)
    
    print(f"\n{Colors.GREEN}📁 Found {len(pdf_files)} PDF file(s) in SalesSource:{Colors.RESET}")
    print("=" * 60)
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f" {Colors.BOLD}{i}. {pdf_file['name']}{Colors.RESET}")
        print(f"    {Colors.YELLOW}📅 Period: {pdf_file['date_range']}{Colors.RESET}")
        if pdf_file['printed_date'] != "Not available":
            print(f"    {Colors.BLUE}🖨️  Printed: {pdf_file['printed_date']}{Colors.RESET}")
        print(f"    {Colors.WHITE}⏰ Modified: {pdf_file['mod_time_str']}{Colors.RESET}")
        print()
    
    while True:
        try:
            choice = input(f"{Colors.CYAN}Select the PDF file Number from above list (1-{len(pdf_files)}) : {Colors.RESET}").strip()
            if not choice:
                continue
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(pdf_files):
                selected_file = pdf_files[choice_num - 1]
                print(f"{Colors.GREEN}✅ Selected: {selected_file['name']}{Colors.RESET}")
                print(f"{Colors.YELLOW}📅 Period: {selected_file['date_range']}{Colors.RESET}")
                if selected_file['printed_date'] != "Not available":
                    print(f"{Colors.BLUE}🖨️  Printed: {selected_file['printed_date']}{Colors.RESET}")
                return selected_file['path']
            else:
                print(f"{Colors.RED}❌ Please enter 1-{len(pdf_files)}{Colors.RESET}")
        except ValueError:
            print(f"{Colors.RED}❌ Please enter a valid number{Colors.RESET}")

# Auto-Import Functions
def scan_downloads_for_pdfs():
    """Scan downloads for PDF files"""
    download_folders = [
        "/storage/emulated/0/Download",
        "/storage/emulated/0/Downloads", 
        "/storage/emulated/0/download",
        "/storage/emulated/0/downloads"
    ]
    
    candidate_pdfs = []
    
    for folder in download_folders:
        if not os.path.exists(folder):
            continue
            
        try:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file.lower().endswith(('.pdf', '.PDF')):
                        file_path = os.path.join(root, file)
                        if not os.path.isfile(file_path):
                            continue
                        file_size = os.path.getsize(file_path) / (1024 * 1024)
                        if 5.0 <= file_size <= 6.0:
                            creation_time = os.path.getctime(file_path)
                            candidate_pdfs.append({
                                'path': file_path,
                                'name': file,
                                'size_mb': file_size,
                                'creation_time': creation_time,
                                'source_folder': root,
                                'relative_path': os.path.relpath(file_path, folder) if root != folder else file
                            })
        except:
            continue
    
    return candidate_pdfs

def find_latest_pdf_in_downloads(known_hashes):
    """Find latest PDF in downloads"""
    candidate_pdfs = scan_downloads_for_pdfs()
    
    if not candidate_pdfs:
        return None
    
    candidate_pdfs.sort(key=lambda x: x['creation_time'], reverse=True)
    latest_pdf = candidate_pdfs[0]
    
    file_hash = calculate_single_file_hash(latest_pdf['path'])
    if not file_hash:
        return None
    
    if file_hash in known_hashes:
        sales_source_path = os.path.join("/storage/emulated/0/SalesSource", latest_pdf['name'])
        if os.path.exists(sales_source_path):
            print(f"{Colors.YELLOW}⏭️  Skipping known file: {latest_pdf['name']}{Colors.RESET}")
            return None
        else:
            print(f"{Colors.GREEN}🔄 File was previously processed but deleted, re-importing: {latest_pdf['name']}{Colors.RESET}")
    
    latest_pdf['hash'] = file_hash
    return latest_pdf

def auto_import_pdf_from_downloads():
    """Auto import PDF from downloads"""
    print(f"{Colors.CYAN}🔍 Scanning Download folders for NEW PDF files...{Colors.RESET}")
    
    show_progress("Scanning download directories", 2)
    
    known_hashes = load_hash_registry()
    latest_pdf = find_latest_pdf_in_downloads(known_hashes)
    
    if not latest_pdf:
        print(f"{Colors.GREEN}✅ No new PDFs found (or all files already processed){Colors.RESET}")
        return None
    
    print(f"{Colors.GREEN}🎯 Found NEW PDF: {latest_pdf['name']}{Colors.RESET}")
    sales_source_dir = "/storage/emulated/0/SalesSource"
    destination_path = os.path.join(sales_source_dir, latest_pdf['name'])
    
    try:
        import shutil
        shutil.move(latest_pdf['path'], destination_path)
        print(f"{Colors.GREEN}✅ Successfully imported to SalesSource{Colors.RESET}")
        save_to_hash_registry(latest_pdf['hash'], latest_pdf['name'], latest_pdf['size_mb'], latest_pdf['source_folder'])
        return destination_path
    except Exception as e:
        print(f"{Colors.RED}❌ Error importing PDF{Colors.RESET}")
        return None

# Command Functions
def get_current_version():
    version_file = SCRIPT_DIR / "version.txt"
    if version_file.exists():
        try:
            with open(version_file, 'r') as f:
                return f.read().strip()
        except:
            pass
    return "v1.0.0"

def show_help():
    print(f"{Colors.CYAN}IPL SALES ANALYZER - HELP{Colors.RESET}")
    print(f"{Colors.WHITE}Usage:{Colors.RESET}")
    print(f"  {Colors.GREEN}report{Colors.RESET}               - Start the analyzer")
    print(f"  {Colors.GREEN}report -u / --update{Colors.RESET} - Check and install updates")
    print(f"  {Colors.GREEN}report -r / --reinstall{Colors.RESET} - Reinstall application")
    print(f"  {Colors.GREEN}report -v / --version{Colors.RESET} - Show version information")
    print(f"  {Colors.GREEN}report -h / --help{Colors.RESET}   - Show this help message")
    print(f"\n{Colors.BLUE}Repository: https://github.com/5C0R410N/IPL-Sales-Analyzer{Colors.RESET}")

def show_version():
    current_version = get_current_version()
    print(f"{Colors.GREEN}IPL Sales Analyzer Version: {current_version}{Colors.RESET}")
    print(f"{Colors.BLUE}Repository: https://github.com/5C0R410N/IPL-Sales-Analyzer{Colors.RESET}")

# Utility Functions
def get_safe_width():
    try:
        return shutil.get_terminal_size().columns
    except:
        return 80

def print_header(title):
    width = get_safe_width()
    print("\n" + "=" * width)
    print_centered(title, Colors.CYAN)
    print("=" * width)

def print_section(title):
    print(f"\n{Colors.YELLOW}{title}{Colors.RESET}")
    print(f"{Colors.YELLOW}{'-' * len(title)}{Colors.RESET}")

def format_current_time():
    return datetime.now().strftime("%I:%M:%S %p")

def get_user_data():
    user_file = SCRIPT_DIR / USER_DATA_FILE
    if user_file.exists():
        try:
            with open(user_file, 'r', encoding='utf-8') as f:
                data = f.read().strip()
                if data:
                    return data
        except:
            pass
    
    print_header("FIRST TIME SETUP")
    print(f"{Colors.WHITE}Welcome to IPL Sales Analyzer!{Colors.RESET}")
    
    while True:
        first_name = input(f"\n{Colors.CYAN}Enter your First Name: {Colors.RESET}").strip()
        last_name = input(f"{Colors.CYAN}Enter your Last Name: {Colors.RESET}").strip()
        
        if first_name and last_name:
            full_name = f"{first_name} {last_name}"
            try:
                with open(user_file, 'w', encoding='utf-8') as f:
                    f.write(full_name)
                print(f"{Colors.GREEN}✅ User data saved: {full_name}{Colors.RESET}")
                return full_name
            except:
                return "User"
        else:
            print(f"{Colors.RED}❌ Please enter both first and last name{Colors.RESET}")

def get_target_share():
    target_file = SCRIPT_DIR / TARGET_SHARE_FILE
    if target_file.exists():
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                data = f.read().strip()
                if data:
                    return float(data)
        except:
            pass
    
    print_header("TARGET SHARE SETUP")
    print(f"{Colors.WHITE}Please set your target share for National Average calculation.{Colors.RESET}")
    print(f"{Colors.WHITE}Example: 0.33 for 33% target share{Colors.RESET}")
    
    while True:
        try:
            target_input = input(f"\n{Colors.CYAN}Enter your Target Share (e.g., 0.33): {Colors.RESET}").strip()
            if not target_input:
                continue
            
            target_share = float(target_input)
            if target_share <= 0:
                print(f"{Colors.RED}❌ Target share must be greater than 0{Colors.RESET}")
                continue
            
            try:
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(str(target_share))
                print(f"{Colors.GREEN}✅ Target share saved: {target_share}{Colors.RESET}")
                return target_share
            except:
                return 0.33
                
        except ValueError:
            print(f"{Colors.RED}❌ Please enter a valid number (e.g., 0.33){Colors.RESET}")

def ensure_directories():
    directories = [
        "/storage/emulated/0/SalesSource",
        "/storage/emulated/0/Analytics_Reports"
    ]
    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
            except:
                return False
    return True

def run_command_with_progress(cmd, desc):
    """Run command with progress display"""
    print(f"{Colors.CYAN}🕒 {desc}...{Colors.RESET}")
    show_progress(desc, 3)
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}❌ Error in {desc}{Colors.RESET}")
        sys.exit(1)

# Product Display Functions - MODIFIED FOR TARGET CALCULATIONS
def display_product_data_list(matching_products, zero_matches, target_share):
    """Display product data with ALL products included in target calculations"""
    all_products = matching_products + zero_matches
    
    if not all_products:
        print(f"{Colors.YELLOW}No products found matching the criteria.{Colors.RESET}")
        return "", 0.0
    
    # Calculate totals from ALL products for target values
    totals = calculator.calculate_totals_python(all_products)
    
    list_content = f"--- Found {len(all_products)} product(s) matching query ---\n"
    list_content += f"   - {len(matching_products)} with sales activity\n"
    list_content += f"   - {len(zero_matches)} with zero sales activity\n\n"
    report_content = list_content

    # Display active products first
    if matching_products:
        list_content += f"--- Products WITH Sales Activity ({len(matching_products)}) ---\n\n"
        report_content += f"--- Products WITH Sales Activity ({len(matching_products)}) ---\n\n"
        
        for product in matching_products:
            entry_str = f"Product Code: {product['code']}\n"
            entry_str += f"Brand Name: {product['brand_name']}\n"
            entry_str += f"    - Target Quantity: {product['tgt_qty']}\n"
            entry_str += f"    - Sold Quantity: {product['sold_qty']}\n"
            entry_str += f"    - In Transit Quantity: {product['int_qty']}\n"
            entry_str += f"    - Target Value (Taka): {product['tgt_val']:.2f}\n"
            entry_str += f"    - Sold Value (Taka): {product['sold_val']:.2f}\n"
            entry_str += f"    - In Transit Value (Taka): {product['int_val']:.2f}\n"
            entry_str += f"    - Total Accounted Value (Sold + In Transit, Taka): {product['total_val']:.2f}\n\n"
            list_content += entry_str
            report_content += entry_str
    
    # Display zero-sales products
    if zero_matches:
        list_content += f"--- Products WITH ZERO Sales Activity ({len(zero_matches)}) ---\n\n"
        report_content += f"--- Products WITH ZERO Sales Activity ({len(zero_matches)}) ---\n\n"
        
        for product in zero_matches:
            entry_str = f"Product Code: {product['code']}\n"
            entry_str += f"Brand Name: {product['brand_name']}\n"
            entry_str += f"    - Target Quantity: {product['tgt_qty']}\n"
            entry_str += f"    - Sold Quantity: {product['sold_qty']}\n"
            entry_str += f"    - In Transit Quantity: {product['int_qty']}\n"
            entry_str += f"    - Target Value (Taka): {product['tgt_val']:.2f}\n"
            entry_str += f"    - Sold Value (Taka): {product['sold_val']:.2f}\n"
            entry_str += f"    - In Transit Value (Taka): {product['int_val']:.2f}\n"
            entry_str += f"    - Total Accounted Value (Taka): {product['total_val']:.2f}\n\n"
            list_content += entry_str
            report_content += entry_str
    
    print(list_content)
    
    totals_content = f"--- Total for ALL matching products ({len(all_products)} products) ---\n"
    totals_content += f"    - Total Target Quantity: {totals['total_tgt_qty']}\n"
    totals_content += f"    - Total Sold Quantity: {totals['total_sold_qty']}\n"
    totals_content += f"    - Total In Transit Quantity: {totals['total_int_qty']}\n"
    totals_content += f"    - Total Accounted Quantity: {totals['total_accounted_qty']}\n"
    totals_content += f"    - Total Target Value (Taka): {totals['total_tgt_val']:.2f}\n"
    totals_content += f"    - Total Sold Value (Taka): {totals['total_sold_val']:.2f}\n"
    totals_content += f"    - Total In Transit Value (Taka): {totals['total_int_val']:.2f}\n"
    totals_content += f"    - Total Accounted Value (Taka): {totals['total_accounted_val']:.2f}\n\n"
    
    print(totals_content)
    report_content += totals_content
    
    national_avg_rounded = calculator.calculate_national_average_python(totals['total_accounted_val'], target_share)
    
    if national_avg_rounded > 0:
        avg_content = f"--- National Average Calculation ---\n"
        avg_content += f"    - Total Accounted Value: {totals['total_accounted_val']:.2f} Taka\n"
        avg_content += f"    - Target Share: {target_share}\n"
        avg_content += f"    - National Average (Crores): {national_avg_rounded}\n\n"
    else:
        avg_content = f"--- National Average Calculation ---\n"
        avg_content += f"    - Calculation skipped (insufficient data)\n\n"
    
    print(avg_content)
    report_content += avg_content
    
    return report_content, national_avg_rounded

def display_zero_value_products_list(zero_matches):
    if not zero_matches:
        return "", 0.0
    
    message = f"--- {len(zero_matches)} product(s) have zero sales ---\n"
    message += "All values are zero (no sales activity)\n\n"
    print(message)
    
    report_content = message
    
    for product in zero_matches:
        entry_str = f"Product Code: {product['code']}\n"
        entry_str += f"Brand Name: {product['brand_name']}\n"
        entry_str += f"    - Target Quantity: {product['tgt_qty']}\n"
        entry_str += f"    - Sold Quantity: {product['sold_qty']}\n"
        entry_str += f"    - In Transit Quantity: {product['int_qty']}\n"
        entry_str += f"    - Target Value (Taka): {product['tgt_val']:.2f}\n"
        entry_str += f"    - Sold Value (Taka): {product['sold_val']:.2f}\n"
        entry_str += f"    - In Transit Value (Taka): {product['int_val']:.2f}\n"
        entry_str += f"    - Total Accounted Value (Taka): {product['total_val']:.2f}\n\n"
        report_content += entry_str
        print(entry_str)
    
    return report_content, 0.0

# MAIN FUNCTION
def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['-u', '--update']:
            # auto_update() - You can implement this later
            print(f"{Colors.YELLOW}Update feature coming soon!{Colors.RESET}")
            return
        elif arg in ['-r', '--reinstall']:
            # reinstall_application() - You can implement this later
            print(f"{Colors.YELLOW}Reinstall feature coming soon!{Colors.RESET}")
            return
        elif arg in ['-h', '--help']:
            show_help()
            return
        elif arg in ['-v', '--version']:
            show_version()
            return
    
    # Initial setup
    print_header("IPL SALES ANALYZER")
    print_centered(f"🕒 {format_current_time()}", Colors.GREEN)
    
    # Get user data
    user_name = get_user_data()
    print(f"{Colors.GREEN}👤 Welcome Back {user_name}!{Colors.RESET}")
    
    # Get target share
    target_share = get_target_share()
    
    # Ensure directories exist
    if not ensure_directories():
        print(f"{Colors.RED}❌ Directory setup failed{Colors.RESET}")
        sys.exit(1)
    
    # AUTO-IMPORT
    print_header("AUTOMATIC PDF IMPORT SYSTEM")
    imported_pdf = auto_import_pdf_from_downloads()
    
    # FILE SELECTION
    pdf_path = select_pdf_file_with_dates()
    
    # Get page range
    default_start_page = 339
    default_end_page = 345
    page_input = input(f"\n{Colors.CYAN}Enter page range (e.g., 110-118) or press Enter for default ({default_start_page}-{default_end_page}): {Colors.RESET}").strip()
    
    if not page_input:
        print(f"{Colors.GREEN}Using default page range: {default_start_page}-{default_end_page}{Colors.RESET}")
        start_page = default_start_page
        end_page = default_end_page
    else:
        try:
            start_page_str, end_page_str = page_input.split('-')
            start_page = int(start_page_str.strip())
            end_page = int(end_page_str.strip())
            if start_page > end_page:
                print(f"{Colors.RED}❌ Start page cannot be greater than end page{Colors.RESET}")
                sys.exit(1)
        except (ValueError, IndexError):
            print(f"{Colors.RED}❌ Invalid page range format{Colors.RESET}")
            sys.exit(1)
    
    print(f"{Colors.BLUE}📄 Page range: {start_page} - {end_page}{Colors.RESET}")
    
    # PROCESS PDF WITH TABULA - USING CUT PDF
    temp_pdf_name = f"temp_extracted_pages_{start_page}_to_{end_page}.pdf"
    
    # Extract pages (creates the CUT PDF)
    pdftk_cmd = f'pdftk "{pdf_path}" cat {start_page}-{end_page} output "{temp_pdf_name}"'
    run_command_with_progress(pdftk_cmd, "Extracting pages")
    
    # PROCESS WITH TABULA USING CUT PDF
    print_header("PROCESSING PDF x MASUD ")
    
    print(f"{Colors.CYAN}🔍 Analyzing PDF with hybrid method...{Colors.RESET}")
    show_progress("Extracting header information", 2)
    
    try:
        # USE TABULA PARSER ON CUT PDF
        structured_data, zero_value_data, header_data = tabula_parser.extract_pdf_data_tabula(temp_pdf_name, f"{start_page}-{end_page}")
        
        # Get territory and date from header
        selected_territory = header_data.get('territory_id', 'Unknown_Territory')
        doc_date_range = f"{header_data.get('period_from', '')} To {header_data.get('period_to', '')}"
        
        print(f"{Colors.GREEN}📍 Territory: {selected_territory}{Colors.RESET}")
        print(f"{Colors.GREEN}📅 Period: {doc_date_range}{Colors.RESET}")
        
        if not structured_data and not zero_value_data:
            print(f"{Colors.RED}❌ No products parsed. Check page range and PDF format.{Colors.RESET}")
            sys.exit(1)
        
        print(f"{Colors.GREEN}✅ Found {len(structured_data)} products with sales activity{Colors.RESET}")
        if zero_value_data:
            print(f"{Colors.YELLOW}ℹ️  Also found {len(zero_value_data)} products with zero sales activity{Colors.RESET}")
            
    except Exception as e:
        print(f"{Colors.RED}❌ Error parsing data with Tabula{Colors.RESET}")
        sys.exit(1)
    
    # Interactive search
    print_header("INTERACTIVE SEARCH")
    print(f"{Colors.WHITE}📍 Territory: {selected_territory}{Colors.RESET}")
    print(f"{Colors.WHITE}📅 Period: {doc_date_range}{Colors.RESET}")
    print(f"{Colors.WHITE}Type product names to search (e.g., 'montair', 'moxquin'){Colors.RESET}")
    print(f"{Colors.WHITE}Type 'quit' to exit and generate report{Colors.RESET}")
    
    session_log = []
    
    while True:
        print_section(f"Search in {selected_territory}")
        product_query = input(f"\n{Colors.CYAN}🔍 Enter product name to search: {Colors.RESET}").strip().lower()
        
        if product_query == 'quit':
            print(f"{Colors.GREEN}👋 Exiting search...{Colors.RESET}")
            break
        
        if not product_query:
            print(f"{Colors.RED}❌ Please enter a product name{Colors.RESET}")
            continue
        
        # Search products - get ALL matching products (active + zero-sales)
        matching_products, zero_matches = calculator.search_products_python(structured_data + zero_value_data, product_query)
        
        if matching_products or zero_matches:
            # Use MODIFIED function that includes ALL products in target calculations
            report_section, avg_val = display_product_data_list(matching_products, zero_matches, target_share)
        else:
            print(f"{Colors.RED}❌ No products found matching '{product_query}'{Colors.RESET}")
            report_section = f"No products found matching '{product_query}'.\n"
            avg_val = 0.0
        
        session_log.append({
            'query': product_query,
            'result_count': len(matching_products) + len(zero_matches),
            'report_content': report_section,
            'national_avg': avg_val
        })
    
    # Generate final report
    if session_log:
        print_header("GENERATING FINAL REPORT")
        
        show_progress("Generating analysis report", 2)
        
        current_time = datetime.now()
        timestamp = current_time.strftime("%H-%M_%d-%m-%y")
        safe_territory = selected_territory.replace(' ', '_').replace('-', '_')
        report_filename = f"{safe_territory}_Report_{timestamp}.txt"
        reports_dir = "/storage/emulated/0/Analytics_Reports"
        report_path = os.path.join(reports_dir, report_filename)
        
        full_report = "--- IPL SALES ANALYSIS REPORT ---\n\n"
        full_report += f"Analyst: {user_name}\n"
        full_report += f"Territory: {selected_territory}\n"
        full_report += f"PDF: {os.path.basename(pdf_path)}\n"
        full_report += f"Pages: {start_page} - {end_page}\n"
        full_report += f"Date Range: {doc_date_range}\n"
        full_report += f"Target Share: {target_share}\n"
        full_report += f"Time: {current_time.strftime('%Y-%m-%d %I:%M:%S %p')}\n\n"
        
        for log_entry in session_log:
            full_report += f"QUERY: '{log_entry['query']}'\n"
            full_report += f"Matches: {log_entry['result_count']} total\n"
            full_report += log_entry['report_content']
            if log_entry['national_avg'] > 0:
                full_report += f"National Average: {log_entry['national_avg']:.2f} Crores\n"
            full_report += "-" * 40 + "\n\n"
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(full_report)
            print(f"{Colors.GREEN}✅ Report saved: {report_path}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}❌ Error saving report{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}❌ No searches performed{Colors.RESET}")
    
    # Cleanup
    print(f"\n{Colors.CYAN}🧹 Cleaning up...{Colors.RESET}")
    if os.path.exists(temp_pdf_name):
        try:
            os.remove(temp_pdf_name)
            print(f"{Colors.GREEN}✅ Deleted: {temp_pdf_name}{Colors.RESET}")
        except:
            pass
    
    # Show useful commands
    print_header("USEFUL COMMANDS")
    print(f"{Colors.WHITE}💡 Quick Commands for Next Time:{Colors.RESET}")
    print(f"  {Colors.GREEN}report -u{Colors.RESET}    - Check and install updates")
    print(f"  {Colors.GREEN}report -r{Colors.RESET}    - Reinstall application")
    print(f"  {Colors.GREEN}report -v{Colors.RESET}    - Show version info")
    print(f"  {Colors.GREEN}report -h{Colors.RESET}    - Show help")
    print(f"\n{Colors.BLUE}📱 Current Version: {get_current_version()}{Colors.RESET}")
    print(f"{Colors.BLUE}🔗 Repository: https://github.com/5C0R410N/IPL-Sales-Analyzer{Colors.RESET}")
    
    print_header("ANALYSIS COMPLETED")
    print_centered(f"{Colors.WHITE}Thanks for using IPL Sales Analyzer!{Colors.RESET}", Colors.WHITE)
    print_centered(f"{Colors.RED}Powered By Team : Operon - Xenovision | XO:24  {Colors.RESET}", Colors.RED)
    print_centered(f"{Colors.RED} © Ahia Masud Emon | Halishahar | Chattogram  {Colors.RESET}", Colors.RED)
    print_centered(f"{Colors.GREEN}🕒 {format_current_time()}{Colors.RESET}", Colors.GREEN)

if __name__ == "__main__":
    main()
