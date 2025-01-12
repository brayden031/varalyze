#imports
from shared_imports import *
from tool_options import domain_tool
from features import history_cli_tool
import varalyze_cli

# URLScan API connection
def urlscan(url, URLSCAN_API_KEY, output_print=True):
    headers = {
        'API-Key': URLSCAN_API_KEY,
        'Content-Type': 'application/json',
    }
    data = {
        'url': url,
        'visibility': 'public'
    }
    
    submit_url = "https://urlscan.io/api/v1/scan/"
    
    # Connection attempt to the URLScan site
    try:
        web_page_response = requests.post(submit_url, json=data, headers=headers)
        web_page_response.raise_for_status()
        response_json = web_page_response.json()
        uuid = response_json.get('uuid')
        if uuid:
            scan_url = f"https://urlscan.io/result/{uuid}/"
            if output_print:
                print("")
                print(f"URLScan has started proccessing the URL, this can take a few seconds...")
                # Outputs scan result URL
                print(f"Full scan details can be found at ►►► {scan_url} ◄◄◄") 
        else:
            print("Failed to get a UUID from the scan submission.")
        return uuid
    # Throw request error if cannot successfully connect
    except requests.exceptions.RequestException as e:
        print("An error has occured attempting to make the request:", e)
        return None

# Function to attempt to retrieve completed scan
def result_complete(uuid, output_print=True):
    id_url = f"https://urlscan.io/api/v1/result/{uuid}/"
    if output_print:
        print("\nURLScan has queued the check, this can take a few seconds...")

    # Time delay whilst urlscan finishes processing
    time.sleep(20)
    while True:
        try:
            web_page_response = requests.get(id_url)
            if (web_page_response.status_code == 404 and output_print):
                print("URLScan is proccessing the URL, this can take a few seconds...")
                # Time delay before re-checking
                time.sleep(20)
                continue

            web_page_response.raise_for_status()
            response_json = web_page_response.json()
            return response_json
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the results: {e}")
            return None

# Formatting the results retrieved into the command line    
def url_results(response_json, url, prompt_for_comment=True):
    
    stats = response_json
    
    # Time related information
    time_info = stats.get('task', {}).get('time', {})
    submitted_at = time_info if isinstance(time_info, str) else time_info.get('submitted', 'N/A')
    completed_at = time_info if isinstance(time_info, str) else time_info.get('completed', 'N/A')
    
    # Web page hosting details
    title = stats.get('page', {}).get('title', 'N/A')
    url = stats.get('page', {}).get('url', 'N/A')
    ip = stats.get('page', {}).get('ip', 'N/A')
    server = stats.get('page', {}).get('server', 'N/A')
    country = stats.get('page', {}).get('country', 'N/A')
    
    # Vendors verdict
    malicious = 'Yes' if stats.get('verdicts', {}).get('overall', {}).get('malicious') else 'No'
    google_safebrowsing = 'Yes' if stats.get('verdicts', {}).get('engines', {}).get('google_safebrowsing') else 'No'
    phishing = 'Yes' if stats.get('verdicts', {}).get('engines', {}).get('phishing') else 'No'

    user_comment = ""
    print("\n▼ URLScan results ▼\n")
    table.field_names = ["Field", "Result"]
    table.add_row(["Submitted at", Fore.GREEN + submitted_at + Style.RESET_ALL])
    table.add_row(["Completed at", Fore.GREEN + completed_at + Style.RESET_ALL])
    table.add_row(["", ""])
    table.add_row(["Title", Fore.GREEN + title + Style.RESET_ALL])
    table.add_row(["URL", Fore.GREEN + url + Style.RESET_ALL])
    table.add_row(["Hosting IP", Fore.GREEN + ip + Style.RESET_ALL])
    table.add_row(["Server", Fore.GREEN + server + Style.RESET_ALL])
    table.add_row(["Country", Fore.GREEN + country + Style.RESET_ALL])
    table.add_row(["", ""])
    table.add_row(["Malicious", Fore.GREEN + malicious + Style.RESET_ALL])
    table.add_row(["Google safebrowsing", Fore.GREEN + google_safebrowsing + Style.RESET_ALL])
    table.add_row(["Phishing", Fore.GREEN + phishing + Style.RESET_ALL])
    table.max_width["Result"] = 80
    print(table)
    table.clear_rows()
    
    # Collating results
    result_log = {
        "Submitted at": submitted_at,
        "Completed at": completed_at,
        "Title": title,
        "URL": url,
        "Hosting IP": ip,
        "Server": server,
        "Country": country,
        "Malicious": malicious,
        "Google safebrowsing": google_safebrowsing,
        "Phishing": phishing
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
    history_cli_tool.record_search("URL Scan", "URL", url, user_comment, result_log)

# Function used within the multi-use feature of program
def multi(multi_url_check):
    try:
        URLSCAN_API_KEY = os.environ["URLSCAN_API_KEY"]
    except KeyError:
        print("Error: URLSCAN_API_KEY environment variable is not set.")
        print("Skipping this tool...")
        return
    ip_data = urlscan(multi_url_check, URLSCAN_API_KEY, output_print=False)
    if ip_data:
        response_json = result_complete(ip_data, output_print=False)
        if response_json:
            url_results(response_json, multi_url_check, prompt_for_comment=False)
        return

# Function used within the report generation feature of program
def multi_data(multi_url_check):
    try:
        URLSCAN_API_KEY = os.environ["URLSCAN_API_KEY"]
    except KeyError:
        print("Error: URLSCAN_API_KEY environment variable is not set.")
        print("Skipping this tool...")
        return
    ip_data = urlscan(multi_url_check, URLSCAN_API_KEY, output_print=False)
    if ip_data:
        response_json = result_complete(ip_data, output_print=False)
        if response_json:
            return response_json
    

def main():
    print("\033[1m" + "\n►►► Welcome to the URLScan CLI tool ◄◄◄\n" + "\033[0m")
    # Overall while loop for tool being run
    running_tool = True
    while running_tool:
        # Try to fetch API key environment variable, if fails displays error message but doesn't prevent program running
        try:
            URLSCAN_API_KEY = os.environ["URLSCAN_API_KEY"]
        except KeyError:
            os.system('cls')
            print("Error: URLSCAN_API_KEY environment variable is not set.")
            print("Returning back to the tool page...")
            domain_tool.domain_tools()
        url = input("Enter an url/domain to check: ")
        uuid = urlscan(url, URLSCAN_API_KEY)
        if uuid:
            response_json = result_complete(uuid)
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