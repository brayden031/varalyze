# imports
import varalyze_cli
from shared_imports import *
#from Scripts import abuseIPDB_cli_tool
#from Scripts import whois_cli_tool
#from Scripts import ipquality_cli_tool
#from Scripts import iplocation_cli_tool

# function to decide which tool the user wishes to use
def ip_tools():
    print("\n►►► You have selected IP address tools ◄◄◄")
    print("Welcome to the ip address tools. These tools will retrieve a vast amount of useful details associated with an ip...")
    awaiting_valid_tool_choice = True
    while awaiting_valid_tool_choice:
            user_option = input("""\nChoose a tool from the options below: \n\n 1. AbuseIPDB \n 2. Whois \n 3. iplocation \n 4. ipquality \n\n 5. Return to home page \n 6. Exit program \n\nEnter the number of the tool you wish to select: """) 
            if user_option == '1':
                os.system('cls')
                #abuseIPDB_cli_tool.main()
                awaiting_valid_tool_choice = False
            elif user_option == '2':
                os.system('cls')
                #whois_cli_tool.main()
                awaiting_valid_tool_choice = False
            elif user_option == '3':
                os.system('cls')
                #iplocation_cli_tool.main()
                awaiting_valid_tool_choice = False
            elif user_option == '4':
                os.system('cls')
                #ipquality_cli_tool.main()
                awaiting_valid_tool_choice = False
            elif user_option == '5':
                os.system('cls')
                varalyze_cli.main()
            elif user_option == '6':
                varalyze_cli.exit_program()
            else:
                os.system('cls')
                print("\nError: Invalid choice. Please select from 1-6...\n")
    awaiting_valid_tool_choice = True