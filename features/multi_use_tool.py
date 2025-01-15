# imports
from shared_imports import *
from scripts import abuseIPDB_cli_tool
from scripts import whois_cli_tool
from scripts import iplocation_cli_tool
from scripts import ipquality_cli_tool
from scripts import urlscan_cli_tool
from scripts import virustotal_cli_tool
from scripts import whois_domain_cli_tool
from tqdm import tqdm
import varalyze_cli

# Dictionary used to map user choice to script
ip_tools = {
            "1": abuseIPDB_cli_tool,
            "2": whois_cli_tool,
            "3": iplocation_cli_tool,
            "4": ipquality_cli_tool
        }

# Dictionary used to map user choice to script
url_tools = {
            "1": urlscan_cli_tool,
            "2": virustotal_cli_tool,
            "3": whois_domain_cli_tool,
        }
 
# Multi-use feature for passing an IP address             
def multi_ip():
    awaiting_valid_tool_choices = True
    while awaiting_valid_tool_choices:
        user_options = input("\nChoose the tools you would like to use from the options below (separate with commas): \n\n 1. AbuseIPDB \n 2. Whois \n 3. iplocation \n 4. ipquality\n\nAnswer: ")
        user_selections = [choice.strip() for choice in user_options.split(",")]
                
        # Checks user selection is valid before proceeding
        valid_selections = True
        for choice in user_selections:
            if choice not in ip_tools:
                os.system('cls')
                print("\nError: Invalid choice. Please select from 1-4...") 
                valid_selections = False
                
            # Prompts for IP address to pass to scripts if valid user choices
            if valid_selections:
                # User input that will be passed into the multi function within the scripts
                multi_ip_check = input("Enter an IP address: ")
                    
                for choice in user_selections:
                    try:
                        # Get the tool/module corresponding to the user's choice
                        module = ip_tools.get(choice)

                        if module:
                            # Call the multi function from the users choice of tools
                            module.multi(multi_ip_check)
                        # Error handling
                        else:
                            print(f"Error: Invalid choice {choice}. Please choose a valid number.")
                    except AttributeError as e:
                        print(f"Error: {e} - The selected tool doesn't have a 'multi' function.")
                    except Exception as e:
                        print(f"An error occurred: {e}")
                    
                # After feature has been used presents the user with the option to use again or exit this part of the program
                print("Would you like to use the multi-use feature again or return to the home page? \n\n1. Again \n2. Home\n")
                continue_choice = input("Answer: ")
                if continue_choice == '1':
                    os.system('cls')
                    main()
                elif continue_choice == '2':
                    varalyze_cli.main()
                else:
                    varalyze_cli.main()

# Multi-use feature for passing a URL
def multi_url():
    awaiting_valid_tool_choices = True
    while awaiting_valid_tool_choices:
        user_options = input("\nChoose the tools you would like to use from the options below (separate with commas): \n\n 1. URLScan \n 2. VirusTotal \n 3. Whois \n\nAnswer: ")
        user_selections = [choice.strip() for choice in user_options.split(",")]
   
        # Checks user selection is valid before proceeding
        valid_selections = True
        for choice in user_selections:
            if choice not in url_tools:
                os.system('cls')
                print("\nError: Invalid choice. Please select from 1-3...") 
                valid_selections = False
                
            # Prompts for IP address to pass to scripts if valid user choices
            if valid_selections:
                # User input that will be passed into the multi function within the scripts
                multi_url_check = input("Enter a domain/URL: ")
                    
                for choice in user_selections:
                    try:
                        # Get the tool/module corresponding to the user's choice
                        module = url_tools.get(choice)

                        if module:
                            # Call the multi function from the users choice of tools
                            module.multi(multi_url_check)
                        # Error handling
                        else:
                            print(f"Error: Invalid choice {choice}. Please choose a valid number.")
                    except AttributeError as e:
                        print(f"Error: {e} - The selected tool doesn't have a 'multi' function.")
                    except Exception as e:
                        print(f"An error occurred: {e}")
                    
                # After feature has been used presents the user with the option to use again or exit this part of the program
                print("Would you like to use the multi-use feature again or return to the home page? \n\n1. Again \n2. Home\n")
                continue_choice = input("Answer: ")
                if continue_choice == '1':
                    os.system('cls')
                    main()
                elif continue_choice == '2':
                    varalyze_cli.main()
                else:
                    varalyze_cli.main()

# Report generation feature for passing an IP address
# Requires seperate function as data is collected and analysed first, then outputted in report format rather than calling the results function of scripts                  
def multi_ip_report(multi_ip_check):
    results = {}
    # Progress bar using tqdm
    for key, module in tqdm(ip_tools.items(), desc="Processing tools "):
        if module: 
            tool_data = module.multi_data(multi_ip_check)
            if tool_data:
                results[key] = tool_data
    return results

# Report generation feature for passing a URL
# Requires seperate function as data is collected and analysed first, then outputted in report format rather than calling the results function of scripts        
def multi_url_report(multi_url_check):   
    results = {}
    for key, module in tqdm(url_tools.items(), desc="Processing tools "):
        if module: 
            tool_data = module.multi_data(multi_url_check)
            if tool_data:
                results[key] = tool_data
    return results
    
def main():
    print("\033[1m" + "\n►►►►►►►►► Welcome to the multi-use page ◄◄◄◄◄◄◄◄◄\n" + "\033[0m")
    print("""▼ Choose a category from the list below to begin your investigations ▼
1. IP Address
2. Domain / URL

3. Return to home page
4. Exit\n""")
    
    awaiting_valid_category = True
    while awaiting_valid_category:
        user_tool = input("Enter the number you wish to select: ")
        
        if user_tool == '1':
            multi_ip()
        elif user_tool == '2':
            multi_url()
        elif user_tool == '3':
            varalyze_cli.main()
        elif user_tool == '4':
            varalyze_cli.exit_program()
            return
        
        else:
            print("\nError: Invalid choice. Please select from 1-4...\n")
            
if __name__ == "__main__":
    main()