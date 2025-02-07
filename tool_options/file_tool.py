# imports
import varalyze_cli
from shared_imports import *
from scripts import virustotal_file_cli_tool
from features import advanced_file_tool

# function to decide which tool the user wishes to use
def file_tools():
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                               File / Hash tool                             ║
║                                                                            ║ 
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║         Welcome to the file & hash tool. This tools can analyse files      ║
║             to help determine whether they are safe or malware...          ║
║                                                                            ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║                                
║               ▼ Choose a tool from the list below to begin ▼               ║
║                                                                            ║
║       TOOLS                                                   OTHER        ║
║                                                                            ║
║       1. VirusTotal (Malware detection, multi-engine analyis) 3. Home page ║
║       2. Advanced file investigation                          4. Exit      ║                   
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")
    awaiting_valid_tool_choice = True
    while awaiting_valid_tool_choice:
        user_option = input("Enter the number you wish to select: ") 
        if user_option == '1':
            os.system('cls')
            virustotal_file_cli_tool.main()
            awaiting_valid_tool_choice = False
        if user_option == '2':
            print("\nNote: This tool is still under development and will be available in future releases.\n")
        elif user_option == '3':
            os.system('cls')
            varalyze_cli.main()
            break
        elif user_option == '4':
            varalyze_cli.exit_program()
        else:
            print("\nError: Invalid choice. Please select from 1-4...\n")