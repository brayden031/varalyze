#imports
from shared_imports import *
from tool_options import ip_tool
from features import history_cli_tool
import varalyze_cli

# AbuseIPDB API connection
def abuse_IPDB(ip_address, ABUSEIPDB_API_KEY):
    url= f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip_address}"
    headers = {
        "Key": ABUSEIPDB_API_KEY,
        "Accept": "application/json"
    }
    
    # Connection attempt to the AbuseIPDB site
    try:
        web_page_response = requests.get(url, headers=headers)
        web_page_response.raise_for_status()
        return web_page_response.json()
    # Throw request error if cannot successfully connect
    except requests.exceptions.RequestException as e:
        print("An error has occured attempting to make the request:", e)
        return None

# Formatting the results retrieved into the command line
def ip_results(ip_data, prompt_for_comment=True):
    if 'data' in ip_data:
        data = ip_data['data']
        user_comment = ""
        print("\n▼ AbuseIPDB results ▼\n")
        table.field_names = ["Field", "Result"]
        table.add_row(["IP Address you entered", Fore.GREEN + data.get('ipAddress', 'Unknown') + Style.RESET_ALL])
        table.add_row(["Total number of reports:", Fore.GREEN + str(data.get('totalReports', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["Last reported at", Fore.GREEN + str(data.get('lastReportedAt', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["Confidence of abuse", Fore.GREEN + str(data.get('abuseConfidenceScore', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["", ""])
        table.add_row(["ISP", Fore.GREEN + data.get('isp', 'Unknown') + Style.RESET_ALL])
        table.add_row(["Usage Type", Fore.GREEN + data.get('usageType', 'Unknown') + Style.RESET_ALL])
        table.add_row(["Hostname(s)", Fore.GREEN + ', '.join(data.get('hostnames', ['Unknown'])) + Style.RESET_ALL])
        table.add_row(["Domain", Fore.GREEN + str(data.get('domain', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["Country code", Fore.GREEN + str(data.get('countryCode', 'Unknown')) + Style.RESET_ALL])
        table.add_row(["Tor node", Fore.GREEN + str(data.get('isTor', 'Unknown')) + Style.RESET_ALL])
        table.max_width["Result"] = 80
        print(table)
        table.clear_rows()
        
        # Collating results
        result_log = {
            "IP Address you entered": data.get('ipAddress', 'Unknown') ,
            "Total number of reports:": str(data.get('totalReports', 'Unknown')) ,
            "Last reported at": data.get('lastReportedAt', 'Unknown') ,
            "Confidence of abuse": str(data.get('abuseConfidenceScore', 'Unknown')) ,
            "ISP": data.get('isp', 'Unknown') ,
            "Usage Type": data.get('usageType', 'Unknown') ,
            "Hostname(s)": ', '.join(data.get('hostnames', ['Unknown'])) ,
            "Domain": str(data.get('domain', 'Unknown')) ,
            "Country code": str(data.get('countryCode', 'Unknown')) ,
            "Tor node": str(data.get('isTor', 'Unknown')) 
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
        history_cli_tool.record_search("AbuseIPDB", "IP", data.get('ipAddress', 'Unknown'), user_comment, result_log)

# Allows user to report the ip address they submitted if they wish to
def reporting_ip(ip, category, comment, timestamp, ABUSEIPDB_API_KEY):
    url= f"https://api.abuseipdb.com/api/v2/report"
    headers = {
        "Key": ABUSEIPDB_API_KEY,
        "Accept": "application/json"
    }
    report_params = {
        'ip': ip,
        'categories': category,
        'comment': comment,
        'timestamp': timestamp
     }
  
    # Connection attempt to the AbuseIPDB site
    try:
        web_page_response = requests.post(url, headers=headers, json=report_params)
        web_page_response.raise_for_status()
        print("Successfully reported", ip)
        return web_page_response.json()
    # Throw request error if cannot successfully connect
    except requests.exceptions.RequestException as e:
        print("An error has occured attempting to make the request:", e)
        return None

def multi(multi_ip_check):
    try:
        ABUSEIPDB_API_KEY = os.environ["ABUSEIPDB_API_KEY"]
    except KeyError:
        print("Error: ABUSEIPDB_API_KEY environment variable is not set.")
        print("Skipping this tool...")
        return
    ip_data = abuse_IPDB(multi_ip_check, ABUSEIPDB_API_KEY)
    if ip_data:
        ip_results(ip_data, prompt_for_comment=False)
        return

def main():
    print("\033[1m" + "\n►►►►►►►►► Welcome to the AbuseIPDB CLI tool ◄◄◄◄◄◄◄◄◄\n" + "\033[0m")
    # Overall while loop for tool being run
    running_tool = True
    while running_tool:
        # Try to fetch API key environment variable, if fails displays error message but doesn't prevent program running
        try:
            ABUSEIPDB_API_KEY = os.environ["ABUSEIPDB_API_KEY"]
        except KeyError:
            os.system('cls')
            print("Error: ABUSEIPDB_API_KEY environment variable is not set.")
            print("Returning back to the tool page...")
            ip_tool.ip_tools()
        ip = input("Enter an IP address to check: ")
        ip_data = abuse_IPDB(ip, ABUSEIPDB_API_KEY)
        if ip_data:
            ip_results(ip_data)
            # First loop for determining whether user wishes to report the ip address
            invalid_report = True
            while invalid_report:
                report_ip = input("\nWould you like to report this IP address for malicious activity?\nEnter 'yes' or 'no'\n\nAnswer: ")
                if report_ip == "yes":
                    category = input("Enter the category: ")
                    comment = input("Enter a comment: ")
                    timestamp = input("Enter the timestamp (format ISO 8601 datetime): ")
                    reporting_ip(ip, category, comment, timestamp, ABUSEIPDB_API_KEY)
                    invalid_report = False        
                elif report_ip == "no":
                    
                    # Second loop for determining if the user would like to check another
                    invalid_re_run = True
                    while invalid_re_run:
                        re_run_tool = input("\nWould you like to check another IP?\nEnter 'yes' or 'no'\n\nAnswer: ")
                        if re_run_tool == 'yes':
                            invalid_report = False
                            invalid_re_run = False
                            running_tool = True
                    
                    # Exit loop to determine correct input and next user navigation
                        elif re_run_tool == "no":
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
                # Error statement for report IP selection
                else:
                    os.system('cls')
                    print("Invalid option, please try again")

if __name__ == "__main__":
    main()        