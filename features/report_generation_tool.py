# imports
from tqdm import tqdm
from shared_imports import *
from features import multi_use_tool
import varalyze_cli

failed_tools = []

# Varalyze score calculation function to analyse data sources
def ip_score_calculation(tool_results):
    
    # Initiliasing variables
    varalyze_score = 0
    indicators = []
    failed_tools = []
    
    # Progress bar using tqdm
    with tqdm(total=100, desc="Processing score ") as progress_bar:
        
        # Accessing stored abuseIPDB data
        abuseIPDB_data = tool_results.get("1", {}).get("data", {})
        if abuseIPDB_data:
            confidence_score = abuseIPDB_data.get("abuseConfidenceScore", 0)
            total_reports = abuseIPDB_data.get("totalReports", 0)
            is_tor = abuseIPDB_data.get("isTor", False)

            # Scoring logic for AbuseIPDB data
            varalyze_score += confidence_score * 0.4
            if varalyze_score > 20:
                indicators.append(f"AbuseIPDB Confidence Score: {confidence_score}")
            if total_reports > 10:
                varalyze_score += 10
                indicators.append("Reported several times on AbuseIPDB (10+)")
            if is_tor:
                varalyze_score += 5
                indicators.append("Tied to the Tor network")
        # Dynamically updating progress bar
        for i in range(1, 31):
            progress_bar.update(1)
            time.sleep(0.04)

        # Accessing stored IPQuality data
        ipquality_data = tool_results.get("4", {})
        if ipquality_data:
            fraud_score = ipquality_data.get("fraud_score", 0)
            bot_status = ipquality_data.get("bot_status", False)
            
            proxy_active = ipquality_data.get("proxy", False)
            indicators.append("Using a proxy")
            
            vpn_active = ipquality_data.get("vpn", False)
            indicators.append("Part of VPN network")
            
            # Scoring logic for IPQuality
            varalyze_score += fraud_score * 0.3 
            if proxy_active:
                varalyze_score += 10
            if vpn_active:
                varalyze_score += 5
            if bot_status:
                varalyze_score += 10
                
        for i in range(1, 31):
            progress_bar.update(1)
            time.sleep(0.04)
            
        # Accessing stored IPLocation data
        iplocation_data = tool_results.get("3", {})
        ip_country_code = iplocation_data.get("country_code2", "")

        for i in range(1, 21):
            progress_bar.update(1)
            time.sleep(0.04)
                 
        # Accessing stored whoIS data
        whois_data = tool_results.get("2", {})
        whois_country_code = whois_data.get("country", "")

        # Scoring logic for whoIS
        if ip_country_code and whois_country_code and ip_country_code != whois_country_code:
            varalyze_score += 10
            indicators.append("Mismatch observed between IPLocation and whoIS")
        if whois_country_code in {"RU", "CN", "NK", "IR"}:
            varalyze_score += 10
            indicators.append("High risk country")
            
        for i in range(1, 21):
            progress_bar.update(1)
            time.sleep(0.04)
        
        # Restrict varalyze score (can exceed 100 incase of missing data so it still gives accurate scoring)
        varalyze_score = min(varalyze_score, 100)
        # Call report function to structure concatenated data
        return report_generation_ip(varalyze_score, indicators)

def url_score_calculation(tool_results):
    
    # Initiliasing variables
    varalyze_score = 0
    indicators = []
    failed_tools = []
    
    # Progress bar using tqdm
    with tqdm(total=100, desc="Processing score ") as progress_bar:
        
        # Accessing stored urlscan data
        urlscan_data = tool_results.get("1", {}).get("data", {})
        if urlscan_data:
            urlscan_malicious = 'Yes' if urlscan_data.get('verdicts', {}).get('overall', {}).get('malicious') else 'No'
            
            # Scoring logic for AbuseIPDB data
            if urlscan_malicious == 'Yes':
                varalyze_score += 10
                indicators.append("Flagged as malicious on URLScan")
        else:
            failed_tools.append("Note - URLScan failed to retrieve data which will effect the score given.")
            
        for i in range(1, 34):
            progress_bar.update(1)
            time.sleep(0.04)
        
        # Accessing stored VirusTotal data    
        virustotal_data = tool_results.get("2", {})
        if virustotal_data:
            virustotal_stats = virustotal_data.get('data', {}).get('attributes', {}).get('stats', {})
            if virustotal_stats:
                malicious = int(virustotal_stats.get('malicious', 0))  
                suspicious = int(virustotal_stats.get('suspicious', 0))  
                
                # Scoring logic for VirusTotal data
                if malicious >= 10:
                    varalyze_score += 40
                    indicators.append("Numerous vendors reported as malicious on VirusTotal (10+)")
                if (malicious < 10 and malicious > 1):
                    varalyze_score += 20
                    indicators.append("Several vendors reported as malicious on VirusTotal (1-10)")
                if suspicious >= 2:
                    varalyze_score += 20
                    indicators.append("Numerous vendors reported as suspicious on VirusTotal")
        else:
            failed_tools.append("Note - VirusTotal failed to retrieve data which will effect the score given.")
            
        for i in range(1, 34):
            progress_bar.update(1)
            time.sleep(0.04)

        # Accessing stored WhoIS data   
        whois_data = tool_results.get("3", {})
        if whois_data:
            whois_creation = whois_data.get("creation_date")
            whois_expiration = whois_data.get("expiration_date")
            
            # Processing creation/expiration date from list value
            if isinstance(whois_creation, list):
                whois_creation = whois_creation[0]
            if isinstance(whois_creation, datetime):
                domain_life = (datetime.now() - whois_creation).days      
            else:
                domain_life = None  
             
            if isinstance(whois_expiration, list):
                whois_expiration = whois_expiration[0]
            if isinstance(whois_expiration, datetime):
                domain_expire = (whois_expiration - datetime.now()).days
            else:
                domain_expire = None
            
            # Scoring logic for WhoIS data       
            if domain_life < 25:
                varalyze_score += 15
                indicators.append("Domain has been recently created within the last 25 days (very recent)")
            elif domain_life < 100:
                varalyze_score += 10
                indicators.append("Domain has been recently created within the last 100 days (fairly recent)")
        
            if domain_expire < 90:
                varalyze_score += 10
                indicators.append("Domain expiration upcoming")   
        else:
            failed_tools.append("Note - WhoIS failed to retrieve data which will effect the score given.") 
            
        for i in range(1, 35):
            progress_bar.update(1)
            time.sleep(0.04)
        
        # Restrict varalyze score (can exceed 100 incase of missing data so it still gives accurate scoring)
        varalyze_score = min(varalyze_score, 100)
        # Call report function to structure concatenated data
        return report_generation_url(varalyze_score, indicators)

# Function to structure IP report output and produce investigative tips 
def report_generation_ip(varalyze_score, indicators):
    if varalyze_score <= 25:
        threat_rank = Fore.GREEN + "Low" + Style.RESET_ALL
        investigative_steps = [
            "Varalyze has determined this IP address to be a " + Fore.GREEN + "low threat" + Style.RESET_ALL + " however the authenticity should always be checked further.",
            "Investigate the IP addresses activity across internal security logs.",
            "Check if any suspicious patterns can be seen & whether connections from this origin country are expected."
        ]
    elif (varalyze_score > 25 and varalyze_score <= 60):
        threat_rank = Fore.YELLOW + "Moderate" + Style.RESET_ALL
        investigative_steps = [
            "Varalyze has determined this IP address to be a " + Fore.YELLOW + "moderate threat" + Style.RESET_ALL + " however the authenticity should always be checked further.",
            "Ensure the reputation of the associated ISP/hosting service is legitimate.",
            "Investigate for any historical incidents related to this IP to gain a better understanding of it's potential nature.",
            "Verify if this IP is contained in any blocklists or flagged in security databases."
        ]
    elif (varalyze_score > 60 and varalyze_score <= 80):
        threat_rank = Fore.RED + "Suspicious" + Style.RESET_ALL
        investigative_steps = [
            "Varalyze has determined this IP address to be a " + Fore.RED + "suspicious threat" + Style.RESET_ALL + " that should be investigated further.",
            "Conduct a thorough investigation into what activity has been observed by this IP address across services.",
            "Research past incidents to see if this IP address has been seen before within your environment.",
            "Ensure traffic is being blocked by relevant security tooling, if not consider escalating up the chain of command."
        ]
    else:
        threat_rank = Fore.RED + "Highly suspicious" + Style.RESET_ALL
        investigative_steps = [
            "Varalyze has determined this IP address to be a " + Fore.RED + "highly suspicious threat" + Style.RESET_ALL + " that certainly should be investigated further.",
            "Ensure traffic is being blocked by relevant security tooling, if not strongly consider escalating up the chain of command.",
            "Under approval consider the use of isolation/blocking of related connections.",
            "Conduct a thorough investigation into what activity has been observed by this IP address across services.",
            "Research past incidents to see if this IP address has been seen before within your environment."
        ]
    
    report = "\033[1m" + "\n►►►►►►►►► Varalyze report ◄◄◄◄◄◄◄◄◄\n" + "\033[0m"   
    report += f"\nVaralyze score: {varalyze_score}\n"
    report += f"Ranking: {threat_rank}\n\n"
    report += f"Key factors:\n"
    for obs in indicators:
        report += f"  - {obs}\n"
    if failed_tools:
        report += f"* Note *"
        for tool in failed_tools:
            report += f"* {tool} *"
    report += f"\nInvestigative Tips:\n"
    for tip in investigative_steps:
        report += f"  - {tip}\n"
    
    return report 

# Function to structure domain report output and produce investigative tips 
def report_generation_url(varalyze_score, indicators):
    if varalyze_score <= 25:
        threat_rank = Fore.GREEN + "Low" + Style.RESET_ALL
        investigative_steps = [
            "Varalyze has determined this URL to be a " + Fore.GREEN + "low threat" + Style.RESET_ALL + " however the authenticity should always be checked further.",
            "Investigate the URL activity across internal security logs.",
            "Check if any suspicious patterns can be seen & whether connections to this domain are expected."
        ]
    elif (varalyze_score > 25 and varalyze_score <= 60):
        threat_rank = Fore.YELLOW + "Moderate" + Style.RESET_ALL
        investigative_steps = [
            "Varalyze has determined this URL to be a " + Fore.YELLOW + "moderate threat" + Style.RESET_ALL + " however the authenticity should always be checked further.",
            "Ensure the reputation of the associated hosting service is legitimate.",
            "Investigate for any historical incidents related to this URL to gain a better understanding of it's potential nature.",
            "Verify if this URL/domain is contained in any blocklists or flagged in security databases."
        ]
    elif (varalyze_score > 60 and varalyze_score <= 80):
        threat_rank = Fore.RED + "Suspicious" + Style.RESET_ALL
        investigative_steps = [
            "Varalyze has determined this URL to be a " + Fore.RED + "suspicious threat" + Style.RESET_ALL + " that should be investigated further.",
            "Conduct a thorough investigation into what activity has been observed related to this domain across services.",
            "Research past incidents to see if this domain has been seen before within your environment.",
            "Ensure traffic is being blocked by relevant security tooling, if not consider escalating up the chain of command."
        ]
    else:
        threat_rank = Fore.RED + "Highly suspicious" + Style.RESET_ALL
        investigative_steps = [
            "Varalyze has determined this URL to be a " + Fore.RED + "highly suspicious threat" + Style.RESET_ALL + " that certainly should be investigated further.",
            "Ensure traffic is being blocked by relevant security tooling, if not strongly consider escalating up the chain of command.",
            "Under approval consider the use of isolation/blocking of related connections.",
            "Conduct a thorough investigation into what activity has been observed by this domain across services.",
            "Research past incidents to see if this domain has been seen before within your environment."
        ]
    
    report = "\033[1m" + "\n►►►►►►►►► Varalyze report ◄◄◄◄◄◄◄◄◄\n" + "\033[0m"   
    report += f"\nVaralyze score: {varalyze_score}\n"
    report += f"Ranking: {threat_rank}\n\n"
    report += f"Key factors:\n"
    for obs in indicators:
        report += f"  - {obs}\n"
    if failed_tools:
        report += f"* Note *"
        for tool in failed_tools:
            report += f"* {tool} *"
    report += f"\nInvestigative Tips:\n"
    for tip in investigative_steps:
        report += f"  - {tip}\n"
    
    return report 

def main():
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║                          Report generation feature                         ║
║                                                                            ║ 
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║      Welcome to the report generation tool. This feature can be used to    ║
║          automate and produce comprehensive threat intel reports ...       ║
║                                                                            ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║                                
║              ▼ Choose an option from the list below to begin ▼             ║
║                                                                            ║
║                    TOOLS                          OTHER                    ║
║                                                                            ║
║                    1. IP Address                  3. Home page             ║
║                    2. Domain/URL                  4. Exit                  ║               
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
""")
    awaiting_valid_category = True
    while awaiting_valid_category:
        user_tool = input("Enter the number you wish to select: ")
        if user_tool == '1':
            multi_ip_check = input("Enter an IP address: ")
            tool_results = multi_use_tool.multi_ip_report(multi_ip_check)
            if tool_results:
                varalyze_report = ip_score_calculation(tool_results)
                print(varalyze_report)
                awaiting_valid_category = False
                invalid_re_run = True
                while invalid_re_run:
                    re_run_tool = input("\nWould you like to check another?\nEnter 'yes' or 'no'\n\nAnswer: ")
                    if re_run_tool == 'yes':
                        os.system('cls')
                        main()
                    else:
                        varalyze_cli.main()
            else:
                print("Error: Data missing please try again...")
        elif user_tool == '2':
            multi_url_check = input("Enter a url/domain: ")
            tool_results = multi_use_tool.multi_url_report(multi_url_check)
            if tool_results:
                varalyze_report = url_score_calculation(tool_results)
                print(varalyze_report)
                awaiting_valid_category = False
                invalid_re_run = True
                while invalid_re_run:
                    re_run_tool = input("\nWould you like to check another?\nEnter 'yes' or 'no'\n\nAnswer: ")
                    if re_run_tool == 'yes':
                        os.system('cls')
                        main()
                    else:
                        varalyze_cli.main()
            else:
                print("Error: Data missing please try again...")
        elif user_tool == '3':
            varalyze_cli.main()
        elif user_tool == '4':
            varalyze_cli.exit_program()
            return
        else:
            print("\nError: Invalid choice. Please select from 1-4...\n")
            
if __name__ == "__main__":
    main()