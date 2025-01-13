from shared_imports import os, time
import varalyze_cli

def api_key_check():
    api_keys = ["ABUSEIPDB_API_KEY", "IPQUALITY_API_KEY", "URLSCAN_API_KEY", "VIRUSTOTAL_API_KEY"]
    for key in api_keys:
        value = os.getenv(key)
        if value is not None:
            print(f"{key}: VALID")
        else:
            print(f"{key} is not set in the environment variables. Please retrieve your API key from the vendor and use the API config tool to help set it on your system.")

def main():
    print("\033[1m" + "\n►►►►►►►►► Welcome to the API key check ◄◄◄◄◄◄◄◄◄\n" + "\033[0m")
    api_key_check()
    print("\nReturning to main menu...")
    time.sleep(4)
    varalyze_cli.main()

if __name__ == "__main__":
    main()