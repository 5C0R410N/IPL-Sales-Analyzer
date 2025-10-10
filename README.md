```txt
# IPL Sales Analyzer

Advanced sales data analyzer for IPL with territory detection and interactive search.

## 🚀 One-Click Installation

**Copy this command and paste it in Termux:**

```bash
pkg update -y && pkg upgrade -y && pkg install -y git python && git clone https://github.com/5C0R410N/IPL-Sales-Analyzer.git && cd IPL-Sales-Analyzer && chmod +x install.sh && python setup_directories.py && ./install.sh
```

📱 Complete Setup Guide

Step 1: Install Termux from F-Droid

· Download Termux directly from: https://f-droid.org/packages/com.termux/
· Suggested version: 0.118.3 (1002) (You will see "suggested/recommended" version beside the name)
· Not mandatory to download this specific version

Step 2: Install Termux App

· After download, find the Termux app in your Internal Storage at "Download" or "Downloads" folder (varies by device)
· During installation, you may see Google Security alerts about "outdated package" or "unknown source installation"
· Just ignore these warnings and continue the installation process

Step 3: Verify Termux Authenticity

· Termux is a legitimate open-source project
· You can verify it here: https://github.com/termux
· If you have doubts about installing "virus or malware", this tool is not for you

Step 4: Run Installation Command

1. Open Termux app (needs 10-20MB data for first run)
2. Copy and paste the one-click installation command above
3. The script will automatically install everything needed

Step 5: Grant Permissions

· Termux will ask for permission to manage file access
· Tap "Allow" or sometimes type "Y" to continue
· Wait for installation to complete

Step 6: Setup File Structure

1. After installation completes, type "exit" on terminal to close Termux
2. Open your phone's File Manager
3. You will see a new folder named "SalesSource" in your Internal Memory (Phone storage)
4. Copy or move your PDF sales file to this folder (Example: mpo_sale_qty_value_SPECIAL_t.PDF)

🎯 How to Use the Analyzer

Starting the Program

· Open Termux and type "report" (the program will start)
· For first time setup, program will ask for your name - input that
· Then it will ask for your Target Share (Example: 0.33) - input this for future uses

Selecting PDF File

· Program will show list of PDF files in the directory:

```
Found 3 PDF file(s):
   1. mpo_sale_qty_value_SPECIAL_t-23.PDF
      Modified: 10-10-25 (04:08 AM)
   2. mpo_sale_qty_value_SPECIAL_t(1).PDF
      Modified: 07-10-25 (05:04 PM)
   3. mpo_sale_qty_value_SPECIAL_t.PDF
      Modified: 07-10-25 (02:10 AM)

Select PDF file (1-3): 1
✅ Selected: mpo_sale_qty_value_SPECIAL_t-23.PDF
📅 Modified: 10-10-25 (04:08 AM)
```

Setting Page Range

```
Enter page range (e.g., 110-118) or press Enter for default (339-345): 
```

(Enter your Territory Page number, found at the bottom of Sales Report)

· Press Enter to use default range: 339-345
· Program will process the data automatically

Searching Products

· Type product names correctly to find sales data
· To quit or close the program, simply type "quit" at the search prompt
· To close Termux completely: pull down notification panel and click "Exit"

🔄 Important Notes

· Steps 1-6 are for FIRST TIME INSTALLATION only
· After setup, you only need to use "report" command daily
· This is one-time setup work

🤝 Credits & Acknowledgments

This project is open source. You can check, use, distribute and modify as you want. I request you to give credit as well - removing credit doesn't make you shiner.

Special thanks to great Artificial Intelligence Language Models:

· Qwen: https://github.com/QwenLM/Qwen
· DeepSeek: https://github.com/deepseek-ai/DeepSeek-Coder

🙏 Personal Note

Thanks to Almighty Allah Subhanahu Wa Ta'ala that I completed this project. It took about 167+ hours over 12 days to complete.

Special thanks to Mr. Bulbul Ahmed, Senior MPO of Aster Team, Port - Halishahar Region, Chittagong (Incepta Pharmaceuticals Limited). His inspiration and curiosity motivated me to create this.

Finally, I'm sorry to you 'Tasnia Tasnim' - without giving you proper time, I worked on this project. Please accept my apology.

Love You "Priyotoma Tasnim"

(The End)

---

Repository: https://github.com/5C0R410N/IPL-Sales-Analyzer

```
