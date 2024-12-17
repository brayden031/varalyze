#imports
from shared_imports import *
from tool_options import file_tool
from features import history_cli_tool
import varalyze_cli

# VirusTotal API connection
def virustotal(file_path, VIRUSTOTAL_API_KEY):
    headers = {
        'x-apikey': VIRUSTOTAL_API_KEY
    }
    files = {
        'file':(file_path, open(file_path, 'rb'))
    }
    
    # v3 API URL
    submit_url = "https://www.virustotal.com/api/v3/files"
    
    # Connection attempt to the VirusTotal site
    try:
        web_page_response = requests.post(submit_url, headers=headers, files=files)
        web_page_response.raise_for_status()
        response_json = web_page_response.json()
        
        vt_analysis_id = response_json['data']['id']
        return vt_analysis_id
    
    # Throw request error if cannot successfully connect
    except requests.exceptions.RequestException as e:
        print("An error has occured attempting to make the request:", e)
        return None

# Function to attempt to retrieve completed scan   
def result_complete(vt_analysis_id, VIRUSTOTAL_API_KEY):
    headers = {
        'x-apikey': VIRUSTOTAL_API_KEY
    }
    
    id_url = f'https://www.virustotal.com/api/v3/analyses/{vt_analysis_id}'
    
    # Querying web page status
    while True:
        web_page_response = requests.get(id_url, headers=headers)
        if web_page_response.status_code == 200:
            analysis_status = web_page_response.json()['data']['attributes']['status']
            if analysis_status == 'completed':
                return web_page_response.json()
            else:
                print("VirusTotal is still proccessing the File, this can take a few seconds...")
                # Time delay whilst VirusTotal finishes processing
                time.sleep(30)
        else:
            print(f"VirusTotal encountered an error retrieving analysis results: {web_page_response.status_code}")
            print(web_page_response.text)
            return None

# Formatting the results retrieved into the command line    
def file_results(response_json, file_path):
    
    stats = response_json['data']['attributes']['stats']
    
    malicious = str(stats.get('malicious', 0))
    suspicious = str(stats.get('suspicious', 0))
    harmless = str(stats.get('harmless', 0))
    undetected = str(stats.get('undetected', 0))
    
    print("\n▼ VirusTotal results ▼\n ")
    table.field_names = ["Field", "Result"]
    table.add_row(["Total malicious", Fore.GREEN + malicious + Style.RESET_ALL])
    table.add_row(["Total suspicious", Fore.GREEN + suspicious + Style.RESET_ALL])
    table.add_row(["Total harmless", Fore.GREEN + harmless + Style.RESET_ALL])
    table.add_row(["Total undetected", Fore.GREEN + undetected + Style.RESET_ALL])
    table.max_width["Result"] = 80
    print(table)
    table.clear_rows()
    
    # Collating results
    result_log = {
    "Total malicious": malicious,
    "Total suspicious": suspicious,
    "Total harmless": harmless,
    "Total undetected": undetected
    }
     
    # Passing results into history feature   
    history_cli_tool.record_search("VirusTotal (file)", "File", file_path, result_log)
        
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
        print("No malicious or suspicious results found.")
                
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
            file_tool.File_tools()
        # File path error handling
        while True:
            file_path = input("Enter the file path of the file you wish to submit: ")
            if os.path.exists(file_path):
                break
            else:
                print("Error: File path", file_path, "not found!")
        vt_analysis_id = virustotal(file_path, VIRUSTOTAL_API_KEY)
        if vt_analysis_id:
            response_json = result_complete(vt_analysis_id, VIRUSTOTAL_API_KEY)
            if response_json:
                file_results(response_json, file_path)
        
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
                        file_tool.File_tools()
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