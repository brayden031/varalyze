#imports
from shared_imports import *
from tool_options import ip_tool
from features import history_cli_tool
from features import case_workflow_tool
import varalyze_cli
import whois

# Whois connection
def whois_query_results(query, prompt_for_comment=True, user_comment=""):
    try:
        query_results = whois.whois(query)
        print("\n▼ Whois results ▼\n")
        # Formatting the results retrieved into the command line
        table.field_names = ["Field", "Result"]
        table.add_row(["Domain name", Fore.GREEN + str(query_results.get('domain_name') or 'Unknown') + Style.RESET_ALL])
        table.add_row(["Registrar", Fore.GREEN + str(query_results.get('registrar', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["Creation date", Fore.GREEN + str(query_results.get('creation_date', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["Expiration date", Fore.GREEN + str(query_results.get('expiration_date', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["", ""])
        table.add_row(["Organisation", Fore.GREEN + str(query_results.get('org', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["Address", Fore.GREEN + str(query_results.get('address', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["City", Fore.GREEN + str(query_results.get('city', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["State", Fore.GREEN + str(query_results.get('state', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["Country", Fore.GREEN + str(query_results.get('country', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["Postal code", Fore.GREEN + str(query_results.get('postal_code', 'Unknown')) + Style.RESET_ALL])
        table.max_width["Result"] = 80
        print(table)
        table.clear_rows()
        
        # Collating results
        result_log = {
            "Domain name": str(query_results.get('domain_name') or 'Unknown'),
            "Registrar": str(query_results.get('registrar', 'Unknown')),
            "Creation date": str(query_results.get('creation_date', 'Unknown')),
            "Creation date": str(query_results.get('expiration_date', 'Unknown')),
            "Organisation": str(query_results.get('org', 'Unknown')),
            "Address": str(query_results.get('address', 'Unknown')),
            "City": str(query_results.get('city', 'Unknown')),
            "State": str(query_results.get('state', 'Unknown')),
            "Country": str(query_results.get('country', 'Unknown')),
            "Postal code": str(query_results.get('postal_code', 'Unknown'))
        }
        
        if case_workflow_tool.session_active:  
            case_workflow_tool.log_activity("\nWhois IP address results:\n")
            case_workflow_tool.log_activity(json.dumps(result_log, indent=4))
        
        # Comment feature
        if prompt_for_comment:
            awaiting_comment = True
            while awaiting_comment:
                add_comment = input("Would you like to add a comment to this search? (enter y/n): ")
                if add_comment == "y":
                    user_comment = input("Enter a comment (max 30 characters): ")
                    awaiting_comment = False
                    if len(user_comment) > 50:
                        user_comment = user_comment[:30]
                elif add_comment == "n":
                    user_comment = ""
                    awaiting_comment = False
                else:
                    print("Invalid option, please try again") 
        
        # Passing results into history feature 
        history_cli_tool.record_search("WhoIS", "IP", query, user_comment, result_log)
        
    except Exception as e:
        print("Error encountered", e)

# Function used within the multi-use feature of program
def multi(multi_ip_check, comment):
    ip_data = whois_query_results(multi_ip_check, prompt_for_comment=False, user_comment=comment)
    if ip_data:
        return

# Function used within the report generation feature of program
# Required an additional function as initial function handles both query and results together so needed to be split
def whois_query_report(multi_ip_check):
    try:
        query_results = whois.whois(multi_ip_check)
        return query_results
    except Exception as e:
        print("Error encountered", e)

# Function used within the report generation feature of program     
def multi_data(multi_ip_check):
    ip_data = whois_query_report(multi_ip_check)
    if ip_data:
        return ip_data

def main():
    print("\033[1m" + "\n►►► Welcome to the Whois CLI tool ◄◄◄\n" + "\033[0m")
    # Overall while loop for tool being run
    running_tool = True
    while running_tool:
            query_input = input("Enter an ip address: ")
            whois_query_results(query_input)
            
            # First loop for determining if the user would like to check another
            invalid_re_run = True
            while invalid_re_run:
                re_run_tool = input("\nWould you like to check another ?\nEnter 'yes' or 'no'\n\nAnswer: ")
                if re_run_tool == 'yes':
                    running_tool = True
                    invalid_re_run = False
                    
                # Exit loop to determine correct input and next user navigation
                elif re_run_tool == 'no':
                    running_tool = False
                    invalid_re_run = False
                    invalid_exit = True
                    while invalid_exit:
                        exit_tool = input("\nWould you like to return to the category page, home page or exit the program?\nEnter 'category' or 'home' 'exit'\n\nAnswer: ")
                        if exit_tool == "category":
                            invalid_exit = False
                            running_tool = False
                            os.system('cls')
                            ip_tool.ip_tools()
                        elif exit_tool == "home":
                            invalid_exit = False
                            running_tool = False
                            os.system('cls')
                            varalyze_cli.main()
                        elif exit_tool == "exit":
                            invalid_exit = False
                            running_tool = False
                            varalyze_cli.exit_program()
                        # Error statement for category selection
                        else:
                            os.system('cls')
                            print("Invalid option, please try again")
                    # Error statement for check again selection
                    else:
                        os.system('cls')
                        print("Invalid option, please try again")
                else:
                    os.system('cls')
                    print("Invalid option, please try again")
        
if __name__ == "__main__":
    main()