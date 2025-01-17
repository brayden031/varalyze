#imports
from shared_imports import *
from tool_options import ip_tool
from features import history_cli_tool
import varalyze_cli

# iplocation API connection
def iplocation_connection(ip_address):
    url = f'https://api.iplocation.net/?ip={ip_address}'
    try:
        # Connection produces 200 even on invalid entries but this still determines that overall site is available for requests
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error: Not successful response code to proceed - ", response.status_code)
    except requests.exceptions.RequestException as e:
        print("An error has occured attempting to make the request:", e)
        return None

# Formatting the results retrieved into the command line
def ip_results(ip_data, ip_address, prompt_for_comment=True, user_comment=""):
    if ip_data is None:
        print("No data found for this IP address you provided.")
    else:
        print("\n▼ IP Location results ▼\n")
        table.field_names = ["Field", "Result"]
        table.add_row(["ISP", Fore.GREEN + ip_data.get('isp', 'Unknown') + Style.RESET_ALL])
        table.add_row(["Country", Fore.GREEN + ip_data.get('country_name', 'Unknown') + Style.RESET_ALL])
        table.add_row(["Country code", Fore.GREEN + str(ip_data.get('country_code2', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["IP version", Fore.GREEN + str(ip_data.get('ip_version', 'Unknown')) + Style.RESET_ALL])
        # Site will produce 200 status even on invalid entries so getting the response parameter shows if it was an actual valid query
        table.add_row(["Responde code", Fore.GREEN + str(ip_data.get('response_code', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["Response message", Fore.GREEN + str(ip_data.get('response_message', 'Unknown')) + Style.RESET_ALL])
        table.max_width["Result"] = 80 
        print(table)
        table.clear_rows()
        
        # Collating results
        result_log = {
            "ISP": ip_data.get('isp', 'Unknown'),
            "Country": ip_data.get('country_name', 'Unknown'),
            "Country code": str(ip_data.get('country_code2', 'Unknown')),
            "IP version": str(ip_data.get('ip_version', 'Unknown')),
            "Responde code": str(ip_data.get('response_code', 'Unknown')),
            "Response message": str(ip_data.get('response_message', 'Unknown')),
        }
        
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
        history_cli_tool.record_search("IPLocation", "IP", ip_address, user_comment, result_log)

# Function used within the multi-use feature of program
def multi(multi_ip_check, comment):
    ip_data = iplocation_connection(multi_ip_check)
    if ip_data:
        ip_results(ip_data, multi_ip_check, prompt_for_comment=False, user_comment=comment)
        return

# Function used within the report generation feature of program  
def multi_data(multi_ip_check):
    ip_data = iplocation_connection(multi_ip_check)
    if ip_data:
        return ip_data

def main():
    print("\033[1m" + "\n►►► Welcome to the iplocation CLI tool ◄◄◄\n" + "\033[0m")
    # Overall while loop for tool being run
    running_tool = True
    while running_tool:
        ip_address = input("Enter an IP address to check: ")
        ip_data = iplocation_connection(ip_address)
        ip_results(ip_data, ip_address)
        
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