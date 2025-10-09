#!/usr/bin/env python3
"""
IPL Sales Analyzer - Final Optimized Version (Cython + Python Features)
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
import re
from collections import Counter

# Simple direct imports - Cython/Python fallback
try:
    import parser_pure_python
    import calculator_pure_python  
    import core_pure_python
    print("Using Python fallback modules")
    
    parser = parser_pure_python
    calculator = calculator_pure_python
    core = core_pure_python
    
except ImportError as e:
    print(f"Module import error: {e}")
    sys.exit(1)

# Configuration
USER_DATA_FILE = "user_data.txt"
TARGET_SHARE_FILE = "target_share.txt"
SCRIPT_DIR = Path(__file__).parent.parent

def get_safe_width():
    """Gets terminal width or defaults to 80 if unavailable."""
    try:
        return min(shutil.get_terminal_size().columns, 80)
    except OSError:
        return 80

def print_header(title):
    """Print clean header without excessive lines."""
    width = get_safe_width()
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)

def print_section(title):
    """Print simple section separator."""
    width = get_safe_width()
    print("\n" + title)
    print("-" * len(title))

def format_file_time(timestamp):
    """Format file modification time in 12-hour format."""
    return datetime.fromtimestamp(timestamp).strftime("%d-%m-%y (%I:%M %p)")

def format_current_time():
    """Format current time in 12-hour format."""
    return datetime.now().strftime("%I:%M:%S %p")

def get_user_data():
    """Get or create user data"""
    user_file = SCRIPT_DIR / USER_DATA_FILE
    
    if user_file.exists():
        try:
            with open(user_file, 'r', encoding='utf-8') as f:
                data = f.read().strip()
                if data:
                    return data
        except:
            pass
    
    # First time setup
    print_header("FIRST TIME SETUP")
    print("Welcome to IPL Sales Analyzer!")
    
    while True:
        first_name = input("\nEnter your First Name: ").strip()
        last_name = input("Enter your Last Name: ").strip()
        
        if first_name and last_name:
            full_name = f"{first_name} {last_name}"
            try:
                with open(user_file, 'w', encoding='utf-8') as f:
                    f.write(full_name)
                print(f"✅ User data saved: {full_name}")
                return full_name
            except Exception as e:
                print(f"❌ Error saving user data: {e}")
                return "User"
        else:
            print("❌ Please enter both first and last name.")

def get_target_share():
    """Get or create target share data"""
    target_file = SCRIPT_DIR / TARGET_SHARE_FILE
    
    if target_file.exists():
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                data = f.read().strip()
                if data:
                    return float(data)
        except:
            pass
    
    # First time setup
    print_header("TARGET SHARE SETUP")
    print("Please set your target share for National Average calculation.")
    print("Example: 0.33 for 33% target share")
    
    while True:
        try:
            target_input = input("\nEnter your Target Share (e.g., 0.33): ").strip()
            if not target_input:
                print("❌ Please enter a target share value.")
                continue
            
            target_share = float(target_input)
            if target_share <= 0:
                print("❌ Target share must be greater than 0.")
                continue
            
            try:
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(str(target_share))
                print(f"✅ Target share saved: {target_share}")
                return target_share
            except Exception as e:
                print(f"❌ Error saving target share: {e}")
                return 0.33
                
        except ValueError:
            print("❌ Please enter a valid number (e.g., 0.33)")

def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        "/storage/emulated/0/SalesSource",
        "/storage/emulated/0/Analytics_Reports"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"✅ Created directory: {directory}")
            except Exception as e:
                print(f"❌ Error creating directory {directory}: {e}")
                return False
    return True

def run_command(cmd, desc="Running command"):
    """Helper function to run shell commands"""
    print(f"🔄 {desc}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {desc} succeeded.")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error occurred while {desc.lower()}: {e}")
        print(f"Command: {cmd}")
        
        # Cleanup temp files on error
        temp_files = [
            f"temp_extracted_pages_{start_page}_to_{end_page}.pdf",
            f"temp_layout_output_{start_page}_to_{end_page}.txt"
        ]
        
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    print(f"🧹 Deleted temporary file: {temp_file}")
                except OSError:
                    pass
        
        sys.exit(1)

def find_pdf_files():
    """Find PDF files in SalesSource directory with modification times"""
    source_dir = "/storage/emulated/0/SalesSource"
    pdf_files = []
    
    if not os.path.exists(source_dir):
        print(f"❌ SalesSource directory not found: {source_dir}")
        return []
    
    try:
        for file in os.listdir(source_dir):
            if file.lower().endswith('.pdf'):
                full_path = os.path.join(source_dir, file)
                mod_time = os.path.getmtime(full_path)
                mod_time_str = format_file_time(mod_time)
                
                pdf_files.append({
                    'path': full_path,
                    'name': file,
                    'mod_time': mod_time,
                    'mod_time_str': mod_time_str
                })
    except Exception as e:
        print(f"❌ Error scanning directory: {e}")
    
    # Sort by modification time (newest first)
    pdf_files.sort(key=lambda x: x['mod_time'], reverse=True)
    return pdf_files

def select_pdf_file():
    """Let user select PDF file with modification times"""
    print("\n📁 Checking SalesSource directory...")
    pdf_files = find_pdf_files()
    
    if not pdf_files:
        print("❌ No PDF files found in SalesSource directory")
        sys.exit(1)
    
    print(f"\n📄 Found {len(pdf_files)} PDF file(s):")
    
    for i, pdf_file in enumerate(pdf_files, 1):
        file_name = pdf_file['name']
        mod_time_str = pdf_file['mod_time_str']
        print(f"   {i}. {file_name}")
        print(f"      Modified: {mod_time_str}")
    
    while True:
        try:
            choice = input(f"\nSelect PDF file (1-{len(pdf_files)}): ").strip()
            if not choice:
                continue
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(pdf_files):
                selected_file = pdf_files[choice_num - 1]['path']
                selected_name = pdf_files[choice_num - 1]['name']
                selected_time = pdf_files[choice_num - 1]['mod_time_str']
                print(f"✅ Selected: {selected_name}")
                print(f"📅 Modified: {selected_time}")
                return selected_file
            else:
                print(f"❌ Please enter 1-{len(pdf_files)}")
        except ValueError:
            print("❌ Please enter a valid number")

def get_all_territory_ids_from_text(text_file_path):
    """Extracts ALL Territory IDs from the text file"""
    try:
        with open(text_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        territories = []
        
        for line_num, line in enumerate(lines, 1):
            territory_match = re.search(r'Terr Id:\s+([A-Z0-9\-]+)', line)
            if territory_match:
                territory_id = territory_match.group(1)
                territories.append({
                    'id': territory_id,
                    'line': line_num
                })
        
        # Count occurrences of each territory
        territory_counter = Counter([t['id'] for t in territories])
        unique_territories = list(territory_counter.keys())
        
        return territories, unique_territories, territory_counter
        
    except Exception as e:
        print(f"❌ Error extracting territory IDs: {e}")
        return [], ["Unknown_Territory"], Counter()

def select_territory(unique_territories, territory_counter):
    """Let user select which territory to analyze."""
    if len(unique_territories) <= 1:
        if unique_territories:
            print(f"📍 Single territory detected: {unique_territories[0]}")
            return unique_territories[0]
        else:
            return "Unknown_Territory"
    
    # Multiple territories found - let user choose
    print(f"\n🔍 Found {len(unique_territories)} territories:")
    
    for i, territory in enumerate(unique_territories, 1):
        count = territory_counter[territory]
        print(f"   {i}. {territory} (appears {count} times)")
    
    while True:
        try:
            choice = input(f"\nSelect territory (1-{len(unique_territories)}): ").strip()
            if not choice:
                continue
                
            choice_num = int(choice)
            if 1 <= choice_num <= len(unique_territories):
                selected_territory = unique_territories[choice_num - 1]
                print(f"✅ Selected: {selected_territory}")
                return selected_territory
            else:
                print(f"❌ Please enter 1-{len(unique_territories)}")
        except ValueError:
            print("❌ Please enter a valid number")

def get_date_range_for_territory(text_file_path, selected_territory):
    """Extracts date range from the text file"""
    try:
        with open(text_file_path, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        # Look for date range pattern
        date_match = re.search(r'From : (\d{2}-[A-Z]{3}-\d{2})\s+To\s+(\d{2}-[A-Z]{3}-\d{2})', text_content)
        if date_match:
            from_date = date_match.group(1)
            to_date = date_match.group(2)
            return f"{from_date} To {to_date}"
        else:
            return "Date range not found"
    except Exception as e:
        print(f"❌ Error extracting date range: {e}")
        return "Unknown Date Range"

def display_product_data_list(matching_products, target_share):
    """Display product data in list format"""
    if not matching_products:
        print("No products found matching the criteria.")
        return "", 0.0
    
    # Use calculator module for fast calculations
    totals = calculator.calculate_totals_python(matching_products)
    
    # List display
    list_content = f"--- Found {len(matching_products)} product(s) matching query ---\n\n"
    report_content = list_content
    
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
    
    print(list_content)
    
    # Totals display
    totals_content = f"--- Total for matching products ---\n"
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
    
    # National Average calculation
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
    """Display zero-value products in list format"""
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

def main():
    global start_page, end_page
    
    # Initial setup
    print_header("IPL SALES ANALYZER")
    print(f"🕒 {format_current_time()}")
    
    # Get user data
    user_name = get_user_data()
    print(f"👤 Welcome Back {user_name}!")
    
    # Get target share
    target_share = get_target_share()
    
    # Ensure directories exist
    if not ensure_directories():
        print("❌ Directory setup failed.")
        sys.exit(1)
    
    # Select PDF file
    pdf_path = select_pdf_file()
    
    # Get page range
    default_start_page = 339
    default_end_page = 345
    page_input = input(f"\nEnter page range (e.g., 110-118) or press Enter for default ({default_start_page}-{default_end_page}): ").strip()
    
    if not page_input:
        print(f"Using default page range: {default_start_page}-{default_end_page}")
        start_page = default_start_page
        end_page = default_end_page
    else:
        try:
            start_page_str, end_page_str = page_input.split('-')
            start_page = int(start_page_str.strip())
            end_page = int(end_page_str.strip())
            if start_page > end_page:
                print("❌ Start page cannot be greater than end page.")
                sys.exit(1)
        except (ValueError, IndexError):
            print("❌ Invalid page range format. Please use 'start-end'.")
            sys.exit(1)
    
    print(f"📄 Page range: {start_page} - {end_page}")
    
    # Process PDF
    temp_pdf_name = f"temp_extracted_pages_{start_page}_to_{end_page}.pdf"
    temp_text_name = f"temp_layout_output_{start_page}_to_{end_page}.txt"
    
    print(f"\n📖 Extracting pages {start_page} to {end_page}...")
    pdftk_cmd = f'pdftk "{pdf_path}" cat {start_page}-{end_page} output "{temp_pdf_name}"'
    run_command(pdftk_cmd, "Extracting pages")
    
    print("🔤 Converting PDF to text...")
    pdftotext_cmd = f'pdftotext -layout "{temp_pdf_name}" "{temp_text_name}"'
    run_command(pdftotext_cmd, "Converting PDF to text")
    
    # Detect and Select Territory
    print("🔍 Analyzing territory information...")
    territories, unique_territories, territory_counter = get_all_territory_ids_from_text(temp_text_name)
    
    selected_territory = select_territory(unique_territories, territory_counter)
    doc_date_range = get_date_range_for_territory(temp_text_name, selected_territory)
    
    print(f"\n📍 Territory: {selected_territory}")
    print(f"📅 Date Range: {doc_date_range}")
    
    # Parse data using Cython-optimized parser
    print("📊 Parsing sales data...")
    
    try:
        structured_data, zero_value_data = parser.parse_layout_text_for_territory_python(temp_text_name, selected_territory)
    except Exception as e:
        print(f"❌ Error parsing data: {e}")
        # Cleanup
        for temp_file in [temp_pdf_name, temp_text_name]:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        sys.exit(1)
    
    if not structured_data and not zero_value_data:
        print("❌ No products parsed. Check page range and territory.")
        for temp_file in [temp_pdf_name, temp_text_name]:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        sys.exit(1)
    
    print(f"✅ Found {len(structured_data)} products with sales activity.")
    if zero_value_data:
        print(f"ℹ️  Also found {len(zero_value_data)} products with zero sales activity.")
    
    # Interactive search
    print_header("INTERACTIVE SEARCH")
    print(f"📍 Territory: {selected_territory}")
    print(f"📅 Period: {doc_date_range}")
    print("Type product names to search (e.g., 'montair', 'moxquin')")
    print("Type 'quit' to exit and generate report")
    
    session_log = []
    
    while True:
        print_section(f"Search in {selected_territory}")
        product_query = input("\n🔍 Enter product name to search: ").strip().lower()
        
        if product_query == 'quit':
            print("👋 Exiting search...")
            break
        
        if not product_query:
            print("❌ Please enter a product name.")
            continue
        
        # Fast search using Cython-optimized calculator
        matching_products, zero_matches = calculator.search_products_python(structured_data + zero_value_data, product_query)
        
        if matching_products:
            report_section, avg_val = display_product_data_list(matching_products, target_share)
        elif zero_matches:
            print(f"⚠️  '{product_query}' has no sales activity.")
            report_section, avg_val = display_zero_value_products_list(zero_matches)
        else:
            print(f"❌ No products found matching '{product_query}'.")
            report_section = f"No products found matching '{product_query}'.\n"
            avg_val = 0.0
        
        session_log.append({
            'query': product_query,
            'result_count': len(matching_products) + len(zero_matches),
            'non_zero_result_count': len(matching_products),
            'zero_result_count': len(zero_matches),
            'report_content': report_section,
            'national_avg': avg_val
        })
    
    # Generate final report
    if session_log:
        print_header("GENERATING FINAL REPORT")
        
        # Generate filename
        current_time = datetime.now()
        timestamp = current_time.strftime("%H-%M_%d-%m-%y")
        safe_territory = selected_territory.replace(' ', '_').replace('-', '_')
        report_filename = f"{safe_territory}_Report_{timestamp}.txt"
        
        reports_dir = "/storage/emulated/0/Analytics_Reports"
        report_path = os.path.join(reports_dir, report_filename)
        
        # Prepare report content
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
        
        # Save report
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(full_report)
            print(f"✅ Report saved: {report_path}")
        except Exception as e:
            print(f"❌ Error saving report: {e}")
    
    else:
        print("\n❌ No searches performed.")
    
    # Cleanup
    print("\n🧹 Cleaning up...")
    for temp_file in [temp_pdf_name, temp_text_name]:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                print(f"✅ Deleted: {temp_file}")
            except OSError:
                pass
    
    print_header("ANALYSIS COMPLETED")
    print("Thanks for using IPL Sales Analyzer!")
    print(f"🕒 {format_current_time()}")

if __name__ == "__main__":
    main()
