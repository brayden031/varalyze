# imports
import varalyze_cli
from shared_imports import *
#from Scripts import urlscan_cli_tool
#from Scripts import virustotal_cli_tool
#from Scripts import whois_domain_cli_tool

# function to decide which tool the user wishes to use
def domain_tools():
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                             Domain / URL tools                             ║
║                                                                            ║ 
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║          Welcome to the Domain & URL tools. These tools will retrieve      ║
║                useful details associated with an Domain/URL..              ║
║                                                                            ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║                                
║               ▼ Choose a tool from the list below to begin ▼               ║
║                                                                            ║
║        TOOLS                                                  OTHER        ║
║                                                                            ║
║        1. URLScan (Site behaviour, security insights)         4. Home page ║
║        2. VirusTotal (Malware detection, reputation analysis) 5. Exit      ║ 
║        3. WhoIS (Domain ownership, registration details)                   ║                  
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")
    awaiting_valid_tool_choice = True
    while awaiting_valid_tool_choice:
            user_option = input("Enter the number of the tool you wish to select: ") 
            if user_option == '1':
                os.system('cls')
                #urlscan_cli_tool.main()
                awaiting_valid_tool_choice = False
            elif user_option == '2':
                os.system('cls')
                #virustotal_cli_tool.main()
                awaiting_valid_tool_choice = False
            elif user_option == '3':
                os.system('cls')
                #whois_domain_cli_tool.main()
                awaiting_valid_tool_choice = False
            elif user_option == '4':
                os.system('cls')
                varalyze_cli.main()
                break
            elif user_option == '5':
                varalyze_cli.exit_program()
            else:
                print("\nError: Invalid choice. Please select from 1-5...\n")