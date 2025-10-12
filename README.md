IPL Sales Analyzer

Advanced sales data analyzer for IPL with automatic PDF import, territory detection, and interactive search.

🚀 One-Click Installation

Copy this command and paste it in Termux:

```bash
pkg update -y && pkg upgrade -y && pkg install -y git python && git clone https://github.com/5C0R410N/IPL-Sales-Analyzer.git && cd IPL-Sales-Analyzer && chmod +x install.sh && python setup_directories.py && ./install.sh
```

🆕 What's New in Latest Version

✨ Auto PDF Import Feature

· 🔍 Smart Scanning: Automatically finds PDF files in Download folders.

· 📁 Recursive Search: Searches through all subdirectories (WhatsApp, Telegram, etc.)

· ⚡ Duplicate Prevention: MD5 hash-based system prevents processing same files multiple times

· 📊 Size Filtering: Only imports PDFs in 5-6MB range (typical sales report size)

· 🔄 Automatic Organization: Moves PDFs to SalesSource folder automatically


📱 Complete Setup Guide

Step 1: Install Termux from F-Droid

📥 Download Termux from: https://f-droid.org/packages/com.termux/

💡 Suggested version: 0.118.3 (1002)

⚠️ Not mandatory to download this specific version

Step 2: Install Termux App

📁 Find Termux app in Internal Storage → Download/Downloads folder

🛡️ Ignore Google Security alerts during installation

✅ Continue installation process

Step 3: Verify Termux Authenticity

🔍 Termux is legitimate open-source project

🌐 Verify here: https://github.com/termux

⚠️ If security concerns, this tool not for you

Step 4: Run Installation Command

1. 📱 Open Termux app (needs 10-20MB data)
2. 📋 Paste one-click installation command
3. ⏳ Wait for automatic installation

Step 5: Grant Permissions

✅ Allow file access permission

👆 Tap "Allow" or type "Y"

⏳ Wait for installation complete

Step 6: Setup File Structure

1. ❌ Type "exit" to close Termux
2. 📁 Open File Manager
3. 📂 Find "SalesSource" folder in Internal Memory
4. 📄 OPTIONAL: Copy PDF sales file to this folder (mpo_sale_qty_value_SPECIAL_t.PDF)

🎯 How to Use the Analyzer

Starting the Program

```bash
report
```

OR use any case variation:

```bash
Report
REPORT
```

First Time Setup

👤 Enter your name

🎯 Enter Target Share (Example: 0.33)

🆕 Automated Daily Workflow

Option 1: Auto-Import (RECOMMENDED)

1. 📧 Receive sales PDF via Email/WhatsApp/Telegram
2. 📥 Open with Google Drive and download
3. 🚀 Run report command
4. ✅ Script automatically finds, verifies, and imports the PDF
5. 📊 Continue with analysis

Option 2: Manual Method

1. 📄 Copy new sales PDF to SalesSource folder
2. 📊 File: mpo_sale_qty_value_SPECIAL_t.PDF
3. 📁 Replace old file or keep multiple versions
4. 🚀 Run report command

Auto-Import Process

When you run report, the script will:

```
🔍 Scanning Download folders for NEW PDF files (5-6MB)...
📊 Loaded X known PDF hashes from registry
🎯 Found NEW PDF: sales_report.pdf
   Size: 5.42 MB
   Location: /storage/emulated/0/Download/WhatsApp
   Hash: a1b2c3d4e5f6...
✅ Successfully MOVED to SalesSource: sales_report.pdf
```

Selecting PDF File

Program shows available PDF files in SalesSource:

```
📁 Checking SalesSource directory...
📄 Found 3 PDF file(s):
  1. mpo_sale_qty_value_SPECIAL_t-23.PDF
     Modified: 15-01-24 (02:30 PM)
  2. mpo_sale_qty_value_SPECIAL_t(1).PDF
     Modified: 14-01-24 (11:15 AM)
  3. mpo_sale_qty_value_SPECIAL_t.PDF
     Modified: 13-01-24 (09:45 AM)

Select PDF file (1-3): 1
✅ Selected: mpo_sale_qty_value_SPECIAL_t-23.PDF
📅 Modified: 15-01-24 (02:30 PM)
```

Setting Page Range

```
Enter page range (e.g., 110-118) or press Enter for default (339-345):
```

📖 Enter Territory Page number from report bottom

⏎ Press Enter for default range: 339-345

🔄 Program processes data automatically

Searching Products

🔍 Type product names to find sales data (e.g., 'montair', 'moxquin')

❌ Type "quit" to exit program and generate report

📱 Close Termux: notification panel → "Exit"

🛠️ Technical Features

🔧 Advanced PDF Processing

· Automatic territory detection from PDF content
· Smart data parsing with error correction
· Fast calculations using optimized Python/Cython
· Duplicate prevention with MD5 hash registry

📊 Analysis Capabilities

· Product-wise sales data extraction
· National average calculation with target share
· Interactive search with real-time results
· Comprehensive reporting with timestamps

🔒 Smart File Management

· Hash-based duplicate detection prevents reprocessing
· Automatic file organization from Downloads to SalesSource
· Size filtering (5-6MB) ensures correct file type
· Recursive scanning finds files in any subdirectory

🔄 Important Notes

🎯 Steps 1-6: FIRST TIME INSTALLATION ONLY

📅 Daily: Download PDF → Run report → Auto-import → Analyze

⚡ One-time setup required

💾 Hash Registry: The system remembers processed files to avoid duplicates

🤝 Credits & Acknowledgments

This project is open source. You can check, use, distribute and modify as you want. I request you to give credit as well - removing credit doesn't make you shiner.

Special thanks to great Artificial Intelligence Language Models:

🤖 Qwen: https://github.com/QwenLM/Qwen

🧠 DeepSeek: https://github.com/deepseek-ai/DeepSeek-Coder

🙏 Personal Note

Thanks to Almighty Allah Subhanahu Wa Ta'ala that I completed this project. It took about 167+ hours over 12 days to complete.

Special thanks to Mr. Bulbul Ahmed, Senior MPO of Aster Team, Port - Halishahar Region, Chittagong (Incepta Pharmaceuticals Limited). His inspiration and curiosity motivated me to create this.

Finally, I'm sorry to you 'Tasnia Tasnim' - without giving you proper time, I worked on this project. Please accept my apology.

Love You "Priyotoma Tasnim"

---

Repository: https://github.com/5C0R410N/IPL-Sales-Analyzer

Latest Feature: Auto PDF Import with Smart Duplicate Prevention 🚀

(The End)
