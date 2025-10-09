#!/usr/bin/env python3
"""
IPL Sales Analyzer - Pure Python Calculator Fallback
Python implementation of calculator functions when Cython is not available
"""

def calculate_totals_python(product_data):
    """
    Calculate totals for product data - Python fallback version
    """
    total_tgt_qty = 0.0
    total_sold_qty = 0.0
    total_int_qty = 0.0
    total_tgt_val = 0.0
    total_sold_val = 0.0
    total_int_val = 0.0
    total_accounted_val = 0.0
    
    for product in product_data:
        total_tgt_qty += product['tgt_qty']
        total_sold_qty += product['sold_qty']
        total_int_qty += product['int_qty']
        total_tgt_val += product['tgt_val']
        total_sold_val += product['sold_val']
        total_int_val += product['int_val']
        total_accounted_val += product['total_val']
    
    total_accounted_qty = total_sold_qty + total_int_qty
    
    # Verify and correct accounted value if needed
    calculated_accounted_val = total_sold_val + total_int_val
    if abs(total_accounted_val - calculated_accounted_val) > 0.01:
        total_accounted_val = calculated_accounted_val
    
    return {
        'total_tgt_qty': total_tgt_qty,
        'total_sold_qty': total_sold_qty,
        'total_int_qty': total_int_qty,
        'total_tgt_val': total_tgt_val,
        'total_sold_val': total_sold_val,
        'total_int_val': total_int_val,
        'total_accounted_val': total_accounted_val,
        'total_accounted_qty': total_accounted_qty
    }

def calculate_national_average_python(total_accounted_val, target_share):
    """
    Calculate national average - Python fallback version
    """
    national_avg_rounded = 0.0
    
    if total_accounted_val > 0 and target_share > 0:
        national_avg_raw = (total_accounted_val / target_share) / 100000
        national_avg_rounded = round(national_avg_raw, 2)
    
    return national_avg_rounded

def filter_products_by_activity_python(product_data):
    """
    Filter products based on activity - Python fallback version
    Returns two lists: active_products, inactive_products
    """
    active_products = []
    inactive_products = []
    
    for product in product_data:
        has_activity = (
            product['sold_qty'] > 0 or
            product['int_qty'] > 0 or
            product['sold_val'] > 0 or
            product['int_val'] > 0 or
            product['total_val'] > 0
        )
        
        if has_activity:
            active_products.append(product)
        else:
            inactive_products.append(product)
    
    return active_products, inactive_products

def search_products_python(product_data, search_query):
    """
    Search products by brand name - Python fallback version
    """
    matching_products = []
    zero_matches = []
    query_lower = search_query.lower()
    
    for product in product_data:
        brand_name_lower = product['brand_name'].lower()
        
        if query_lower in brand_name_lower:
            has_activity = (
                product['sold_qty'] > 0 or
                product['int_qty'] > 0 or
                product['sold_val'] > 0 or
                product['int_val'] > 0 or
                product['total_val'] > 0
            )
            
            if has_activity:
                matching_products.append(product)
            else:
                zero_matches.append(product)
    
    return matching_products, zero_matches

def verify_data_consistency_python(product_data):
    """
    Verify data consistency and correct any mismatches - Python fallback
    Returns corrected product data
    """
    corrected_data = []
    
    for product in product_data:
        corrected_product = product.copy()
        total_val = corrected_product['total_val']
        calculated_total = corrected_product['sold_val'] + corrected_product['int_val']
        
        # Fix data inconsistency if found
        if abs(total_val - calculated_total) > 0.01:
            corrected_product['total_val'] = calculated_total
        
        corrected_data.append(corrected_product)
    
    return corrected_data
