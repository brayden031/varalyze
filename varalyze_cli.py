# varalyze
# CLI version of varalyze

# imports
from shared_imports import *

# page imports
from tool_options import ip_tool
from tool_options import domain_tool
from tool_options import file_tool
from tool_options import mac_tool
from features import history_cli_tool
from features import multi_use_tool
from features import report_generation_tool
from features import case_workflow_tool
from config import api_key_check
from config import api_key_set

# function used anytime user wishes to exit the program
def exit_program():
    print("Exiting the program...")
    sys.exit()

# main function which is displayed on launch and acts as the home page
def main():
    home_page = True
    while home_page:
            os.system('cls')
            print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                                                                            ║
║       ██╗   ██╗ █████╗ ██████╗  █████╗ ██╗  ██╗   ██╗███████╗███████╗      ║
║       ██║   ██║██╔══██╗██╔══██╗██╔══██╗██║  ╚██╗ ██╔╝╚══███╔╝██╔════╝      ║
║       ██║   ██║███████║██████╔╝███████║██║   ╚████╔╝   ███╔╝ █████╗        ║
║       ╚██╗ ██╔╝██╔══██║██╔══██╗██╔══██║██║    ╚██╔╝   ███╔╝  ██╔══╝        ║
║        ╚████╔╝ ██║  ██║██║  ██║██║  ██║███████╗██║   ███████╗███████╗      ║
║         ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝   ╚══════╝╚══════╝      ║
║                                                                            ║
║                   Vᴇʀsɪᴏɴ: 1.0            Aᴜᴛʜᴏʀ: ʙʀᴀʏᴅᴇɴ031               ║  
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║           Welcome to the homepage of the Varalyze tool suite...            ║
║                                                                            ║
║         Varalyze is a threat intelligence tool suite that combines         ║
║         a diverse range of web-based applications into one seamless        ║
║         platform through the use of APIs and Python libraries. This        ║
║         allows for comprehensive security event triaging due to the        ║
║       holistic view of the threat landscape this tool suite can offer.     ║
║                                                                            ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║                                
║           ▼ Choose a category from the list below to begin ▼               ║
║                                                                            ║
║        TOOL PAGES              FEATURES               OTHER                ║
║                                                                            ║
║        1. IP Address           5. Multi-use             9.  API Key Check  ║
║        2. Domain & URL         6. Generate Report       10. API Key Config ║
║        3. File & Hash          7. History               11. Exit           ║
║        4. MAC Address          8. Case Workflow                            ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")
            awaiting_valid_choice = True
            while awaiting_valid_choice:
                user_tool = input("Enter the number you wish to select: ")
                if user_tool == '1':
                    os.system('cls')
                    ip_tool.ip_tools()
                    awaiting_valid_choice = False
                elif user_tool == '2':
                    os.system('cls')
                    domain_tool.domain_tools()
                    awaiting_valid_choice = False
                elif user_tool == '3':
                    os.system('cls')
                    file_tool.file_tools()
                    awaiting_valid_choice = False
                elif user_tool == '4':
                    os.system('cls')
                    mac_tool.mac_tools()
                    awaiting_valid_choice = False
                elif user_tool == '5':
                    os.system('cls')
                    multi_use_tool.main()
                    awaiting_valid_choice = False
                elif user_tool == '6':
                    os.system('cls')
                    report_generation_tool.main()
                    awaiting_valid_choice = False
                elif user_tool == '7':
                    os.system('cls')
                    history_cli_tool.main()
                    awaiting_valid_choice = False
                elif user_tool == '8':
                    os.system('cls')
                    case_workflow_tool.main()
                    awaiting_valid_choice = False
                elif user_tool == '9':
                    os.system('cls')
                    api_key_check.main()
                    awaiting_valid_choice = False
                elif user_tool == '10':
                    os.system('cls')
                    api_key_set.main()
                    awaiting_valid_choice = False
                elif user_tool == '11':
                    exit_program()
                else:
                    print("\nError: Invalid choice. Please select from 1-10...\n")               
            home_page = False
    
if __name__ == "__main__":
    main()