IPL Sales Analyzer

Advanced sales data analyzer for IPL with territory detection and interactive search.

🚀 One-Click Installation

Copy this command and paste it in Termux:

```bash
pkg update -y && pkg upgrade -y && pkg install -y git python && git clone https://github.com/5C0R410N/IPL-Sales-Analyzer.git && cd IPL-Sales-Analyzer && chmod +x install.sh && python setup_directories.py && ./install.sh
```

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
4. 📄 Copy PDF sales file to this folder (mpo_sale_qty_value_SPECIAL_t.PDF)

🎯 How to Use the Analyzer

Starting the Program

```bash
report
```

First Time Setup

👤 Enter your name

🎯 Enter Target Share (Example: 0.33)

Daily Setup

🔄 Copy new sales PDF to SalesSource folder

📊 File: mpo_sale_qty_value_SPECIAL_t.PDF

📁 Replace old file or keep multiple versions

Selecting PDF File

Program shows available PDF files:

```
Found 3 PDF file(s):
  1. mpo_sale_qty_value_SPECIAL_t-23.PDF
  2. mpo_sale_qty_value_SPECIAL_t(1).PDF
  3. mpo_sale_qty_value_SPECIAL_t.PDF

Select PDF file (1-3): 1
✅ Selected: mpo_sale_qty_value_SPECIAL_t-23.PDF
```

Setting Page Range

```
Enter page range (e.g., 110-118) or press Enter for default (339-345):
```

📖 Enter Territory Page number from report bottom

⏎ Press Enter for default range: 339-345

🔄 Program processes data automatically

Searching Products

🔍 Type product names to find sales data

❌ Type "quit" to exit program

📱 Close Termux: notification panel → "Exit"

🔄 Important Notes

🎯 Steps 1-6: FIRST TIME INSTALLATION ONLY

📅 Daily: Copy new sales file → Run "report"

⚡ One-time setup required

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

(The End)

---

Repository: https://github.com/5C0R410N/IPL-Sales-Analyzer
