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
    
    # PHONE STORAGE directories - CRITICAL for the app to work
    phone_directories = [
        "/storage/emulated/0/SalesSource",
        "/storage/emulated/0/Analytics_Reports"
    ]
    
    # LOCAL directories in project folder
    local_directories = [
        "data"
    ]
    
    print("Setting up IPL Sales Analyzer directories...")
    
    # Create phone storage directories (MOST IMPORTANT)
    for directory in phone_directories:
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"✅ Created/verified: {directory}")
        except Exception as e:
            print(f"❌ Error creating {directory}: {e}")
            print(f"   This may cause the app to fail! Please check storage permissions.")
    
    # Create local project directories
    for directory in local_directories:
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"✅ Created/verified: {directory}")
        except Exception as e:
            print(f"⚠️  Warning creating {directory}: {e}")
    
    # Create data files if they don't exist
    data_files = ["user_data.txt", "target_share.txt", "debug_log.txt"]
    for file in data_files:
        try:
            Path(file).touch(exist_ok=True)
            print(f"✅ Created/verified: {file}")
        except Exception as e:
            print(f"⚠️  Warning creating {file}: {e}")
    
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
    
    alias_added = False
    
    for bashrc in bashrc_paths:
        if os.path.exists(bashrc):
            try:
                with open(bashrc, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if any report alias already exists
                if not any(alias in content for alias in ['alias report=', 'alias Report=', 'alias REPORT=']):
                    with open(bashrc, 'a', encoding='utf-8') as f:
                        f.write('\n' + '\n'.join(alias_commands) + '\n')
                    print(f"✅ Command aliases added to {bashrc}")
                    alias_added = True
                else:
                    print(f"✅ Command aliases already exist in {bashrc}")
                    alias_added = True
                    
            except Exception as e:
                print(f"❌ Could not update {bashrc}: {e}")
    
    return alias_added

if __name__ == "__main__":
    create_directories()
    alias_success = setup_bashrc_alias()
    
    print("\n" + "="*50)
    print("✅ SETUP COMPLETED!")
    print("="*50)
    
    print("\n📁 DIRECTORY STATUS:")
    print("   ✅ /storage/emulated/0/SalesSource/ - For PDF files")
    print("   ✅ /storage/emulated/0/Analytics_Reports/ - For generated reports")
    print("   ✅ data/ - For local configuration")
    
    if alias_success:
        print("\n💻 COMMAND ALIASES:")
        print("   ✅ report   - Available from anywhere in Termux")
        print("   ✅ Report   - Same as 'report'")
        print("   ✅ REPORT   - Same as 'report'")
        print("\n📍 To apply immediately, run: source ~/.bashrc")
    else:
        print("\n❌ Command aliases could not be set up automatically")
        print("   You can manually run: python src/ipl_analyzer.py")
    
    print("\n🔗 Repository: https://github.com/5C0R410N/IPL-Sales-Analyzer")
