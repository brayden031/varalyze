#imports
from shared_imports import *
from tool_options import domain_tool
from features import history_cli_tool
from features import case_workflow_tool
from datetime import datetime
import varalyze_cli


# VirusTotal API connection
def virustotal(url, VIRUSTOTAL_API_KEY):
    headers = {
        "x-apikey": VIRUSTOTAL_API_KEY,
        "Accept": "application/json"
    }
    params = {
        "url": url
    }
    
    # v3 API URL
    submit_url = "https://www.virustotal.com/api/v3/urls"
    
    # Connection attempt to the VirusTotal site
    try:
        web_page_response = requests.post(submit_url, headers=headers, data=params)
        web_page_response.raise_for_status()
        response_json = web_page_response.json()
        
        vt_analysis_id = response_json['data']['id']
        return vt_analysis_id
    
    # Throw request error if cannot successfully connect
    except requests.exceptions.RequestException as e:
        print("An error has occured attempting to make the request:", e)
        return None

# Function to attempt to retrieve completed scan
def result_complete(VIRUSTOTAL_API_KEY, vt_analysis_id, output_print=True):
    headers = {
        "x-apikey": VIRUSTOTAL_API_KEY,
        "Accept": "application/json"
    }
    
    id_url = f"https://www.virustotal.com/api/v3/analyses/{vt_analysis_id}"
    
    # Querying web page status
    delay, poll_count = 5, 0
    while True:
        web_page_response = requests.get(id_url, headers=headers)
        web_page_response.raise_for_status()
        response_json = web_page_response.json()
        
        status = response_json['data']['attributes']['status']
    
        if status == 'completed':
            return response_json
        elif status in ['queued', 'in_progress']:
            poll_count += 1
            if output_print and poll_count % 3 == 0:
                print("VirusTotal is still processing the URL, please wait...")
            # Time delay before re-checking
            time.sleep(delay)
            delay = min(delay + 2, 20)
                   
# Formatting the results retrieved into the command line    
def url_results(response_json, url, prompt_for_comment=True, user_comment=""):
    
    stats = response_json['data']['attributes']['stats']
    malicious = stats.get('malicious', 0)
    suspicious = stats.get('suspicious', 0)
    harmless = str(stats.get('harmless', 0))
    undetected = str(stats.get('undetected', 0))
    
    malicious_color = Fore.RED if malicious > 5 else Fore.GREEN
    suspicious_color = Fore.YELLOW if suspicious > 2 else Fore.GREEN
    
    attributes = response_json['data']['attributes']
    analysis_timestamp = attributes.get('date')
    if analysis_timestamp:
        analysis_date = datetime.fromtimestamp(analysis_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    else:
        analysis_date = "N/A"
    
    print("\n▼ VirusTotal results ▼\n")
    table.field_names = ["Field", "Result"]
    table.align["Field"] = "l"
    table.add_row(["Total malicious", malicious_color + str(malicious) + Style.RESET_ALL])
    table.add_row(["Total suspicious", suspicious_color + str(suspicious) + Style.RESET_ALL])
    table.add_row(["Total harmless", Fore.GREEN + harmless + Style.RESET_ALL])
    table.add_row(["Total undetected", Fore.GREEN + undetected + Style.RESET_ALL])
    table.add_row(["Analysis Date", Fore.GREEN + analysis_date + Style.RESET_ALL])
    table.max_width["Result"] = 80 
    print(table)
    table.clear_rows()
    
    # Collating results
    result_log = {
        "Total malicious": malicious,
        "Total suspicious": suspicious,
        "Total harmless": harmless,
        "Total undetected": undetected,
        "Analysis Date": analysis_date
    }

    if case_workflow_tool.session_active:  
            case_workflow_tool.log_activity("\nVirusTotal domain results:\n")
            case_workflow_tool.log_activity(json.dumps(result_log, indent=4))
    
    flagged_results = response_json['data']['attributes']['results']
    
    # Secondary table that outputs if any vendors have flagged the domain/url as malicious or suspicious
    table_vendor = PrettyTable()
    table_vendor.field_names = ["Vendor", "Category", "Result"]
    reports_found = False
    print("\n▼ Vendors results for malicious/suspicious ▼\n")
    
    for scanner, result in flagged_results.items():
        category = result.get('category', 'unknown')
        result_label = result.get('result', 'No label')
        if category in ['malicious', 'suspicious']:
            table_vendor.add_row([Fore.RED + scanner + Style.RESET_ALL, Fore.RED + category + Style.RESET_ALL, Fore.RED + result_label + Style.RESET_ALL])
            table.max_width["Result"] = 80 
            reports_found = True
    if reports_found:
        print(table_vendor)
    else:
        print("No malicious or suspicious results found.\n")

    # Comment feature
    if prompt_for_comment:
            awaiting_comment = True
            while awaiting_comment:
                add_comment = input("\nWould you like to add a comment to this search? (enter y/n): ")
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
    history_cli_tool.record_search("VirusTotal", "URL", url, user_comment, result_log)

# Function used within the multi-use feature of program
def multi(multi_url_check, comment):
    try:
        VIRUSTOTAL_API_KEY = os.environ["VIRUSTOTAL_API_KEY"]
    except KeyError:
        print("Error: VIRUSTOTAL_API_KEY environment variable is not set.")
        print("Skipping this tool...")
        return
    ip_data = virustotal(multi_url_check, VIRUSTOTAL_API_KEY)
    if ip_data:
        response_json = result_complete(VIRUSTOTAL_API_KEY, ip_data, output_print=False)
        if response_json:
            url_results(response_json, multi_url_check, prompt_for_comment=False, user_comment=comment)
        return

# Function used within the report generation feature of program
def multi_data(multi_url_check):
    try:
        VIRUSTOTAL_API_KEY = os.environ["VIRUSTOTAL_API_KEY"]
    except KeyError:
        print("Error: VIRUSTOTAL_API_KEY environment variable is not set.")
        print("Skipping this tool...")
        return
    ip_data = virustotal(multi_url_check, VIRUSTOTAL_API_KEY)
    if ip_data:
        response_json = result_complete(VIRUSTOTAL_API_KEY, ip_data, output_print=False)
        if response_json:
            return response_json

def main():
    print("\033[1m" + "\n►►► Welcome to the VirusTotal CLI tool ◄◄◄\n" + "\033[0m")
    # Overall while loop for tool being run
    running_tool = True
    while running_tool:
        # Try to fetch API key environment variable, if fails displays error message but doesn't prevent program running
        try:
            VIRUSTOTAL_API_KEY = os.environ["VIRUSTOTAL_API_KEY"]
        except KeyError:
            os.system('cls')
            print("Error: VIRUSTOTAL_API_KEY environment variable is not set.")
            print("Returning back to the tool page...")
            domain_tool.domain_tools()
        url = input("Enter an url/domain to check: ")
        vt_analysis_id = virustotal(url, VIRUSTOTAL_API_KEY)
        if vt_analysis_id:
            response_json = result_complete(VIRUSTOTAL_API_KEY, vt_analysis_id)
            if response_json:
                url_results(response_json, url)
                
        # Second loop for determining if the user would like to check another
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
                        domain_tool.domain_tools()
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