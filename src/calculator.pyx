# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: initializedcheck=False
# cython: nonecheck=False
# cython: cdivision=True

"""
IPL Sales Analyzer - Cython Optimized Calculator
High-performance calculations for sales data analysis
"""

# REMOVE THESE LINES - no numpy needed
# import numpy as np
# cimport numpy as cnp

def calculate_totals_cython(product_data):
    """
    Calculate totals for product data using Cython optimization
    """
    cdef:
        double total_tgt_qty = 0.0
        double total_sold_qty = 0.0
        double total_int_qty = 0.0
        double total_tgt_val = 0.0
        double total_sold_val = 0.0
        double total_int_val = 0.0
        double total_accounted_val = 0.0
        double total_accounted_qty = 0.0
        int i
        int data_len = len(product_data)
    
    for i in range(data_len):
        product = product_data[i]
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

def calculate_national_average_cython(double total_accounted_val, double target_share):
    """
    Calculate national average using Cython optimization
    """
    cdef double national_avg_rounded = 0.0
    
    if total_accounted_val > 0 and target_share > 0:
        national_avg_raw = (total_accounted_val / target_share) / 100000
        national_avg_rounded = round(national_avg_raw, 2)
    
    return national_avg_rounded

def filter_products_by_activity_cython(product_data):
    """
    Filter products based on activity using Cython optimization
    Returns two lists: active_products, inactive_products
    """
    cdef:
        list active_products = []
        list inactive_products = []
        int i
        int data_len = len(product_data)
        bint has_activity
    
    for i in range(data_len):
        product = product_data[i]
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

def search_products_cython(product_data, str search_query):
    """
    Search products by brand name using Cython optimization
    """
    cdef:
        list matching_products = []
        list zero_matches = []
        int i
        int data_len = len(product_data)
        str brand_name_lower
        str query_lower = search_query.lower()
        bint has_activity
    
    for i in range(data_len):
        product = product_data[i]
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

def verify_data_consistency_cython(product_data):
    """
    Verify data consistency and correct any mismatches using Cython
    Returns corrected product data
    """
    cdef:
        list corrected_data = []
        int i
        int data_len = len(product_data)
        double calculated_total
        double total_val
    
    for i in range(data_len):
        product = product_data[i].copy()
        total_val = product['total_val']
        calculated_total = product['sold_val'] + product['int_val']
        
        # Fix data inconsistency if found
        if abs(total_val - calculated_total) > 0.01:
            product['total_val'] = calculated_total
        
        corrected_data.append(product)
    
    return corrected_data
