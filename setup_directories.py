#!/usr/bin/env python3
"""
IPL Sales Analyzer - Directory Setup
Creates necessary directories and sets up the environment
"""

import os
import sys
from pathlib import Path

def create_directories():
    """Create all necessary directories for the application"""
    
    directories = [
        "/storage/emulated/0/SalesSource",
        "/storage/emulated/0/Analytics_Reports",
        "data"
    ]
    
    print("Setting up IPL Sales Analyzer directories...")
    
    for directory in directories:
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"Created/verified: {directory}")
        except Exception as e:
            print(f"Error creating {directory}: {e}")
    
    # Create data files if they don't exist
    data_files = ["user_data.txt", "target_share.txt", "debug_log.txt"]
    for file in data_files:
        try:
            Path(file).touch(exist_ok=True)
        except:
            pass
    
    print("Directory setup completed!")

def setup_bashrc_alias():
    """Setup bashrc alias for easy command access - case insensitive"""
    
    bashrc_paths = [
        "/data/data/com.termux/files/usr/etc/bash.bashrc",
        os.path.expanduser("~/.bashrc"),
        os.path.expanduser("~/.bash_profile")
    ]
    
    current_dir = os.getcwd()
    
    # Create aliases for all case variations
    alias_commands = [
        '# IPL Sales Analyzer command aliases',
        f'alias report="cd {current_dir} && python src/ipl_analyzer.py"',
        f'alias Report="cd {current_dir} && python src/ipl_analyzer.py"', 
        f'alias REPORT="cd {current_dir} && python src/ipl_analyzer.py"'
    ]
    
    for bashrc in bashrc_paths:
        if os.path.exists(bashrc):
            try:
                with open(bashrc, 'r') as f:
                    content = f.read()
                
                # Check if any report alias already exists
                if not any(alias in content for alias in ['alias report=', 'alias Report=', 'alias REPORT=']):
                    with open(bashrc, 'a') as f:
                        f.write('\n' + '\n'.join(alias_commands) + '\n')
                    print(f"Command aliases added to {bashrc}")
                else:
                    print(f"Command aliases already exist in {bashrc}")
                    
            except Exception as e:
                print(f"Could not update {bashrc}: {e}")

if __name__ == "__main__":
    create_directories()
    setup_bashrc_alias()
    
    print("\nSetup completed!")
    print("Command 'report' is now available in these variations:")
    print("  - report")
    print("  - Report") 
    print("  - REPORT")
    print("\nYou can use any of these commands from anywhere in Termux")
    print("To apply immediately, run: source ~/.bashrc")
    print("\nRepository: https://github.com/5C0R410N/IPL-Sales-Analyzer")
