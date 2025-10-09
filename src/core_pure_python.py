#!/usr/bin/env python3
"""
IPL Sales Analyzer - Pure Python Core Functions Fallback
Python implementation of core functions when Cython is not available
"""

import os
import re
from datetime import datetime
import pytz

def get_bst_time_python():
    """
    Get current time in Bangladesh Standard Time - Python fallback
    """
    try:
        bst_tz = pytz.timezone('Asia/Dhaka')
        return datetime.now(bst_tz)
    except:
        return datetime.now()

def format_bst_time_python():
    """
    Format current time in Bangladesh Standard Time - Python fallback
    """
    current_time = get_bst_time_python()
    return current_time.strftime("%I:%M:%S %p BST")

def format_bst_date_python():
    """
    Format current date for filename - Python fallback
    """
    current_time = get_bst_time_python()
    return current_time.strftime("%H-%M_%d-%m-%y")

def extract_territory_ids_python(text_content):
    """
    Extract territory IDs from text content - Python fallback
    """
    territories = []
    
    territory_pattern = re.compile(r'Terr Id:\s+([A-Z0-9\-]+)')
    
    for territory_match in territory_pattern.finditer(text_content):
        territory_id = territory_match.group(1)
        territories.append(territory_id)
    
    return territories

def extract_date_range_python(text_content):
    """
    Extract date range from text content - Python fallback
    """
    date_pattern = re.compile(r'From : (\d{2}-[A-Z]{3}-\d{2})\s+To\s+(\d{2}-[A-Z]{3}-\d{2})')
    date_match = date_pattern.search(text_content)
    
    if date_match:
        from_date = date_match.group(1)
        to_date = date_match.group(2)
        return f"{from_date} To {to_date}"
    else:
        return "Unknown Date Range"

def parse_product_line_python(line):
    """
    Parse a single product line - Python fallback
    Returns product data or None if invalid
    """
    # Skip header/footer lines
    skip_words = ["Territory Wise Sale", "Group:", "Terr Id:", "Code Brand Name", "Page", "Total :"]
    for word in skip_words:
        if word in line:
            return None
    
    parts = line.split()
    
    # Validate minimum parts
    if len(parts) < 3:
        return None
    
    code = parts[0]
    
    # Identify numerical values from the end
    num_count = 0
    for i in range(len(parts) - 1, 0, -1):
        try:
            float(parts[i])
            num_count += 1
        except ValueError:
            break
    
    if num_count >= 1:
        number_parts = parts[-num_count:]
        brand_name_parts = parts[1:-num_count]
        
        if not brand_name_parts:
            return None
        
        # Pad or truncate numbers to expected 7 values
        expected_num_values = 7
        if len(number_parts) < expected_num_values:
            padding_needed = expected_num_values - len(number_parts)
            number_parts += ['0'] * padding_needed
        elif len(number_parts) > expected_num_values:
            number_parts = number_parts[-expected_num_values:]
        
        if len(number_parts) != expected_num_values:
            return None
        
        try:
            # Parse numerical values
            numbers = [float(p) for p in number_parts]
            tgt_qty = int(numbers[0])
            sold_qty = int(numbers[1])
            int_qty = int(numbers[2])
            tgt_val = numbers[3]
            sold_val = numbers[4]
            int_val = numbers[5]
            total_val = numbers[6]
            
            # Verify and correct total value
            calculated_total = sold_val + int_val
            if abs(total_val - calculated_total) > 0.01:
                total_val = calculated_total
            
            brand_name = ' '.join(brand_name_parts)
            
            # Check if product has any activity
            has_activity = (
                sold_qty > 0 or
                int_qty > 0 or
                sold_val > 0 or
                int_val > 0 or
                total_val > 0
            )
            
            return {
                'code': code,
                'brand_name': brand_name,
                'tgt_qty': tgt_qty,
                'sold_qty': sold_qty,
                'int_qty': int_qty,
                'tgt_val': tgt_val,
                'sold_val': sold_val,
                'int_val': int_val,
                'total_val': total_val,
                'has_activity': has_activity
            }
            
        except (ValueError, IndexError):
            return None
    
    return None

def get_safe_terminal_width_python():
    """
    Get terminal width safely - Python fallback
    """
    try:
        import shutil
        width = shutil.get_terminal_size().columns
        return min(width, 120) if width > 0 else 100
    except:
        return 100

def validate_page_range_python(page_input, default_start, default_end):
    """
    Validate page range input - Python fallback
    Returns (start_page, end_page, error_message)
    """
    if not page_input.strip():
        return default_start, default_end, None
    
    page_parts = page_input.split('-')
    
    if len(page_parts) != 2:
        return 0, 0, "Invalid page range format. Please use 'start-end' (e.g., 110-118)"
    
    try:
        start_page = int(page_parts[0].strip())
        end_page = int(page_parts[1].strip())
        
        if start_page > end_page:
            return 0, 0, "Start page cannot be greater than end page"
        
        return start_page, end_page, None
        
    except ValueError:
        return 0, 0, "Invalid page numbers. Please use numeric values"
