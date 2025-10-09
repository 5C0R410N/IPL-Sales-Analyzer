# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: nonecheck=False
# cython: cdivision=True

"""
IPL Sales Analyzer - Cython Optimized Parser
High-performance PDF text parsing and data extraction
"""

import re
from collections import Counter

def parse_layout_text_for_territory_cython(str file_path, str selected_territory):
    """
    Parse layout text file for specific territory using Cython optimization
    Returns (filtered_products, zero_value_products)
    """
    cdef:
        list lines = []
        list territory_products = []
        list filtered_products = []
        list zero_value_products = []
        str line
        str current_territory = None
        bint in_correct_territory = False
        dict product_entry
        int i
    
    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # First pass: Find territory boundaries and collect products
    for i in range(len(lines)):
        line = lines[i]
        
        # Check if this line starts a new territory section
        territory_match = re.search(r'Terr Id:\s+([A-Z0-9\-]+)', line)
        if territory_match:
            current_territory = territory_match.group(1)
            in_correct_territory = (current_territory == selected_territory)
        
        # Only process product lines if we're in the correct territory
        if in_correct_territory:
            # Skip header/footer lines
            skip_words = ["Territory Wise Sale", "Group:", "Terr Id:", "Code Brand Name", "Page", "Total :"]
            skip_line = False
            for word in skip_words:
                if word in line:
                    skip_line = True
                    break
            
            if skip_line:
                continue
            
            parts = line.split()
            if len(parts) < 3:
                continue
            
            code = parts[0]
            
            # Identify numerical values from the end of the line
            num_count = 0
            for j in range(len(parts) - 1, 0, -1):
                try:
                    float(parts[j])
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
    for i in range(len(territory_products)):
        product = territory_products[i]
        
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

def get_all_territory_ids_cython(str file_path):
    """
    Extract ALL territory IDs from text file with Cython optimization
    Returns (territories, unique_territories, territory_counter)
    """
    cdef:
        list territories = []
        list lines = []
        str line
        str territory_id
        object territory_match
        int line_num
        dict territory_counter
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line_num in range(len(lines)):
        line = lines[line_num]
        
        # Look for territory ID pattern
        territory_match = re.search(r'Terr Id:\s+([A-Z0-9\-]+)', line)
        if territory_match:
            territory_id = territory_match.group(1)
            territories.append({
                'id': territory_id,
                'line': line_num + 1,
                'text': line.strip()
            })
    
    # Count occurrences of each territory
    territory_ids = [t['id'] for t in territories]
    territory_counter = Counter(territory_ids)
    unique_territories = list(territory_counter.keys())
    
    return territories, unique_territories, territory_counter

def parse_complete_file_cython(str file_path):
    """
    Parse complete text file without territory filtering using Cython
    Returns all products found in the file
    """
    cdef:
        list lines = []
        list all_products = []
        str line
        dict product_entry
        int i
        int j
        int num_count
        list number_parts
        list brand_name_parts
        list numbers
        double calculated_total
        bint has_activity
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i in range(len(lines)):
        line = lines[i]
        
        # Skip header/footer lines
        skip_words = ["Territory Wise Sale", "Group:", "Terr Id:", "Code Brand Name", "Page", "Total :"]
        skip_line = False
        for word in skip_words:
            if word in line:
                skip_line = True
                break
        
        if skip_line:
            continue
        
        parts = line.split()
        if len(parts) < 3:
            continue
        
        code = parts[0]
        
        # Identify numerical values from the end of the line
        num_count = 0
        for j in range(len(parts) - 1, 0, -1):
            try:
                float(parts[j])
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
