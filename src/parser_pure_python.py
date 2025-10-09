#!/usr/bin/env python3
"""
IPL Sales Analyzer - Pure Python Parser Fallback
Python implementation of parser functions when Cython is not available
"""

import re
from collections import Counter

def parse_layout_text_for_territory_python(file_path, selected_territory):
    """
    Parse layout text file for specific territory - Python fallback
    Returns (filtered_products, zero_value_products)
    """
    territory_products = []
    filtered_products = []
    zero_value_products = []
    current_territory = None
    in_correct_territory = False
    
    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # First pass: Find territory boundaries and collect products
    for i, line in enumerate(lines):
        # Check if this line starts a new territory section
        territory_match = re.search(r'Terr Id:\s+([A-Z0-9\-]+)', line)
        if territory_match:
            current_territory = territory_match.group(1)
            in_correct_territory = (current_territory == selected_territory)
        
        # Only process product lines if we're in the correct territory
        if in_correct_territory:
            # Skip header/footer lines
            skip_words = ["Territory Wise Sale", "Group:", "Terr Id:", "Code Brand Name", "Page", "Total :"]
            if any(word in line for word in skip_words):
                continue
            
            parts = line.split()
            if len(parts) < 3:
                continue
            
            code = parts[0]
            
            # Identify numerical values from the end of the line
            num_count = 0
            for part in reversed(parts):
                try:
                    float(part)
                    num_count += 1
                except ValueError:
                    break
            
            if num_count >= 1:
                number_parts = parts[-num_count:]
                brand_name_parts = parts[1:-num_count]
                
                if not brand_name_parts:
                    continue
                
                # Pad the number list if less than 7 numbers are found
                expected_num_values = 7
                if len(number_parts) < expected_num_values:
                    padding_needed = expected_num_values - len(number_parts)
                    number_parts += ['0'] * padding_needed
                elif len(number_parts) > expected_num_values:
                    number_parts = number_parts[-expected_num_values:]
                
                if len(number_parts) != expected_num_values:
                    continue
                
                try:
                    # Parse the 7 numerical values
                    numbers = [float(p) for p in number_parts]
                    tgt_qty = int(numbers[0])
                    sold_qty = int(numbers[1])
                    int_qty = int(numbers[2])
                    tgt_val = numbers[3]
                    sold_val = numbers[4]
                    int_val = numbers[5]
                    total_val = numbers[6]
                    
                    # Verify and correct total value if needed
                    calculated_total = sold_val + int_val
                    if abs(total_val - calculated_total) > 0.01:
                        total_val = calculated_total
                    
                    brand_name = ' '.join(brand_name_parts)
                    
                    product_entry = {
                        'code': code,
                        'brand_name': brand_name,
                        'tgt_qty': tgt_qty,
                        'sold_qty': sold_qty,
                        'int_qty': int_qty,
                        'tgt_val': tgt_val,
                        'sold_val': sold_val,
                        'int_val': int_val,
                        'total_val': total_val,
                        'territory': current_territory
                    }
                    territory_products.append(product_entry)
                    
                except (ValueError, IndexError):
                    continue
    
    # Separate products based on activity
    for product in territory_products:
        # Check if product has any sales activity
        has_activity = (
            product['sold_qty'] > 0 or
            product['int_qty'] > 0 or
            product['sold_val'] > 0 or
            product['int_val'] > 0 or
            product['total_val'] > 0
        )
        
        if has_activity:
            filtered_products.append(product)
        else:
            zero_value_products.append(product)
    
    return filtered_products, zero_value_products

def get_all_territory_ids_python(file_path):
    """
    Extract ALL territory IDs from text file - Python fallback
    Returns (territories, unique_territories, territory_counter)
    """
    territories = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line_num, line in enumerate(lines, 1):
        # Look for territory ID pattern
        territory_match = re.search(r'Terr Id:\s+([A-Z0-9\-]+)', line)
        if territory_match:
            territory_id = territory_match.group(1)
            territories.append({
                'id': territory_id,
                'line': line_num,
                'text': line.strip()
            })
    
    # Count occurrences of each territory
    territory_ids = [t['id'] for t in territories]
    territory_counter = Counter(territory_ids)
    unique_territories = list(territory_counter.keys())
    
    return territories, unique_territories, territory_counter

def parse_complete_file_python(file_path):
    """
    Parse complete text file without territory filtering - Python fallback
    Returns all products found in the file
    """
    all_products = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        # Skip header/footer lines
        skip_words = ["Territory Wise Sale", "Group:", "Terr Id:", "Code Brand Name", "Page", "Total :"]
        if any(word in line for word in skip_words):
            continue
        
        parts = line.split()
        if len(parts) < 3:
            continue
        
        code = parts[0]
        
        # Identify numerical values from the end of the line
        num_count = 0
        for part in reversed(parts):
            try:
                float(part)
                num_count += 1
            except ValueError:
                break
        
        if num_count >= 1:
            number_parts = parts[-num_count:]
            brand_name_parts = parts[1:-num_count]
            
            if not brand_name_parts:
                continue
            
            # Pad the number list if less than 7 numbers are found
            expected_num_values = 7
            if len(number_parts) < expected_num_values:
                padding_needed = expected_num_values - len(number_parts)
                number_parts += ['0'] * padding_needed
            elif len(number_parts) > expected_num_values:
                number_parts = number_parts[-expected_num_values:]
            
            if len(number_parts) != expected_num_values:
                continue
            
            try:
                # Parse the 7 numerical values
                numbers = [float(p) for p in number_parts]
                tgt_qty = int(numbers[0])
                sold_qty = int(numbers[1])
                int_qty = int(numbers[2])
                tgt_val = numbers[3]
                sold_val = numbers[4]
                int_val = numbers[5]
                total_val = numbers[6]
                
                # Verify and correct total value if needed
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
                
                product_entry = {
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
                all_products.append(product_entry)
                
            except (ValueError, IndexError):
                continue
    
    return all_products
