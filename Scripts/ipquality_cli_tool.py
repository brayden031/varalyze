#imports
from shared_imports import *
from tool_options import ip_tool
from features import history_cli_tool
import varalyze_cli

# ipquality API connection
def ipquality_connection(ip_address, IPQUALITY_API_KEY):
    url = f'https://www.ipqualityscore.com/api/json/ip/{IPQUALITY_API_KEY}/{ip_address}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error: Not successful response code to proceed - ", response.status_code)
    except requests.exceptions.RequestException as e:
        print("An error has occured attempting to make the request:", e)
        return None

# Formatting the results retrieved into the command line
def ip_results(ip_data, ip_address):
    if ip_data is None:
        print("No data found for this IP address you provided.")
    else:
        print("\n▼ IP Quality results ▼\n")
        table.field_names = ["Field", "Result"]
        table.add_row(["IP Quality score", Fore.GREEN + str(ip_data.get('fraud_score', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["ISP", Fore.GREEN + ip_data.get('ISP', 'Unknown') + Style.RESET_ALL])
        table.add_row(["VPN Connection", Fore.GREEN + str(ip_data.get('vpn', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["Active VPN connection", Fore.GREEN + str(ip_data.get('active_vpn', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["Tor Connection", Fore.GREEN + str(ip_data.get('tor', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["Proxy", Fore.GREEN + str(ip_data.get('proxy', 'Unknown')) + Style.RESET_ALL])
        table.max_width["Result"] = 80
        print(table)
        table.clear_rows()
        
        # Collating results
        result_log = {
            "IP Quality score": str(ip_data.get('fraud_score', 'Unknown')),
            "ISP": ip_data.get('ISP', 'Unknown'),
            "VPN Connection": str(ip_data.get('vpn', 'Unknown')),
            "Active VPN connection": str(ip_data.get('active_vpn', 'Unknown')),
            "Tor Connection": str(ip_data.get('tor', 'Unknown')),
            "Proxy": str(ip_data.get('proxy', 'Unknown')),
        }
        
        # Passing results into history feature
        history_cli_tool.record_search("IPQuality", ip_address, result_log)

def main():
    print("\033[1m" + "\n►►► Welcome to the ipquality CLI tool ◄◄◄\n" + "\033[0m")
    # Overall while loop for tool being run
    running_tool = True
    while running_tool:
        # Try to fetch API key environment variable, if fails displays error message but doesn't prevent program running
        try:
            IPQUALITY_API_KEY = os.environ["IPQUALITY_API_KEY"]
        except KeyError:
            os.system('cls')
            print("Error: IPQUALITY_API_KEY environment variable is not set.")
            print("Returning back to the tool page...")
            ip_tool.ip_tools()
        ip_address = input("Enter an IP address to check: ")
        ip_data = ipquality_connection(ip_address, IPQUALITY_API_KEY)
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