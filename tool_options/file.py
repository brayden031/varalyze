# imports
import varalyze_cli
from shared_imports import *
#from Scripts import virustotal_file_cli_tool

# function to decide which tool the user wishes to use
def File_tools():
        print("\n►►► You have selected File/Hash tools ◄◄◄")
        print("Welcome to the file & hash tools. This tools can analyse files to help determine whether they are safe or malware...")
        awaiting_valid_tool_choice = True
        while awaiting_valid_tool_choice:
            user_option = input("""\n 1. VirusTotal \n\n 2. Return to home page \n 3. Exit \n\nEnter the number you wish to select: """) 
            if user_option == '1':
                os.system('cls')
                #virustotal_file_cli_tool.main()
                awaiting_valid_tool_choice = False
            elif user_option == '2':
                os.system('cls')
                varalyze_cli.main()
                break
            elif user_option == '3':
                varalyze_cli.exit_program()
            else:
                print("\nError: Invalid choice. Please select from 1-3...\n")