# imports
import varalyze_cli
from shared_imports import *
from scripts import macvendors_cli_tool

# function to decide which tool the user wishes to use
def mac_tools():
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                               MAC address tool                             ║
║                                                                            ║ 
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║         Welcome to the MAC address tool. This tool will retrieve a         ║
║                   vendor for an associated MAC address...                  ║
║                                                                            ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║                                
║               ▼ Choose a tool from the list below to begin ▼               ║
║                                                                            ║
║          TOOL                                                 OTHER        ║
║                                                                            ║
║   1. MAC Vendors (Manufacturer lookup, device identification) 2. Home page ║
║                                                               3. Exit      ║                   
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")
    awaiting_valid_tool_choice = True
    while awaiting_valid_tool_choice:
        user_option = input("Enter the number you wish to select: ") 
        if user_option == '1':
            os.system('cls')
            macvendors_cli_tool.main()
            awaiting_valid_tool_choice = False
        elif user_option == '2':
            os.system('cls')
            varalyze_cli.main()
            break
        elif user_option == '3':
            varalyze_cli.exit_program()
        else:
            print("\nError: Invalid choice. Please select from 1-3...\n")