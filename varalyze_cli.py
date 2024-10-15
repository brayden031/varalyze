# varalyze
# CLI version of varalyze

# imports
from shared_imports import *

# page imports
from tool_options import ip
from tool_options import domain
from tool_options import file
from tool_options import mac
#from features import history_cli_tool

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
║         holistic view of the threat landscape this tool suite can offer.   ║
║                                                                            ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║                                
║           ▼ Choose a category from the list below to begin ▼               ║
║                                                                            ║
║        TOOL PAGES              FEATURES               OTHER                ║
║                                                                            ║
║        1. IP Address           5. History             8. API Key Check     ║
║        2. Domain & URL         6. Multi-use           9. API Key Config    ║
║        3. File & Hash          7. Generate Report     10. Exit             ║
║        4. MAC Address                                                      ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")
            awaiting_valid_choice = True
            while awaiting_valid_choice:
                user_tool = input("Enter the number you wish to select: ")
                if user_tool == '1':
                    os.system('cls')
                    ip.ip_tools()
                    awaiting_valid_choice = False
                elif user_tool == '2':
                    os.system('cls')
                    domain.domain_tools()
                    awaiting_valid_choice = False
                elif user_tool == '3':
                    os.system('cls')
                    file.file_tools()
                    awaiting_valid_choice = False
                elif user_tool == '4':
                    os.system('cls')
                    mac.mac_tools()
                    awaiting_valid_choice = False
                elif user_tool == '5':
                    os.system('cls')
                    #history_cli_tool.main()
                    awaiting_valid_choice = False
                elif user_tool == '10':
                    exit_program()
                else:
                    print("\nError: Invalid choice. Please select from 1-10...\n")               
            home_page = False
    
if __name__ == "__main__":
    main()